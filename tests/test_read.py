from . import configure
from task_bypass.tasktypes.read.http_request import http_request, http_request_dynamic
import pytest
import pandas as pd
import vcr
import yaml

db = configure()

def request_dynamic_setup():

    # read in file infos
    with open("tests/test_yamls/test_http_request_dynamic.yml", "r") as stream:
        file_infos = yaml.safe_load(stream)

    request_infos = []
    for file_info in file_infos:
        # get file infos
        input_file = file_info['input_file']
        output_file = file_info['output_file']
        pagination = file_info['pagination']
        mapping_fields = file_info['mapping_fields']
        preserve_fields = file_info['preserve_fields']

        # create input & output dfs
        input_df = pd.read_csv(input_file)
        output_df = pd.read_csv(output_file)
        
        request_infos.append((db, input_df, output_df, pagination, mapping_fields, preserve_fields))

    return request_infos

@pytest.mark.parametrize("db, input_df, output_df, pagination, mapping_fields, preserve_fields", request_dynamic_setup())
@vcr.use_cassette("tests/cassettes/test_http_request_dynamic.yml", record_mode="new_episodes")
def test_http_request_dynamic(db, input_df, output_df, pagination, mapping_fields, preserve_fields):
    resp_df = http_request_dynamic(db, 'test_stage', 'test_id', input_df, preserve_fields, mapping_fields, pagination)
    print(output_df)
    print(resp_df)

    # because api return different message in different calling times
    # so use columns & length to do the test
    assert list(output_df.columns) == list(resp_df.columns)
    assert len(output_df.index) == len(resp_df.index)


def request_setup():

    # read in file infos
    with open("tests/test_yamls/test_http_request.yml", "r") as stream:
        file_infos = yaml.safe_load(stream)

    request_infos = []
    for file_info in file_infos:
        # get file infos
        input_file = file_info['input_file']
        output_file = file_info['output_file']
        extract_field = file_info['extract_field']
        preserve_origin_data = file_info['preserve_origin_data']

        # create input & output dfs
        input_df = pd.read_csv(input_file)
        if 'gzip' in output_file:
            f = open(output_file, "rb")
            binary_str = f.read()
            output_df = pd.DataFrame({"binary": [binary_str]})
        else:
            output_df = pd.read_csv(output_file)

        request_infos.append((db, input_df, output_df, extract_field, preserve_origin_data))

    return request_infos

@pytest.mark.parametrize("db, input_df, output_df, extract_field, preserve_origin_data", request_setup())
@vcr.use_cassette("tests/cassettes/test_http_request.yml", record_mode="new_episodes")
def test_http_request(db, input_df, output_df, extract_field, preserve_origin_data):
    resp_df = http_request(db, 'test_stage', 'test_id', input_df, extract_field, preserve_origin_data)

    # because api return different message in different calling times
    # so use columns & length to do the test
    assert list(output_df.columns) == list(resp_df.columns)
    assert len(output_df.index) == len(resp_df.index)
    
