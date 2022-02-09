import pandas as pd
import os
from dotenv import load_dotenv
from AdviserLogicAPI import AdviserLogicAPI

load_dotenv()
connector = AdviserLogicAPI(os.environ['KEY_USER_ID'], os.environ['KEY_PWD'], os.environ['PARAM_ID'])


class Abstractions:

    @classmethod
    def generate_call_list(cls):
        """Generate the Review Call List midway through the month
        """
        data = pd.read_excel("Nms_ADLIDs.xlsx")
        adl_ids = data["Client.ADLID"].to_list()
        names = data["Client.Full Name"].to_list()

        ids_names_dict = dict(zip(names, adl_ids))
        for k, v in ids_names_dict.items():
            print(k, v)

    

        # loop through the names and get the aldIDs in a dictionary with the name as the key and value as the aldIDs, then go through the aldIDs and check the last review_date (simple timedelta and print the clients required for a review call)

print(Abstractions.generate_call_list())