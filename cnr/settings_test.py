from dotenv import dotenv_values

from cnr.settings import *

MOCK_EXTERNAL_API = dotenv_values(".env.test")["MOCK_EXTERNAL_API"]
