import datetime
import logging

class User:
    def __init__(self) -> None:
        self.address = None
        self.cat_id = None
        self.item_list = []
        self.active_item_list = [] # for furniture in use
        self.coin_a = 0
        self.daliy_update_timestamp = datetime.datetime.fromtimestamp(0)
        self.cat = None
    def deserialize(self, data:dict):
        for key, value in data.items():
            if key == 'item_list':
                setattr(self, key, [Item().deserialize(item) for item in value])
            elif key == '_id':
                self.address = value
            elif key == 'active_item_list':
                setattr(self, key, [Item().deserialize(item) for item in value])
            else:
                setattr(self, key, value)
        return self
    def serialize(self) -> dict:
        data = {}
        for key, value in self.__dict__.items():
            if key == 'item_list':
                data[key] = [item.serialize() for item in value]
            elif key == 'address':
                data['_id'] = value
            elif key == 'active_item_list':
                data[key] = [item.serialize() for item in value]
            elif key == 'cat':
                if value is None:
                    data[key] = None
                else:    
                    data[key] = value.serialize()
            else:
                data[key] = value
        logging.info(data)
        return data
        
class Item:
    def __init__(self, item_id=-1, item_type=-1, item_amount=0, item_name= '') -> None:
        self.id = item_id
        self.type = item_type
        self.amount = item_amount
        self.name = item_name

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.id == other.id
        return False
    
    def serialize(self) -> dict:
        data = {}
        for key, value in self.__dict__.items():
            if key == 'id':
                data['_id'] = value
            else:
                data[key] = value
        return data
    def deserialize(self, data:dict):
        for key, value in data.items():
            if key == '_id':
                self.id = value
            else:
                setattr(self, key, value)
        return self

class Cat:
    def __init__(self) -> None:
        self.id = -1
        self.happiness = 0
        self.energy = 0
        self.texture = 0
        self.token_id = 0
        self.is_active = False
    def serialize(self) -> dict:
        data = {}
        for key, value in self.__dict__.items():
            if key == 'id':
                data['_id'] = value
            else:
                data[key] = value
        return data
    def deserialize(self, data:dict):
        for key, value in data.items():
            if key == '_id':
                self.id = value
            else:
                setattr(self, key, value)
        return self
        