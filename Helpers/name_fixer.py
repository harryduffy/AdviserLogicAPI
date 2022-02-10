from AdviserLogicAPI import AdviserLogicAPI
import os
from dotenv import load_dotenv
import pandas as pd
from Exceptions import ResourceNotFoundError

load_dotenv()

al = AdviserLogicAPI(os.environ['KEY_USER_ID'], os.environ['KEY_PWD'], os.environ['PARAM_ID'])

nms_ids = pd.read_excel("Nms_ADLIDs.xlsx")
ids = nms_ids["Client.ADLID"].to_list()
nms = nms_ids["Client.Full Name"].to_list()

def write_name_ls_to_file(full_names):

    f = open('names.txt',"a")
    for full_name in full_names:
        f.write(full_name)
        f.write("@")

    f.close()

def get_list_of_names_from_file():
    f = open('names.txt',"r")
    full_names = f.readline().split["@"]
    return full_names


full_names =[]
for id in ids:
    fname = str(al.get_specific_client_data(id,'/',['clientBasicInfo','firstName']))
    sname = str(al.get_specific_client_data(id,'/',['clientBasicInfo','surName']))
    pname = str(al.get_specific_client_data(id,'/',['clientBasicInfo','preferredName']))

    partner_dict  = al.get_specific_client_data(id,"/", ["partner"])
    pfname =''
    psname =''
    ppname =''

    if partner_dict != None :
        pfname = str(al.get_specific_client_data(id,'/',['partner','firstName']))
        psname = str(al.get_specific_client_data(id,'/',['partner','surName']))
        ppname = str(al.get_specific_client_data(id,'/',['partner','preferredName']))
    name_ls = []
    name_ls = [sname,fname]
    if pname != '':
        name_ls.append(f'({pname})')
    if psname != '' and psname!=sname:
        name_ls.append(psname)
    if pfname != '':
        name_ls.append(pfname)
    if ppname != '':
        name_ls.append(f'({ppname})')

    full_name = "_".join(name_ls)

    f = open('names.txt',"a")
    f.write(full_name)
    f.write("@")
    f.close()
    print(full_name)


