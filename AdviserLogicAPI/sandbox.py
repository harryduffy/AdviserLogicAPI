from AdviserLogic_API import AdviserLogicAPI
import os
from dotenv import load_dotenv

load_dotenv()

connector = AdviserLogicAPI(os.environ['KEY_USER_ID'], os.environ['KEY_PWD'], os.environ['PARAM_ID'])