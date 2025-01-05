from models import User, Item
from itemUtils import item_dict
from chain import check_bcoin_payment
import logging


def coin_conversion(user: User, coin_a: float, coin_b: float, txhash: str) -> bool:
    if coin_a != coin_b*10:
        return False
    
    if check_bcoin_payment(user.address, coin_b*(10**18), txhash):
        user.coin_a += coin_b*10
        return True
    else:
        return False

def acoin_buy_item(user: User, shopping_list: dict) -> bool:
    for item_id, amount in shopping_list.items():
        item_id = int(item_id)
        amount = int(amount)
        logging.info(item_id)
        logging.info(amount)
        if user.coin_a-item_dict[item_id][3] >= 0:
            user.coin_a -= item_dict[item_id][3]
        else:
            return False
        
        try:
            i = user.item_list.index(Item(item_id))
            user.item_list[i].amount += amount
        except:
            name = item_dict[item_id][0].value
            user.item_list.append(Item(item_id, item_dict[item_id][0].value, 1, item_dict[item_id][1]))
    return True