from models import *
from itemUtils import item_dict

def daily_update(user: User) -> None:
    
    if user is None:
        return
    if 'daliy_update_timestamp' not in user.__dict__:
        user.daliy_update_timestamp = datetime.datetime.fromtimestamp(0)
    #Check if update is done today
    if user.daliy_update_timestamp is not None:
        if user.daliy_update_timestamp.day == datetime.datetime.now().day:
            return
    #Check if user has a cat
    if user.cat is not None:
        user.cat.happiness -= 5
        user.cat.energy -= 5
        if user.cat.happiness < 0:
            user.cat.happiness = 0
        if user.cat.energy < 0:
            user.cat.energy = 0
    user.daily_update_timestamp = datetime.datetime.now()
    user.coin_a += 10
    for item in user.active_item_list:
        user.cat.happiness += item_dict[item.id][2]
    return