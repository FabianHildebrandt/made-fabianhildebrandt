from typing import Dict
import yaml
import pandas as pd
import wbgapi as wb
import os
import requests
from io import StringIO
import sqlite3

def read_pipeline_config(path : str = './pipeline-config.yaml') -> Dict:
    """
    Read out the pipeline configuration

    Args:
        path (str): Path to the config yaml file

    """
    print('\nReading configuration from the provided path...')
    try: 
        with open(path, "r", encoding='utf-8') as yamlfile:
            config = yaml.load(yamlfile, Loader=yaml.FullLoader)
        print("Successfully read yaml config file.")
        return config
    except Exception as e:
        print(f"Error reading configuration from the path {path}: {str(e)}")
        raise

class apiClient:
    def __init__(self, config : dict):
        """
        Initialize the an API client with the provided config
        
        Args:
            config (dict): pipeline configuration
        """
        try: 
            self.config = config
            self.indicators = {}
            self.countries = self.config['countries']
            self.start_year = self.config['date_range']['start_year']
            self.end_year = self.config['date_range']['end_year']
            self.indicator_data = pd.DataFrame()
            self._indicator_data_raw = pd.DataFrame()
            self._metadata_raw = pd.DataFrame()
            self.metadata = pd.DataFrame()
            self.output_path = 'data'
            self.debug = self.config['debug']
            if self.debug:
                if not os.path.exists('../data/pipeline_debug'):
                    os.makedirs('../data/pipeline_debug')
            # Create reverse look up table
            self.country_name_lookup = {v: k for k, v in self.countries.items()}
        except Exception as e:
            raise

    def check_and_clean(self, df : pd.DataFrame, output_path : str = 'data') -> pd.DataFrame:
        """
        Check the indicator quality and remove NaN values and load the quality 

        Args:
            df (pd.DataFrame): Dataframe to check and remove NaN values from
            output_path (str): Prefix of the output file to (opt.)

        Returns:
            df_cleaned (pd.DataFrame): Dataframe from which the NaN Values are removed
        """

        try:
            # check number of values
            row_cnt_raw = df.shape[0]

            # Check for duplicates and drop if any
            df = df.drop_duplicates(subset=['country', 'indicator', 'year']).reset_index(drop=True)
            row_cnt_duplicates = df.shape[0]
            
            # quality report
            indicator_quality = []
            for indicator in self.indicators:
                # get the name of the indicator
                name = indicator
                
                # calculate total number of values for the indicator
                total_values = df.loc[df['indicator'] == indicator].shape[0]
                
                # calculate the count of NaN values in 'value' column for the indicator
                nan_values = df.loc[df['indicator'] == indicator]['value'].isna().sum()
                
                # calculate the NaN ratio
                nan_ratio = nan_values / total_values 

                # determine for how many countries the data is available
                country_cnt = 0
                for country in self.country_name_lookup.keys():
                    country_df = df.loc[(df['indicator'] == indicator) & (df['country'] == country)]
                    country_total_values = country_df.shape[0]
                    country_nan_values = country_df['value'].isna().sum()
                    if country_nan_values == country_total_values:
                        country_cnt += 1 
                country_nan_ratio = country_nan_values / len(self.country_name_lookup.keys())
                
                # create a summary for the indicator
                indicator_summary = {'Indicator Name': name, 'NaN Ratio': nan_ratio, 'Country NaN Ratio': country_nan_ratio}
                indicator_quality.append(indicator_summary)
            
            quality_df = pd.DataFrame(indicator_quality)
            if self.debug: 
                quality_df.to_excel(f'../data/pipeline_debug/{output_path}_quality.xlsx')

            df = df.dropna()

            row_cnt_nan = df.shape[0]

            print(f'Removed {row_cnt_duplicates-row_cnt_nan} nan values and {row_cnt_raw-row_cnt_duplicates} duplicates')
        except Exception as e:
            print(f'Error checking and removing the indicator data: {str(e)}')

        return df
    
    def collect_indicator_metadata(self) -> pd.DataFrame:
        """Method to collect indicator metadata"""
        return None
    
    def clean_indicator_metadata(self) -> pd.DataFrame:
        """Method to clean indicator metadata"""
        return None
    
    def collect_indicator_data(self) -> pd.DataFrame:
        """Method to collect indicator data"""
        return None
    
    def clean_indicator_data(self) -> pd.DataFrame:
        """Method to clean indicator data"""
        return None
    
    def load_data(self):
        """Load cleaned metadata and indicator data to an SQLite database file."""

        print('\nLoading the extracted indicator data and metadata to an SQLite database...')

        # Check if there is any data to load
        if self.metadata.shape[0] == 0:
            raise Exception('Error loading metadata: No metadata available.')
        if self.indicator_data.shape[0] == 0:
            raise Exception('Error loading indicator data: No indicator data available.')
        
        # Define the database path and table names
        db_path = f'../data/{self.output_path}.sqlite'  
        metadata_table = 'metadata'                     
        indicator_data_table = 'indicator_data'         

        try:
            # Connect to the SQLite database (creates file if it doesn’t exist)
            with sqlite3.connect(db_path) as conn:
                # Write DataFrames to tables within the database
                self.indicator_data.to_sql(indicator_data_table, conn, if_exists='replace', index=False)
                self.metadata.to_sql(metadata_table, conn, if_exists='replace', index=False)

            print(f'Data successfully loaded to SQLite database at: {db_path}')

        except Exception as e:
            print(f'Error loading indicator data and metadata to SQLite database: {str(e)}')
            raise
    
    def run_pipeline(self):
        """Retrieve indicator data and metadata and load it to a sink"""

        print('\nRunning the pipeline to extract, transform and load data...')

        self.collect_indicator_metadata()
        self.clean_indicator_metadata()
        self.collect_indicator_data()
        self.clean_indicator_data()
        self.load_data()

        print('Successfully finished the pipeline.')
   
class WorldBankAPI(apiClient):
    """
    A client for the World Bank Indicators API V2 that uses the pipeline configuration file.
    More information on the utilized wbgapi library can be found here: https://pypi.org/project/wbgapi/
    """
    
    def __init__(self, config : dict ):
        """
        Initialize the World Bank API client with the provided config
        
        Args:
            config (dict): pipeline configuration
        """

        print('\n--------------------------------------------')
        print('World Bank Indicators Pipeline')
        print('--------------------------------------------')
        print('\nInitializing the World Bank Indicators API client...')

        try: 
            super().__init__(config)
            self.indicators = self.config['world_bank_api']['indicators']
            self.output_path = self.config['world_bank_api']['output_path']
            print(f'Successfully initialized the World Bank Indicators API client.')
        except Exception as e:
            print(f"Error initializing the client: {str(e)}")
            raise

    
    def collect_indicator_metadata(self) -> pd.DataFrame:
        """Collect the metadata for the indicators"""

        print('\nCollecting the metadata for the configured indicators...')

        metadata_list = []
        for indicator_id in self.indicators:
            if self.debug:
                print(f'Fetching metadata for {indicator_id}')
            try:
                metadata = {}    
                metadata = wb.series.metadata.get(indicator_id).__dict__['metadata']
                metadata['id'] = indicator_id
                metadata_list.append(metadata)
            except Exception as e:
                print(f'Error fetching metadata for indicator {indicator_id}: {str(e)}')
                raise
            
        print(f'Successfully collected the metadata for {len(self.indicators)} configured indicators.')
        self._metadata_raw = pd.DataFrame(metadata_list)

        # store df in xlsx file 
        if self.debug:
            self._metadata_raw.to_excel(f'../data/pipeline_debug/{self.output_path}_metadata_raw.xlsx')

        return self._metadata_raw
    
    def clean_indicator_metadata(self) -> pd.DataFrame:
        """Clean the obtained metadata such that it conly contains the configured attributes"""

        print('\nCleaning the metadata for the configured indicators...')

        if self._metadata_raw is None or type(self._metadata_raw) != pd.DataFrame :
            raise ValueError(f"The provided metadata data type {type(self._metadata_raw)} doesn't match the required datatype (pd.DataFrame).")
        
        try:
            metadata = self._metadata_raw
            self.metadata = pd.DataFrame(metadata)[self.config['world_bank_api']['metadata_attributes']]
            print('Successfully cleaned the metadata.')
        except Exception as e:
            print(f'Error cleaning metadata: {str(e)}')
            raise

        # store df in xlsx file 
        if self.debug:
            self.metadata.to_excel(f'../data/pipeline_debug/{self.output_path}_metadata_cleaned.xlsx')
        
        return self.metadata
    
    def collect_indicator_data(self) -> pd.DataFrame:
        """Collect the indicator data"""

        print('\nCollecting the data for the configured indicators...')

        try:    
            self._indicator_data_raw = wb.data.DataFrame(series=self.indicators, economy=self.country_name_lookup.keys(), time=range(self.start_year, self.end_year+1,1))
            print(f'Successfully collected the indicator data of {len(self.indicators)} indicators for {len(self.country_name_lookup.keys())} countries from {self.start_year} to {self.end_year}')
        except Exception as e:
            print(f'Error reading indicator data: {str(e)}')
            raise

        # store df in xlsx file 
        if self.debug:
            self._indicator_data_raw.to_excel(f'../data/pipeline_debug/{self.output_path}_indicator_data_raw.xlsx')
    
        return self._indicator_data_raw
    
    def clean_indicator_data(self) -> pd.DataFrame:
        """Clean the collected indicator data"""

        print('\nCleaning the collected indicator data...')

        try:
            df = self._indicator_data_raw
            if isinstance(df.index, pd.MultiIndex):
                df = df.reset_index()  
            else:
                df = df.reset_index(drop=True)

            df = pd.melt(df, id_vars=['economy', 'series'], var_name='year', value_name='value')

            # rename the columns
            df = df.rename(columns={'economy':'country', 'series':'indicator'})

            #  Clean the 'year' column by removing the "YR" prefix and converting to integers -> easier access later
            df['year'] = df['year'].str.replace('YR', '').astype(int)

            # Ensure values ares numeric
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            
            self.indicator_data = self.check_and_clean(df, self.output_path)
            
            print(f'Successfully cleaned the indicator data.')

        except Exception as e:
            print(f'Error cleaning indicator data: {str(e)}')
            raise

        # store df in xlsx file 
        if self.debug:
            self.indicator_data.to_excel(f'../data/pipeline_debug/{self.output_path}_indicator_data_cleaned.xlsx')
        
        return self.indicator_data
    
    

class OurWorldInData(apiClient):
    """A client to access the dataset provided by the [*Our World in Data*](https://ourworldindata.org) research initiative"""

    def __init__(self, config : dict):
        """
        Initialize the OWID client with the provided config
        
        Args:
            config (dict): pipeline configuration
        """

        print('\n--------------------------------------------')
        print('Our World in Data Pipeline')
        print('--------------------------------------------')
        print('\nInitializing the Our World in Data client...')

        try: 
            super().__init__(config)
            self.indicators = self.config['owid_api']['indicators']
            self.output_path = self.config['owid_api']['output_path']
            print(f'Successfully initialized the Our World in Data API client.')
        except Exception as e:
            print(f"Error initializing the client: {str(e)}")
            raise
        pass
        
    def collect_indicator_metadata(self) -> pd.DataFrame:
        """Downloads CO2 emissions metadata from OWID GitHub repository."""
        
        print('\nCollecting the metadata from the Our World in Data repository...')

        try:    
            self._metadata_raw = self.extract_from_csv(self.config['owid_api']['metadata_url'])
            print(f'Successfully collected the metadata data from the Our World in Data repository containing {self._metadata_raw.shape[0]} rows.')
        except Exception as e:
            print(f'Error reading indicator data: {str(e)}')
            raise

        # store df in xlsx file 
        if self.debug:
            self._metadata_raw.to_excel(f'../data/pipeline_debug/{self.output_path}_metadata_raw.xlsx')
    
        return self._metadata_raw

    def clean_indicator_metadata(self) -> pd.DataFrame:
        """Clean the obtained metadata such that it conly contains the configured attributes"""

        print('\nCleaning the metadata for the configured indicators...')

        if self._metadata_raw is None or type(self._metadata_raw) != pd.DataFrame :
            raise ValueError(f"The provided metadata data type {type(self._metadata_raw)} doesn't match the required datatype (pd.DataFrame).")
         
        try:
            metadata = self._metadata_raw
            self.metadata = pd.DataFrame(metadata)[self.config['owid_api']['metadata_attributes']]
            print('Successfully cleaned the metadata.')
        except Exception as e:
            print(f'Error cleaning metadata: {str(e)}')
            raise

        # store df in xlsx file 
        if self.debug:
            self.metadata.to_excel(f'../data/pipeline_debug/{self.output_path}_metadata_cleaned.xlsx')
        
        return self.metadata

    def collect_indicator_data(self) -> pd.DataFrame:
        """Downloads CO2 emissions data from OWID GitHub repository."""
        
        print('\nCollecting the data from the Our World in Data repository...')

        try:    
            self._indicator_data_raw = self.extract_from_csv(self.config['owid_api']['data_url'])
            print(f'Successfully collected the indicator data from the Our World in Data repository containing {self._indicator_data_raw.shape[0]} rows.')
        except Exception as e:
            print(f'Error reading indicator data: {str(e)}')
            raise

        # store df in xlsx file 
        if self.debug:
            self._indicator_data_raw.to_excel(f'../data/pipeline_debug/{self.output_path}_indicator_data_raw.xlsx')
    
        return self._indicator_data_raw

    def clean_indicator_data(self) -> pd.DataFrame:
        """Clean the collected indicator data"""

        print('\nCleaning the collected indicator data...')

        try:
            df = self._indicator_data_raw
            columns_to_keep = self.indicators + ['year', 'iso_code']
            df = df.loc[:, columns_to_keep]
            df = df.rename(columns={'iso_code':'country'})
            df = df[
                (df['country'].isin(self.country_name_lookup.keys())) &
                (df['year'] >= self.start_year) &
                (df['year'] <= self.end_year)
            ]
            # convert dataframe to long format (same as for the other dataset)
            df = pd.melt(
                df,
                id_vars= ['year', 'country'],
                value_vars= self.indicators,
                value_name= 'value',
                var_name='indicator'
                )
            
            self.indicator_data = self.check_and_clean(df, self.output_path)

            print(f'Successfully cleaned the indicator data.')
            
        except Exception as e:
            print(f'Error cleaning the indicator data {str(e)}')
            raise

        # store df in xlsx file 
        if self.debug:
            self.indicator_data.to_excel(f'../data/pipeline_debug/{self.output_path}_indicator_data_cleaned.xlsx')
        
        return self.indicator_data 

    def extract_from_csv(self, url : str) -> pd.DataFrame:
        """
        Reads a CSV file from a given URL

        Args:
            url (str): URL of the file to extract
        """

        try:
            # Fetch the content from the URL
            response = requests.get(url, verify=True)  
            response.raise_for_status()  
            # Load the content into a df
            csv_data = pd.read_csv(StringIO(response.text))
            return csv_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None


if __name__ == "__main__":
    # Read out config 
    pipeline_config = read_pipeline_config('./pipeline-config.yaml')
    # Initialize clients with config and run the pipelines
    wbclient = WorldBankAPI(pipeline_config)
    wbclient.run_pipeline()
    owidclient = OurWorldInData(pipeline_config)
    owidclient.run_pipeline()
