from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
from models import User, Cat, Item
import logging
import os

load_dotenv()

_database_link = os.getenv('DB_LINK')
_cert_path = os.getenv('DB_CERT_PATH')

client = MongoClient(_database_link, tlsCertificateKeyFile=_cert_path)
db = client['pawtopia']
users_db = db['users']
cats_db = db['cats']
# items_db = db['items'] 

def get_user_by_address(addr:str) -> User:
    try:
        user = users_db.find_one({'_id': addr})
        logging.info("Encoded"+str(user))
        #logging.info(type(user))
        user = User().deserialize(user)
        cat = cats_db.find_one({'_id': user.cat_id})
        if cat is not None:
            cat = Cat().deserialize(cat)
        user.cat = cat
        logging.info("Decoded"+str(user.coin_a))
        
        return user
    except Exception as e:
        logging.error(e)
        return None
def set_user(user:User) -> bool:
    try:
        user = user.serialize()
        logging.info('encoded:' + str(user))
        if user['cat'] is not None:
            cat = user['cat']
            del user['cat']
            cid  = cat['_id']
            del cat['_id']
            cats_db.replace_one({'_id': cid}, cat, upsert=True)
        uid = user['_id']
        del user['_id']
        r = users_db.update_one({'_id': uid}, {'$set': user}, upsert=True)
        logging.info(r.modified_count, r.matched_count)
        logging.info(r.raw_result)
        return r.modified_count > 0
    except Exception as e:
        logging.error(e)
        return False
def create_user(user:User) -> bool:
    try:
        user = user.serialize()
        users_db.insert_one(user)
        return True
    except Exception as e:
        logging.error(e)
        return False