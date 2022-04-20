import json
import os
from app import app, db
from models.Country import Country

def build_db_from_json():
    """
    Build table from json function
    This function batch loads json files from a landing folder. Once loaded, deletes the file from the folder to make the folder idempotent effectively not allowing duplicates to be added
    """
    country_obj_list = []
    path = "json_data"
    files_in_path = os.listdir(path)
    count = len(files_in_path)
    if count !=0:
        for file_name in os.listdir(path):
            file_path = path + "/" + str(file_name)
            with open(file_path, encoding="utf8") as input_file:
                array_obj = json.loads(input_file.read())
                for x in array_obj:
                    country = str(x["country"])
                    city = str(x["name"]) 
                    country_obj = Country(country=country, city=city)
                    country_obj_list.append(country_obj)
            print (f"bulk insert of {file_name} started")
            db.session.bulk_save_objects(country_obj_list)
            db.session.commit()
            print (f"bulk insert of {file_name} ended")
        print (f"bulk insert ended, deleting the files in {path} now")
        make_json_data_directory_idempotent(path)
    else:
        pass

def make_json_data_directory_idempotent(path):
    try:
        for file_name in os.listdir(path):
            if file_name.endswith('.json'):
                print (f"removing {file_name}")
                os.remove(path + "/" + str(file_name))
        else:
            pass
    except OSError as e:  ## if failed, report it back to the user ##
        print ("Error: %s - %s." % (e.filename, e.strerror))





