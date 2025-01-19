from pipeline import read_config
# import the necessary packages
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import geopandas as gpd
import os 
import yaml
import pandas as pd
import sqlite3
from functools import reduce

def query_indicator_data(db_path : str, indicator : str, countries : tuple,  year_range : tuple, table_name : str = 'indicator_data') -> pd.DataFrame:
    '''
    Query an indicator from a SQLite database:

    Args:
        db_path (str): Path to the SQLite database
        indicator (str): Name of the indicator to be queried
        countries (tuple): Countries to be queried
        year_range (tuple): Start year, end year
        table_name (str): Name of the table containing the indicator data

    Returns:
        data (pd.DataFrame): Dataframe containing all rows for the provided indicator, countries, year range and table
    '''
    # make sure that indicator name is in quotation marks for query
    indicator = f"'{indicator}'"

    # SQL query to fetch data
    query = f"""
    SELECT * 
    FROM {table_name} 
    WHERE country IN {countries} 
    AND indicator = {indicator} 
    AND year BETWEEN {year_range[0]} AND {year_range[1]}
    """

    print(f"\nQuerying indicator data of indicator {indicator}...")
    try: 
        # Fetch data from SQLite
        with sqlite3.connect(db_path) as conn:
            data = pd.read_sql_query(sql=query, con=conn).reset_index(drop=True)

            # Ensure data is sorted by country and year
            data = data.sort_values(by=['country', 'year'])

            print(f'Successfully queried the data of the indicator {indicator}.')

            return data
    except Exception as e:
        print(f"Error querying indicator data configuration from the path {db_path}: {str(e)}")
        raise

def calculate_rate_of_change(data: pd.DataFrame) -> pd.DataFrame:
    '''
    Calculate the annual rate of change in % for a DataFrame containing the data for a single indicator.

    Args:
        data (pd.DataFrame): Expects a DataFrame with the following columns: country, year, value for a single indicator.

    Returns: 
        DataFrame containing the rate of change, NaN if indicator data is missing for a single year.
    '''
    # Ensure data is sorted by country and year
    data = data.sort_values(by=['country', 'year'])

    # Group data by country and calculate the annual rate of change
    def compute_group_rate_of_change(group):
        group['year_diff'] = group['year'].diff()
        # Only consecutive years
        group = group[group['year_diff'] == 1]
        group['value'] = group['value'].pct_change() * 100
        return group

    # Apply transformation to each group
    data = data.groupby('country', group_keys=False).apply(compute_group_rate_of_change)

    return data.reset_index(drop=True)

def rank_countries_by_indicator(data : pd.DataFrame, indicator : str = 'value', high_rank_last : bool = False, new_name : str = '') -> pd.DataFrame:
    """
    Rank countries based on their indicator value

    Args:
        data (pd.DataFrame): Dataframe containing indicator data
        high_rank_last (bool): High values get low ranking (HIGHEST -> last place)
        new_name (str): Rename the indicator, if necessary

    Returns: 
        DataFrame with the country as index and the ranking (named by the indicator)
    """

    # Group by country and calculate the mean value
    if 'value' in data.columns:
        data = data.groupby('country')['value'].mean()
    else:
        data = data.groupby('country')[indicator].mean()

    # Drop NaN values
    data.dropna(axis=0, inplace=True)

    # Sort the data based on high_rank_last
    sorted_data = data.sort_values(ascending=True)
    if high_rank_last:
        # High values rank last 
        ranks = range(1, len(sorted_data) + 1)
    else:
        # High values rank first 
        ranks = range(len(sorted_data), 0, -1)

    # Create a DataFrame with rankings
    ranking_df = pd.DataFrame({
        'country': sorted_data.index,
        f'{indicator}': ranks
    }).set_index('country').sort_values(by=indicator, ascending=True)

    # Rename the indicator 
    if new_name:
        ranking_df = ranking_df.rename(columns={indicator: new_name})

    return ranking_df

def extract_gdf(path : str) -> gpd.GeoDataFrame:
    """
    Extracts a geopandas dataframe containing the GeoDataFrame with the country geometries

    Args: 
        path (str): Path to the shapes file (.shp) containing the GeoData

    Returns: 
        GeoDataFrame with all countries and their shapes
    """
    print(f'\nReading out the GeoPandas data from {path}...')

    try:
        gdf = gpd.read_file(path)
        print('Successfully read out the Geopandas data.')
    except Exception as e:
        print(f'Error reading out GeoPandas data from path {path}: {str(e)}')
        raise

    return gdf

def clean_gdf(gdf : gpd.GeoDataFrame, config : dict) -> gpd.GeoDataFrame:
    """
    Cleans the GeoDataFrame to contain only a list of specified countries/ continents

    Args:
        gdf (gpd.GeoDataFrame): Geopandas data with countries and their shapes
        config (dict): Pipeline config containing all countries

    Return:
        Cleaned GeoDataFrame containing only the required columns
    """

    print(f'\nCleaning GeoPandas data...')

    try:
        # Drop all columns but geometry, NAME, CONTINENT, WB_A3
        gdf = gdf[['NAME', 'WB_A3' ,'geometry']]

        # rename WB_A3 column to country
        gdf = gdf.rename(columns={'WB_A3':'country'})

        # Define the country list to filter within the Americas
        country_list = list(config['countries'].values())

        # Filter the Americas dataset for the countries in the list
        gdf = gdf[gdf["country"].isin(country_list)]

        gdf.reset_index(drop=True, inplace=True)
        gdf.set_index('country', inplace=True)

        print(f'Successfully cleaned the GeoPandas data.')

        return gdf

    except Exception as e:
        print(f'Error cleaning GeoPandas data: {str(e)}')
        raise

def plot_gdf(gdf : gpd.GeoDataFrame, column : str, suptitle : str):
    """
    Plots the GeoDataFrame using the column and stores the plot to a provided filepath

    Args: 
        gdf (gpd.GeoDataFrame): GeoDataFrame containing the country data and their ranking
        column (str): Name of the column that contains the ranking
        suptitle (str): Title of the ranking/ report (e. g. SCA 2024)
    """

    # Ensure the directory exists
    if not os.path.exists('./figures'):
        os.makedirs('./figures')
    
    gdf = gdf.sort_values(by=column, ascending=True)

    filtered_df = gdf[gdf[column].notna()]

    top_10 = filtered_df.head(10)
    bottom_10 = filtered_df.tail(10)

    countries_of_interest = pd.concat([top_10, bottom_10])

    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot()

    gdf.plot(column=column, cmap = 'RdYlGn_r', ax = ax, alpha = 0.7, edgecolor='black', legend=False, missing_kwds = {'color':'lightgrey'})

    # Create legend handles
    legend_handles = [
        mpatches.Patch(color=color, label=f"{int(score)}: {name}")
        for score, name, color in zip(
            countries_of_interest[column], 
            countries_of_interest['NAME'], 
            plt.cm.RdYlGn_r(countries_of_interest[column] / max(countries_of_interest[column]))  # Normalize scores
        )
    ]
    # Adjust this to show other continents
    ax.set_xlim(left=-190, right=20)
    # Make sure that the legend is properly displayed
    ax.legend(handles=legend_handles, title = 'Ranking', loc='center right', fontsize='medium', bbox_to_anchor = (1.0,0.5))

    # turn off axis ticks
    ax.set_xticks([])
    ax.set_yticks([])

    # set the plot title
    plt.title(f"{suptitle}\n{column}", weight = 'bold', fontsize='large')

    # save the plot
    column_name = column[:30]
    path = f'./figures/{column_name}.png'
    plt.savefig(path, dpi = 300)

    plt.close()

def create_and_plot_combined_ranking(rankings : list, gdf: gpd.GeoDataFrame, ranking_name : str, suptitle : str, minimum_data_ratio : float = 0.7):
    '''
    Combine multiple rankings to one joint ranking and plot the results.

    Args:
        rankings (list): List of ranking DataFrames, where each DataFrame contains a single ranking and the index column 'country'.
        gdf (gpd.GeoDataFrame): Contains the shapes of the countries.
        ranking_name (str): Title of the ranking
        suptitle (str): Title of the ranking/ report (e. g. SCA 2024)
        minimum_data_ratio (float): Ratio of the available rankings between 0 and 1, countries with a lower ratio are excluded.
    '''
    rankings = reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True, how='outer'), rankings)

    # Create Excel sheet with ranking results
    rankings.to_excel(f'./data/{ranking_name}.xlsx')
    
    excluded_countries = []

    for country in rankings.index:
        country_rankings = rankings.loc[country]
        no_nan_values = len(country_rankings) - country_rankings.isna().sum()
        if no_nan_values / len(rankings.columns) < minimum_data_ratio:
            rankings.drop(index=country, inplace=True)
            excluded_countries.append(country)

    rankings = rankings.mean(axis=1, skipna=True)
    rankings = pd.DataFrame(rankings)
    rankings.columns = [ranking_name]
    rankings = rank_countries_by_indicator(rankings, ranking_name, high_rank_last=True)
    merged_ranking_gdf = pd.merge(cleaned_gdf, rankings, left_index=True, right_index=True, how='outer')

    print(excluded_countries)

    plot_gdf(merged_ranking_gdf, column=ranking_name, suptitle = suptitle)


if __name__ == "__main__":

    # Set the suptitle of the comparison
    suptitle = 'SCA 2024'

    # Read out config 
    config = read_config('./config.yaml')
    gdf = extract_gdf("./data/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp")
    cleaned_gdf = clean_gdf(gdf, config)

    # Extract the test indicators
    countries = tuple(config['countries'].values())

    # Extract rankings
    rankings = config['sca']

    # Extract the year range for the ranking
    year_range = (config['date_range']['start_year'], config['date_range']['end_year'])

    # Extract the datasources used for the ranking
    datasources = config['sca']

    overall_ranking = []
    rising_stars_ranking = []
    latecomers_ranking = []

    for datasource in datasources:
        # Create the database path for the current datasource
        db_path = f'../data/{datasource}.sqlite'

        for indicator in config['sca'][datasource]:
            # Read the full indicator description from the config
            indicator_description = config['sca'][datasource][indicator]['description']
            # Check whether the indicator is ranked ascending/ descending 
            indicator_high_rank_last = config['sca'][datasource][indicator]['high_rank_last']

            # Query the indicator data and calculate the rate of change
            indicator_data = query_indicator_data(db_path, indicator, countries, year_range)
            rate_of_change_indicator_data = calculate_rate_of_change(indicator_data)

            # Create the rankings for the overall ranking
            overall_ranking_df = rank_countries_by_indicator(indicator_data, indicator, high_rank_last=indicator_high_rank_last, new_name=indicator_description)
            rising_stars_label = f'Rate of Change: {indicator_description}'
            rising_stars_ranking_df = rank_countries_by_indicator(rate_of_change_indicator_data, indicator, high_rank_last=indicator_high_rank_last, new_name=rising_stars_label)            

            # Plot each indicator ranking 
            merged_overall_gdf = pd.merge(cleaned_gdf, overall_ranking_df, left_index=True, right_index=True, how='outer')
            merged_rising_stars_df = pd.merge(cleaned_gdf, rising_stars_ranking_df, left_index=True, right_index=True, how='outer')

            plot_gdf(merged_overall_gdf, indicator_description, suptitle) 
            plot_gdf(merged_rising_stars_df, rising_stars_label, suptitle)

            overall_ranking.append(overall_ranking_df)
            rising_stars_ranking.append(rising_stars_ranking_df)

    create_and_plot_combined_ranking(overall_ranking, cleaned_gdf, 'Overall Champion', suptitle=suptitle)
    create_and_plot_combined_ranking(rising_stars_ranking, cleaned_gdf, 'Rising Stars', suptitle=suptitle)

