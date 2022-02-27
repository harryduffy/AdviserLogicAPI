from AdviserLogic import adviserLogicAPI
import os
from dotenv import load_dotenv
import pandas as pd
from shareplum import Site
from shareplum import Office365
from shareplum.site import Version
import difflib
import subprocess 


load_dotenv()

def write_name_ls_to_file(full_names,file_name):

    f = open(f'{file_name}',"w")
    for full_name in full_names:
        f.write(full_name)
        f.write("@")

    f.close()

def get_list_of_names_from_file(file_name):
    f = open(f'{file_name}',"r")
    full_names = str(f.readline()).split("@")
    f.close()
    return full_names

def dict_name(client_name):
    """The function used to convert a client's Name into a dictionary identifying what each name is

    :param client_name: 
    :type client_name: 
    :return: 
    :rtype: 
    """
    name_ls = client_name.split('_')
    name_dict = {
        'fname':'',
        'sname':'',
        'pname':'',
        'p_fname':'',
        'p_sname':'',
        'p_pname':''
    }

    couple = False
    if len(name_ls) == 2:

        # can only be a single person
        name_dict["fname"]=name_ls[1]
        name_dict["sname"]=name_ls[0]


    elif len(name_ls) == 3:

        # can either be a single person with a nickname or a couple, same last name, without nicknames
        nickname, index, counter = check_nickname(name_ls)

        if nickname:
            name_dict["pname"]=name_ls[2]
            name_dict["fname"]=name_ls[1]
            name_dict["sname"]=name_ls[0]
        else:
            couple = True
            name_dict["sname"]=name_ls[0]
            name_dict["fname"]=name_ls[1]
            name_dict["p_fname"]=name_ls[2]
            name_dict["p_sname"]=name_ls[0]
            

    elif len(name_ls) == 4:
        # can either be a couple, same last name, with one nickname or a couple with different last names
        couple = True
        nickname, index, counter = check_nickname(name_ls)
        
        if nickname:

            first = False
            if index == 2:
                first = True

            if first:
                name_dict["sname"]=name_ls[0]
                name_dict["p_sname"]=name_ls[0]
                name_dict["fname"]=name_ls[1]
                name_dict["pname"]=name_ls[2]
                name_dict["p_fname"]=name_ls[3]
            else:
                name_dict["sname"]=name_ls[0]
                name_dict["p_sname"]=name_ls[0]
                name_dict["fname"]=name_ls[1]
                name_dict["p_fname"]=name_ls[2]
                name_dict["p_pname"]=name_ls[3] 
        else:
            name_dict["sname"]=name_ls[0]
            name_dict["fname"]=name_ls[1]
            name_dict["p_sname"]=name_ls[2]
            name_dict["p_fname"]=name_ls[3] 
        

    elif len(name_ls) == 5:
        # couple, same last name, both with a nickname
        # couple, different last name, with one nickname (two scenarios, depending on location of nickname)
        couple = True
        nickname, index, counter = check_nickname(name_ls)
        
        first = False
        if index == 2:
            first = True
        
        if nickname and counter == 2:
            name_dict["sname"]=name_ls[0]
            name_dict["p_sname"]=name_ls[0]
            name_dict["fname"]=name_ls[1]
            name_dict["pname"]=name_ls[2]
            name_dict["p_fname"]=name_ls[3]
            name_dict["p_pname"]=name_ls[4]
        else:
            if first:
                name_dict["sname"]=name_ls[0]
                name_dict["fname"]=name_ls[1]
                name_dict["pname"]=name_ls[2]
                name_dict["p_sname"]=name_ls[3]
                name_dict["p_fname"]=name_ls[4]

            else:
                name_dict["sname"]=name_ls[0]
                name_dict["fname"]=name_ls[1]
                name_dict["p_sname"]=name_ls[2]
                name_dict["p_fname"]=name_ls[3]
                name_dict["p_pname"]=name_ls[4]


    elif len(name_ls) == 6:
        # couple, different last name, with two nicknames
        couple = True
        name_dict["sname"]=name_ls[0]
        name_dict["fname"]=name_ls[1]
        name_dict["pname"]=name_ls[2]
        name_dict["p_sname"]=name_ls[3]
        name_dict["p_fname"]=name_ls[4]
        name_dict["p_pname"]=name_ls[5]
    
    name_dict["couple"] = couple
    return name_dict

def check_nickname(name_ls):

    nickname = False
    counter = 0
    index = 0

    for i in name_ls:
        if i[0] == "(":
            nickname = True
            index = name_ls.index(i)
            counter += 1

    return nickname, index, counter

def merge_name_dicts(d1,d2):

    names = ['sname','fname','pname','p_sname','p_fname','p_pname']
    for name in names:
        if not (d1[name]!= "" and d2[name]!="" ):
            if  d1[name]!= "":
                d2[name] = d1[name]
            else:
                d1[name] = d2[name]

    return d1

def name_dict_to_string(name_dict):
    name_ls =[]
    names = ['sname','fname','pname','p_sname','p_fname','p_pname']
    for name in names:
        if name_dict[name] != '':
            if name == "p_sname" and name_dict["p_sname"] == name_dict['sname']:
                pass
            else:
                name_ls.append(name_dict[name])
    return "_".join(name_ls)

def combine_names(n1,n2):
    n1_dict = dict_name(n1)
    n2_dict = dict_name(n2)
    combined_dict = merge_name_dicts(n2_dict,n1_dict)
    combined_name = name_dict_to_string(combined_dict)
    return combined_name

def full_names_from_ADLIDs(adl_ids,al):
    full_names =[]
    for adl_id in adl_ids:
        full_names.append(get_full_name_from_adlid(adl_id))
    return full_names


def get_full_name_from_adlid(adlid,al):
    basic_info_dict = al.get_client_data(adlid,'/')
    fname = basic_info_dict['clientBasicInfo']['firstName']
    sname = basic_info_dict['clientBasicInfo']['surName']
    pname = basic_info_dict['clientBasicInfo']['preferredName']

    partner_dict  = basic_info_dict['partner']
    pfname =''
    psname =''
    ppname =''

    if partner_dict != None :
        pfname = basic_info_dict['partner']['firstName']
        psname = basic_info_dict['partner']['surName']
        ppname = basic_info_dict['partner']['preferredName']

    name_ls = []
    if sname != '' and sname!= None : #If client entity is a Business and thus has no last name
        name_ls.append(sname)
    else: 
        name_ls.append(fname)
        full_name = "_".join(name_ls)
        return full_name

    name_ls.append(fname)
    if pname != '' and pname != None :
        name_ls.append(f'({pname})')
    if psname != '' and psname!= None and psname!=sname :
        name_ls.append(psname)
    if pfname != '' and pfname != None:
        name_ls.append(pfname)
    if ppname != '' and ppname != None:
        name_ls.append(f'({ppname})')

    full_name = "_".join(name_ls)
    return full_name
# nm_id_dict = {}
# al_nms_full = get_list_of_names_from_file("names2.txt")
# nm_id_zip = zip(al_nms_full,ids)
# for nm_id_tuple in nm_id_zip:
#     nm_id_dict[nm_id_tuple[0]]= nm_id_tuple[1]


# base_url = os.environ.get("BASE_URL")
# username = os.environ.get("EMAIL")
# password = os.environ.get("PASSWORD")
# authcookie = Office365(base_url, username=username, password=password).GetCookies()
# site = Site(f"{base_url}/sites/IPWSydney/", version=Version.v365, authcookie=authcookie)
# folder = site.Folder('Shared Documents/Clients-NEW1')

# folders_names = sorted(folder.folders)
# write_name_ls_to_file(folders_names,"folder_names.txt")


# al_names = get_list_of_names_from_file('names.txt')
# folder_names = get_list_of_names_from_file('folder_names.txt')


# while len(folder_names)>0:
#     folder = folder_names[0]
#     print(folder)
#     close_matches = difflib.get_close_matches(folder, al_names, 3,0.1)
#     print(close_matches)
#     entry = input("Which Matches?: ")
#     if entry == "1":
#         chosen = close_matches[0]
#     elif entry == "2":
#         chosen = close_matches[1]
#     elif entry == "`":
#         folder_names.pop(0)
#         print("\n")
#         continue
#     elif entry == "q":
#         write_name_ls_to_file(al_names,"names.txt")   
#         write_name_ls_to_file(folder_names,"folder_names.txt") 
#         quit()
    
#     al_names.pop(al_names.index(chosen))
#     folder_names.pop(0)
#     print("\n")
#     if chosen == folder:
#         continue

#     if chosen != folder:
#         combined_name = combine_names(folder,chosen)
#         subprocess.run("pbcopy", universal_newlines=True, input=combined_name)
#         combined_name_dict = dict_name(combined_name)
#         print("combined name\n" +combined_name)
#         adl_id = nm_id_dict[chosen]
#         print(adl_id)
#         al.put_client_data(adl_id, "/", ["clientBasicInfo","firstName"],combined_name_dict["fname"] )
#         al.put_client_data(adl_id, "/", ["clientBasicInfo","surName"],combined_name_dict["sname"])
#         print(al.put_client_data(adl_id, "/", ["clientBasicInfo","preferredName"],combined_name_dict["pname"].strip("(").strip(")")))

#         partner_dict  = al.get_specific_client_data(adl_id,"/", ["partner"])
#         if partner_dict != None :
#             al.put_client_partner_data(adl_id, "firstName", combined_name_dict["p_fname"])
#             al.put_client_partner_data(adl_id, "surName", combined_name_dict["p_sname"])
#             print(al.put_client_partner_data(adl_id, "preferredName", combined_name_dict["p_pname"].strip("(").strip(")")))



# write_name_ls_to_file(al_names,"names.txt")   
# write_name_ls_to_file(folder_names,"folder_names.txt") 