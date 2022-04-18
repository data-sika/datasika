# read content function
## read content based on user & task inputs
## NOTE: might need to think of some parrellal solutions for this function
import pandas as pd
from task_bypass.tasktypes.read.http_request import http_request, http_request_dynamic

def read_content(task_id, inputs, function, _from_output = None):
    # for now all the read_content will do http_request related jobs

    result_lists = []
    if 'user_input' in inputs:
        user_input = inputs['user_input']
        extract_field = None
        if 'extract_field' in user_input:
            extract_field = user_input['extract_field']

        if function == 'http-request':
            if user_input['file_format'] == 'csv':
                if extract_field:
                    input_df = pd.read_csv(user_input['file_name'])
                    rows = input_df[extract_field]
                else:
                    input_df = pd.read_csv(user_input['file_name'], header=None)
                    # default take index 0 column as input
                    rows = input_df[0]
                ## NOTE
                for row in rows:
                    # each of url df will produce a str df in return
                    row_df = pd.DataFrame([row])
                    result_df = http_request(row_df)
                    # add dataframe into lists (produce list of dataframes)
                    result_lists.append(result_df)

                return {
                    task_id: result_lists
                }

    if 'task_inputs' in inputs:
        task_input = inputs['task_inputs'][0]
        if function == 'http-request':
            result_lists = []
            extract_field = None
            if 'extract_field' in task_input:
                extract_field = task_input['extract_field']

            for single_df in _from_output:
                if extract_field:
                    # each of single df will produce a df in return
                    result_df = http_request(single_df, extract_field)

                # no specific extract field
                else:
                    # each of extract df will produce a df in return
                    result_df = http_request(single_df)

                # add dataframe into lists (produce list of dataframes)
                result_lists.append(result_df)

            return {
                task_id: result_lists
            }

        if function == "http-request-dynamic":
            user_input = inputs['user_input']
            params_df = pd.DataFrame({
                'base_url': [user_input['base_url']],
            })

            mapping_items = user_input['params_dynamic']
            fixed_items = user_input['params_fixed']
            param_dict = {}
            preserve_fields = []
            result_lists = []
            mapping_fields = {}
            for single_df in _from_output:
                for item in mapping_items:
                    param_dict[item['name']] = list(single_df[item['value']])
                    preserve_fields.append(item['name'])
                    mapping_fields[item['name']] = item['value']

                params_df = pd.DataFrame(param_dict)

                for item in fixed_items:
                    params_df[item['name']] = item['value']

                params_df['base_url'] = user_input['base_url']

                if 'headers' in user_input:
                    params_df['headers'] = json.dumps(user_input['headers'])

                result_df = http_request_dynamic(params_df, preserve_fields, mapping_fields)

                result_lists.append(result_df)

            return {
                task_id: result_lists
            }







    return {}

