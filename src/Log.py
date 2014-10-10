# -*- coding: utf-8 -*-
from CodernityDB.database import Database
from CodernityDB.hash_index import HashIndex

class LogIndex(HashIndex):
    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = 'f'
        super(LogIndex, self).__init__(*args, **kwargs)

    def make_key(self, key):
        return key
    
    def make_key_value(self, data):
        a_val = data.get('date')
        if a_val is not None:
            return a_val, None

db = Database('log')
if db.exists():
    db.open()
    db.reindex()
else:
    db.create()
    index = LogIndex(db.path, 'logidx')
    db.add_index(index)

class Log():
    def __init__(self):
        self._db = db

    def get(self):
        records = self._db.all("logidx", with_doc=True)
        return [dict(date = r["doc"]["date"], client = r["doc"]["client"], message = r["doc"]["message"]) for r in records]

    def add(self, date, client, message):
        self._db.insert(dict(date = date, client = client, message = message))
