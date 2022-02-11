from AdviserLogic import AdviserLogicAPI
import os
from dotenv import load_dotenv
import pandas as pd
from Exceptions import ResourceNotFoundError

load_dotenv()

connector = AdviserLogicAPI(os.environ['KEY_USER_ID'], os.environ['KEY_PWD'], os.environ['PARAM_ID'])

nms_ADLIDs = pd.read_excel("Nms_ADLIDs.xlsx")
ADLIDs = nms_ADLIDs["Client.ADLID"].to_list()
nms = nms_ADLIDs["Client.Full Name"].to_list()


# connector.makeshift_post_client_data( "ADL6059791","/customformdata", {
#     "fieldData": [
#         {
#         "variableName": "DOB",
#         "value": "string"
#         },
#         {
#         "variableName": "partnerDOB",
#         "value": "string2"
#         }
#     ]
#     } , "True DOB")
# quit()

# i = 0
# while i < len(ADLIDs):
#     print(nms[i])
#     connector.post_client_data( ADLIDs[i],"/customformdata", {
#     "fieldData": [
#         {
#         "variableName": "DOB",
#         "value": "string"
#         },
#         {
#         "variableName": "partnerDOB",
#         "value": "string2"
#         }
#     ]
#     } , "True DOB")

#     i +=1



# connector.put_client_data('1151100', "/customformdata", ['clientFormData', 'fieldData', [1, 'value']], "1949-06-25", 'True DOB' )
# # connector.put_client_data('1151100',"/", ["clientBasicInfo","dateOfBirth"],"1950-01-01" )
# quit()

bdays = []
while len(ADLIDs)>1:
    nm = nms.pop(0)
    id = str(ADLIDs.pop(0))
    print(nm)
    
    bday = str(connector.get_specific_client_data(id,"/", ["clientBasicInfo","dateOfBirth"]))
    partner_dict  = connector.get_specific_client_data(id,"/", ["partner"])
   
    if partner_dict != None :
        print("partner found")
        p_bday = str(connector.get_specific_client_data(id,"/", ["partner","dateOfBirth"]))
        p_year = int(p_bday.split("-")[0])
        if p_year < 1950:
            connector.put_client_partner_data(id, "dateOfBirth","1950-01-01")
        
        
        if p_bday != "1950-01-01":
            connector.put_client_data(id, "/customformdata", ['clientFormData', 'fieldData', [2, 'value']] , p_bday, 'True DOB' )


    year = int(bday.split("-")[0])
    print(year)
    if year < 1950:
        connector.put_client_data(id, "/", ["clientBasicInfo","dateOfBirth"], "1950-01-01" )
    
    if bday != "1950-01-01":
        connector.put_client_data(id, "/customformdata", ['clientFormData', 'fieldData', [1, 'value']], bday, 'True DOB' )
    print("cycle complete")