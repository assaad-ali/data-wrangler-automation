import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIRECTORY = os.path.join(BASE_DIR, 'data')
LOGS_DIRECTORY = os.path.join(BASE_DIR, 'logs')
MODELS_DIRECTORY = os.path.join(BASE_DIR, 'models')

# Other configurations
DEFAULT_RANDOM_STATE = 42
DEFAULT_TEST_SIZE = 0.2
