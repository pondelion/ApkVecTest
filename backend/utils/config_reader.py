import yaml
import os
from .logger import Logger


DEFAULT_MP_FILEPATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..',
    'config/materials_project.yml'
)
DEFAULT_AWS_FILEPATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..',
    'config/aws.yml'
)


def _load_mp_config(filepath: str=DEFAULT_MP_FILEPATH):
    return yaml.safe_load(open(filepath))


def _load_aws_config(filepath: str=DEFAULT_AWS_FILEPATH):
    return yaml.safe_load(open(filepath))


class _MPConfig(type):
    config = _load_mp_config()

    def __getattr__(cls, key: str):
        try:
            return cls.config[key]
        except Exception as e:
            Logger.e(__class__, f'No config value found for {key}')
            raise e


class _AWSConfig(type):
    config = _load_aws_config()

    def __getattr__(cls, key: str):
        try:
            return cls.config[key]
        except Exception as e:
            Logger.e(__class__, f'No config value found for {key}')
            raise e


class MPConfig(metaclass=_MPConfig):
    pass


class AWSConfig(metaclass=_AWSConfig):
    pass
