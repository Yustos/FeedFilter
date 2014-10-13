# -*- coding: utf-8 -*-
from CodernityDB.database import Database
from CodernityDB.tree_index import TreeBasedIndex
import time
import collections

class LogIndex(TreeBasedIndex):
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

    def get(self, count):
        cnt = self._db.count(self._db.all, 'logidx')
        records = self._db.all("logidx", offset = cnt - int(count) if cnt - int(count) > 0 else 0, with_doc=True)
        result =  [dict(date = r["doc"]["date"], localDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(r["doc"]["date"])), client = r["doc"]["client"], message = r["doc"]["message"]) for r in records]
        return reversed(result)

    def add(self, date, client, message):
        self._db.insert(dict(date = date, client = client, message = message))
