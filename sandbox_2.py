from AdviserLogicAPI import AdviserLogicAPI
import os
from dotenv import load_dotenv
from Exceptions import APIHealthFail, AuthenticationFail, ResourceNotFoundError

load_dotenv()

connector = AdviserLogicAPI(os.environ['KEY_USER_ID'], os.environ['KEY_PWD'], os.environ['PARAM_ID'])

test_response = {
  "id": "ADL6289433",
  "formName": "TS3",
  "clientFormData": [
    {
      "id": 1,
      "fieldData": [
        {
          "variableName": "caption3",
          "value": "yooooo"
        },
        {
          "variableName": "testdate",
          "value": "2022-02-10"
        }
      ]
    }
  ],
  "partnerFormData": []
}

custom_form_id = 1
custom_variable = "testdate"
value = "WAZA"

form_dicts = test_response["clientFormData"]
targetted_form_dict = {}

for form_dict in form_dicts:
    if form_dict["id"] == custom_form_id:
        targetted_form_dict = form_dict

if targetted_form_dict == {}:
    raise ResourceNotFoundError("No matching custom form found using ID.")

field_data = targetted_form_dict["fieldData"]

targetted_field = {}
for field_dict in field_data:
    if custom_variable in field_dict.values():
        targetted_field = field_dict

if targetted_field =={}:
    raise ResourceNotFoundError("No matching custom variable found in forms field dictionarys.")

targetted_field["value"] = value

print(test_response)