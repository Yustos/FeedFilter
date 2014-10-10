# -*- coding: utf-8 -*-
from CodernityDB.database import Database
from CodernityDB.hash_index import HashIndex

class SettingsIndex(HashIndex):
    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = '32s'
        super(SettingsIndex, self).__init__(*args, **kwargs)

    def make_key(self, key):
        return md5(key).hexdigest()
    
    def make_key_value(self, data):
        a_val = data.get('name')
        if a_val is not None:
            return md5(a_val).hexdigest(), None

db = Database('settings')
if db.exists():
    db.open()
    db.reindex()
else:
    db.create()
    index = SettingsIndex(db.path, 'settingsidx')
    db.add_index(index)

class Entry():
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Settings():
    def __init__(self):
        
        self._db = db

    def get(self):
        records = self._db.all("settingsidx", with_doc=True)
        return [Entry(r["doc"]["name"], r["doc"]["value"]) for r in records]

    def getItem(self, name):
        record = self._db.get("settingsidx", name, with_doc=True)
        return record["doc"]["value"]

    def add(self, name, value):
        packedName = name.encode('utf-8')
        packedValue = value.encode('utf-8')
        updated = 0
        for curr in self._db.get_many("settingsidx", name, with_doc=True):
            updated = 1
            exist = curr["doc"]["value"]
            exist.append(value)
            self._db.update(curr["doc"])
        if not updated:
            self._db.insert(dict(name=packedName, value = [value]))

    def delete(self, name):
        for curr in self._db.get_many("settingsidx", name, with_doc=True):
            doc = curr['doc']
            self._db.delete(doc)
