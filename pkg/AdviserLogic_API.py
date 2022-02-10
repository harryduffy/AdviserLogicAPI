from re import I
import requests
import json
from Exceptions import APIHealthFail, AuthenticationFail, ResourceNotFoundError

class AdviserLogicAPI:

    def __init__(self, key_user_id, key_pwd, param_id):
        """Constructor method for Get class.
        """
        self._key_user_id = key_user_id
        self._key_pwd = key_pwd
        self.param_id = param_id
        self._authenticated = False
        self._base_url = 'https://factfinder.adviserlogic.com/api/v1/'
        self.headers = {'keyUserId': key_user_id, 
                        'keyPwd': key_pwd, 
                        'paramUID': param_id,
                        'adlClientID': ''}

        self.authenticate()

    def __repr__(self):
        return self.param_id

    def authenticate(self):
        """Authenticate the API user using Adviser Logic's required parameters.
        """

        response = requests.get(self._base_url + 'Status/api-health')
        if response.status_code != 200:
            raise APIHealthFail

        response = requests.get(self._base_url + 'custom-form-schema', headers=self.headers)
        if response.status_code != 200:
            raise AuthenticationFail
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
    def get_client_data(self, adl_client_id, url_endpoint_suffix, form_name=None):

        if self.is_authenticated():

            if form_name == None:
                self.headers['adlClientID'] = adl_client_id
                response = requests.get(self._base_url + 'client' + url_endpoint_suffix, headers=self.headers)


                if response.status_code != 200:
                    raise ResourceNotFoundError

                data = json.loads(response.content)

                return data
            else:
                self.headers['adlClientID'] = adl_client_id
                self.headers['formName'] = form_name
                response = requests.get(self._base_url + 'client' + url_endpoint_suffix, headers=self.headers)


                if response.status_code != 200:
                    raise ResourceNotFoundError

                data = json.loads(response.content)

                return data
            
        else:
            raise AuthenticationFail

    def get_specific_client_data(self, adl_client_id, url_endpoint_suffix, key_path_list):

        if self.is_authenticated():

            data = self.get_client_data(adl_client_id, url_endpoint_suffix)
            value = data
            for key in key_path_list:
                value = value[key]
            
            return value

        else:
            raise AuthenticationFail


    def put_client_data(self, adl_client_id, url_endpoint_suffix, key_path_list, value, form_name=None):

        if self.is_authenticated():

            data = self.get_client_data(adl_client_id, url_endpoint_suffix, form_name)
            
            self.i = 0
            def form_json_replacer(current):
   
                if type(current) == dict:

                    for k, v in current.items(): 
                        
                        if k == key_path_list[len(key_path_list) - 1][1]:
                            self.i += 1
                            if self.i == key_path_list[len(key_path_list) - 1][0]:
                                current[k] = value
                                return

                        if type(v) == dict or type(v) == list:
                            form_json_replacer(v)

                elif type(current) == list:
                    
                    for item in current:
                        if item == key_path_list[len(key_path_list) - 1]:
                            current[current.index(item)] = value
                            return
                        
                        if type(item) == dict or type(item) == list:
                            form_json_replacer(item)
            
            def json_replacer(current):
                                    
                for k, v in current.items(): 
                    
                    if k == key_path_list[len(key_path_list) - 1]:
                        current[k] = value
                        return

                    if type(v) == dict:
                        json_replacer(v)

            if form_name != None:
                form_json_replacer(data)
                data2 = data["clientFormData"][0]
            else:
                json_replacer(data)
                data2 = data
                        
            response = requests.put(self._base_url + 'client' + url_endpoint_suffix, headers=self.headers, json=data2)

            return response

        else:
            raise AuthenticationFail


    def put_client_partner_data(self, adl_client_id, partner_attribute, value):

        if self.is_authenticated():

            data = self.get_client_data(adl_client_id = adl_client_id, url_endpoint_suffix="/")["partner"]
            
            data[partner_attribute]= value
                        
            response = requests.put(self._base_url + 'client/partner', headers=self.headers, json=data)

            return response

        else:
            raise AuthenticationFail