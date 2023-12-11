import os
import json


def load_variable(name: str, default: str = None, throw_error: bool = True, message: str = ""):
    value = os.getenv(name, default)

    if value is None and throw_error is True:
        raise Exception(f'Missing Required Environment Var: {name} {message} ')
    return value




class EnvironmentUtility:
    
    AWS_PROFILE = load_variable('AWS_PROFILE', throw_error=False)
    AWS_REGION = load_variable('AWS_REGION', throw_error=False)


