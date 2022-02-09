from subprocess import call
from time import strftime
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime, date, timedelta
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
        date_in_month = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        date_in_month = date.fromisoformat(date_in_month)
        call_list = {}
        for k, v in ids_names_dict.items():
            
            current_client_review_date = connector.get_specific_client_data(v, '/', ['additionalDetails', 'nextReviewDate'])

            if current_client_review_date != None:
                next_review_date = date.fromisoformat(current_client_review_date)
                
                if next_review_date <= date_in_month:
                    call_list[k] = next_review_date.strftime('%Y-%m-%d')
                    print(call_list[k])


        return call_list

print(Abstractions.generate_call_list())