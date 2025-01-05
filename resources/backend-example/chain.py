import web3
import logging
import os
from dotenv import load_dotenv
from abi import abi_coin,abi_cat
from models import User, Cat, Item
from database import *
load_dotenv()

w3 = web3.Web3(web3.HTTPProvider(os.getenv('ETH_PROVIDER')))

def check_bcoin_payment(address:str, amount:int, txhash:str) -> bool:
    try:
        tx = w3.eth.get_transaction(txhash)
        contr = w3.eth.contract(address=os.getenv('COIN_ADDR'), abi=abi_coin)
        data = contr.decode_function_input(tx.input)
        
        return data[0].fn_name=='transfer' and data[1]['to']==os.getenv('PAYMENT_ADDR') and data[1]['amount']==amount and tx['from']==address
        
    except Exception as e:
        logging.error(e)
        return False
def check_bcoin_balance(address:str) -> int:
    try:
        contr = w3.eth.contract(address=os.getenv('COIN_ADDR'), abi=abi_coin)
        return contr.functions.balanceOf(address).call()
    except Exception as e:
        logging.error(e)
        return -1
def get_claim_cat_id(address:str,txhash:str):
    try:
        contr = w3.eth.contract(address=os.getenv('CAT_ADDR'), abi=abi_cat)
        tx_receipt = w3.eth.wait_for_transaction_receipt(txhash, timeout=10) 
        logs = contr.events.Transfer().process_receipt(tx_receipt)
        log = logs[0]
        if log['args']['to'] == address:
            return log['args']['tokenId']
        else:
            return None
    except Exception as e:
        print (e)
        return None
def align_cat():
    i = 0
    while True:
        try:
            contr = w3.eth.contract(address=os.getenv('CAT_ADDR'), abi=abi_cat)
            own = contr.functions.ownerOf(i).call()
            print (own)
            usr =  get_user_by_address(own)
            if usr is not None:
                if usr.cat_id is None or usr.cat_id != i:
                    usr.cat_id = i
                    print (usr.cat_id)
                    usr.cat = Cat()
                    usr.cat.id = i
                    set_user(usr)
            i += 1                 
        except:
            break