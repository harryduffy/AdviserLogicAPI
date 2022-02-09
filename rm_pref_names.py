from AdviserLogicAPI import AdviserLogicAPI
import os
from dotenv import load_dotenv
import pandas as pd
from Exceptions import ResourceNotFoundError

load_dotenv()

connector = AdviserLogicAPI(os.environ['KEY_USER_ID'], os.environ['KEY_PWD'], os.environ['PARAM_ID'])

nms_ADLIDs = pd.read_excel("Nms_ADLIDs.xlsx")
ADLIDs = nms_ADLIDs["Client.ADLID"].to_list()
nms = nms_ADLIDs["Client.Full Name"].to_list()

# connector.put_client_data(adl_client_id="ADL6289433",url_endpoint_suffix="/", key_path_list=["clientBasicInfo","preferredName"], value="Jim")
# connector.put_client_partner_data('1157514', "preferredName", '')
# quit()
# connector.put_client_data("ADL6289433","/", ["clientBasicInfo","preferredName"], None)


first_names = []
while len(ADLIDs)>1:
    nm = nms.pop(0)
    aDLID = str(ADLIDs.pop(0))
    print(nm)
    try:
        fname = connector.get_specific_client_data(aDLID,"/", ["clientBasicInfo","firstName"] )
        pname = connector.get_specific_client_data(aDLID,"/", ["clientBasicInfo","preferredName"])

        
        partner_dict  = connector.get_specific_client_data(aDLID,"/", ["partner"])

        if partner_dict != None :
            print("partner found")
            p_fname = partner_dict["firstName"]
            p_pname = partner_dict["preferredName"]
            print(p_fname,p_pname)
            if p_fname == p_pname:
                print("replaced partner")
                connector.put_client_partner_data(aDLID, "preferredName", '')


        
        print(fname,pname)
        if fname == pname:
            print("found one")
            connector.put_client_data(aDLID,"/", ["clientBasicInfo","preferredName"], '')

        

        first_names.append( fname)
        print(len(ADLIDs))
    except ResourceNotFoundError:
        print(nm + "=============================================FAILED")



