import json

def load_json_data(file_name: str, base_path: str= './data', lambda_func=None):
    '''
    Load JSON data from a file and optionally apply a lambda function to it.
    Args:
        file_name (str): The name of the JSON file to load.
        base_path (str, optional): The base path where the JSON file is located. Defaults to './data'.
        lambda_func (function, optional): A lambda function to apply to the loaded data. Defaults to None.
    Returns:
        The loaded JSON data, optionally processed by the lambda function.
    '''
    file_path = f"{base_path}/{file_name}" if base_path else file_name
    with open(file_path, 'r') as f:
        data = json.load(f)
        return lambda_func(data) if lambda_func else data