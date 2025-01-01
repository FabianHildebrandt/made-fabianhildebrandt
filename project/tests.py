import pytest
import os
import sqlite3
import pandas as pd
from typing import Type

from pipeline import (
    read_config, 
    WorldBankAPI, 
    OurWorldInData
)

class TestAPIClient:
    """
    Generic test class for the pipelines of both clients.
    """

    # Fixture provides a fix configuration for all of the following test cases -> repeated usage of the config
    @pytest.fixture(scope='module')
    def pipeline_config(self):
        """Fixture to load test pipeline config"""
        config_path = './pipeline-test-config.yaml'
        return read_config(config_path)

    # test will twice: once for the WorldBankAPI client and once for the OWID client
    @pytest.mark.parametrize("client_class", [WorldBankAPI, OurWorldInData])
    def test_api_pipeline(self, pipeline_config, client_class: Type):
        """
        Test the API clients with the following test cases:
        1. Client initialization
        2. Metadata collection
        3. Metadata cleaning
        4. Indicator data collection
        5. Indicator data cleaning
        6. Execute the complete pipeline + load data to SQLite DB
        """
        # 1. Client initialization
        client = client_class(pipeline_config)
        assert client is not None, f"{client_class.__name__} should be created successfully"
        
        # check if indicators are defined
        assert len(client.indicators) > 0, "Indicators should be defined for the client"
        # check if countries are defined
        assert len(client.countries) > 0, "Indicators should be defined for the client"
        
        # 2. Metadata collection
        metadata = client.collect_indicator_metadata()
        assert not metadata.empty, "Metadata shouldn't be empty"
        
        # 3. Metadata cleaning
        cleaned_metadata = client.clean_indicator_metadata()
        assert not cleaned_metadata.empty, "Cleaned metadata shouldn't be empty"
        
        # 4. Indicator data collection
        indicator_data = client.collect_indicator_data()
        assert not indicator_data.empty, "Indicator data shouldn't be empty"
        
        # 5. Indicator data cleaning
        cleaned_indicator_data = client.clean_indicator_data()
        assert not cleaned_indicator_data.empty, "Cleaned indicator data shouldn't be empty"
        assert cleaned_indicator_data['value'].notna().all(), "No NaN values should remain after cleaning the indicator data"
        
        # 6. Execute the complete pipeline + load data to SQLite DB
        client.run_pipeline()
        
        # Verify SQLite DB creation
        db_path = f'../data/{client.output_path}.sqlite'
        assert os.path.exists(db_path), "SQLite database should be created"
        
        # Verify that database is not empty
        with sqlite3.connect(db_path) as conn:
            # Check indicator_data 
            indicator_data_db = pd.read_sql_query("SELECT * FROM indicator_data LIMIT 5", conn)
            assert not indicator_data_db.empty, "Indicator data table shouldn't be empty"
            
            # Check metadata 
            metadata_db = pd.read_sql_query("SELECT * FROM metadata LIMIT 5", conn)
            assert not metadata_db.empty, "Metadata table shouldn't be empty"

        