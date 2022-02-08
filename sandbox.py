from AdviserLogicAPI import AdviserLogicAPI
import os
from dotenv import load_dotenv

load_dotenv()

connector = AdviserLogicAPI(os.environ['KEY_USER_ID'], os.environ['KEY_PWD'], os.environ['PARAM_ID'])

# connector.put_client_data('ADL6289433', '/contact-detail', 'clientContact/homeAddress/line1', 'Grove Lane')
# connector.get_client_data('ADL6289433', '/')
print(connector.get_specific_client_data('ADL6289433', '/contact-detail', 'id'))