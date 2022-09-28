from cnr.settings import *
from dotenv import dotenv_values

MOCK_EXTERNAL_API = dotenv_values(".env.test")["MOCK_EXTERNAL_API"]