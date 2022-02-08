import os
from re import S
from dotenv import load_dotenv

import requests
import json
from Exceptions import APIHealthFail, AuthenticationFail, ResourceNotFoundError

load_dotenv()

class Get:

    def __init__(self, key_user_id, key_pwd, param_id):
        """Constructor method for Get class.
        """
        self._key_user_id = key_user_id
        self._key_pwd = key_pwd
        self.param_id = param_id
        self._authenticated = False
        self._base_url = 'https://factfinder.adviserlogic.com/api/v1/'
        self.headers = {'keyUserID': key_user_id, 
                        'keyPwd': key_pwd, 
                        'paramUID': param_id,
                        'adlClientID': ''}

        self.authenticate()

    def __repr__(self):
        return self.param_id

    def authenticate(self):
        """Authenticate the API user using Adviser Logic's required parameters.
        """

        # begin by checking the API health
        response = requests.get(self._base_url + 'Status/api-health')
        if response.status_code != 200:
            raise APIHealthFail()
        
        # then, attempt to authenticate the user
        response = requests.get(self._base_url + 'custom-form-schema',
        headers=self.headers)
        if response.status_code != 200:
            raise AuthenticationFail()
        else:
            self._authenticated = True
        
    def is_authenticated(self):
        return self._authenticated
    
    """
    URL Endpoint Suffixes for Client ID only:
        - /
        - /assets
        - /consultant
        - /contact-detail
        - /dependant
        - /entity
        - /estate-planning
        - /expense
        - /healthinfo
        - /income
        - /insurance
        - /liabilities
        - /superfund
    """
    def get_client_data(self, adl_client_id, url_endpoint_suffix):

        if self.is_authenticated():

            self.headers['adlClientID'] = adl_client_id

            response = requests.get(self._base_url + 'client' + url_endpoint_suffix,
            headers=self.headers)

            if response != 200:
                raise ResourceNotFoundError

            data = json.loads(response.content)

            return data
            
        else:
            raise AuthenticationFail()


get = Get(os.environ['KEY_USER_ID'], os.environ['KEY_PWD'], os.environ['PARAM_ID'])

print(get.get_content('ADL6289433', '/'))
