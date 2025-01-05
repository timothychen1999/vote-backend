from enum import Enum
import logging
from models import User, Item
import random

class ItemType(Enum):
    Food = 0
    Toy = 1
    Furniture = 2
    Gacha = 3
    Appearance = 4

class ItemName(Enum):
    ball = 0
    flower = 1
    flower1 = 2
    bench = 3
    deco1 = 4
    deco2 = 5
    floormat = 6
    fountain = 7
    soft = 8
    softwithpillow = 9
    gacha = 10
    defaultskin = 11
    normalskin1 = 12
    normalskin2 = 13
    milk = 14
normal_skin_count = 2

# {id: [type,name,value,price]}
_item_dict = {ItemName.ball: [ItemType.Toy, "ball", 1, 3],
             ItemName.flower: [ItemType.Toy, "flower", 1, 5],
             ItemName.flower1: [ItemType.Toy, "flower1", 1, 5],
             ItemName.bench: [ItemType.Furniture, "bench", 1, 10],
             ItemName.deco1: [ItemType.Furniture, "deco1", 1, 10],
             ItemName.deco2: [ItemType.Furniture, "deco2", 1, 10],
             ItemName.floormat: [ItemType.Furniture, "floormat", 1, 10],
             ItemName.fountain: [ItemType.Furniture, "fountain", 1, 10],
             ItemName.soft: [ItemType.Furniture, "soft", 1, 10],
             ItemName.softwithpillow: [ItemType.Furniture, "softwithpillow", 1, 15],
             ItemName.gacha: [ItemType.Gacha, "gacha", -1, 5],
             ItemName.defaultskin: [ItemType.Appearance, "default_skin", -1, 0],
             ItemName.normalskin1: [ItemType.Appearance, "normalskin1", -1, 20],
             ItemName.normalskin2: [ItemType.Appearance, "normalskin2", -1, 20],
             ItemName.milk: [ItemType.Food, "milk", 5, 3]
             }
item_dict = {}
for key, value in _item_dict.items():
    item_dict[key.value] = value

def put_down_furniture(user: User, item_id) -> bool:
    tmp_item = Item(item_id)
    try:
        i = user.item_list.index(tmp_item)
        if user.item_list[i].amount > 0:
            user.item_list[i].amount -= 1
            try:
                j = user.active_item_list.index(tmp_item)
                user.active_item_list[j].amount += 1
            except:
                user.active_item_list.append(Item(item_id, ItemType.Furniture.value, 1, user.item_list[i].name))
            return True
        else:
            return False
    except:
        return False

def take_back_furniture(user: User, item_id) -> bool:
    try:
        tmp_item = Item(item_id)
        i = user.active_item_list.index(tmp_item)
        user.active_item_list[i].amount -= 1
        if user.active_item_list[i].amount == 0:
            user.active_item_list.pop(i)
        
        j = user.item_list.index(tmp_item)
        user.item_list[j].amount += 1
        return True
    except:
        return False

def feed_your_cat(user: User, item_id) -> bool:
    cat = user.cat
    if cat.is_active == False:
        return False

    try:
        tmp_item = Item(item_id)
        i = user.item_list.index(tmp_item)
        user.item_list[i].amount -= 1
        if user.item_list[i].amount == 0:
            user.item_list.pop(i)
        cat.energy += item_dict[item_id][2]
        return True
    except:
        return False

def play_with_cat(user: User, item_id) -> bool:
    cat = user.cat
    if cat.is_active == False:
        logging.info("cat is not active")
        return False

    try:
        tmp_item = Item(item_id)
        i = user.item_list.index(tmp_item)
        user.item_list[i].amount -= 1
        if user.item_list[i].amount == 0:
            user.item_list.pop(i)
        cat.happiness += item_dict[item_id][2]
        logging.info("play with cat")
        
        return True
    except Exception as e:
        logging.error(e)
        return False

def roll_a_skin(user, item_id) -> bool:
    skins = [i for i in range(ItemName.defaultskin+1, ItemName.defaultskin+1+normal_skin_count)]

    try:
        tmp_item = Item(item_id)
        i = user.item_list.index(tmp_item)
        user.item_list[i].amount -= 1
        if user.item_list[i].amount == 0:
            user.item_list.pop(i)
        result_skin = random.choice(skins)
        skin_item = Item(result_skin, item_dict[result_skin][0], 1, item_dict[result_skin][1])

        try:
            i = user.item_list.index(skin_item)
            user.item_list[i].amount += 1
        except:
            user.item_list.append(Item(result_skin, ItemType.Appearance.value, 1, item_dict[result_skin][1]))
        return True
    except:
        return False

def change_appearance(user, item_id) -> bool:
    cat = user.cat
    if cat.is_active == False:
        return False

    try:
        tmp_item = Item(item_id)
        i = user.item_list.index(tmp_item)
        if user.item_list[i].amount > 0:
            user.item_list[i].amount -= 1
            j = user.item_list.index(cat.texture)
            user.item_list[j].amount += 1
            cat.texture = item_id
            return True
        else:
            return False
    except:
        return False

def use_item(user: User, item_id) -> bool:
    item_id = int(item_id)
    logging.info(f"item_id: {item_id}")
    if item_dict[item_id][0] == ItemType.Toy:
        return play_with_cat(user, item_id)
    elif item_dict[item_id][0] == ItemType.Furniture:
        return put_down_furniture(user, item_id)
    elif item_dict[item_id][0] == ItemType.Food:
        return feed_your_cat(user, item_id)
    elif item_dict[item_id][0] == ItemType.Gacha:
        return roll_a_skin(user, item_id)
    elif item_dict[item_id][0] == ItemType.Appearance:
        return change_appearance(user, item_id)
    else:
        raise Exception(f"Invalid item type {item_dict[item_id][0]}")
