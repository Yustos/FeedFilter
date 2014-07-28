# -*- coding: utf-8 -*-
from CodernityDB.database import Database
from CodernityDB.hash_index import HashIndex
import struct

class WithXIndex(HashIndex):

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = 's'
        super(WithXIndex, self).__init__(*args, **kwargs)

    def make_key_value(self, data):
        a_val = data.get("url")
        if a_val is not None:
            return a_val, None
        return None

    def make_key(self, key):
        return key

class Cache():
    def __init__(self):
        db = Database('db')
        if db.exists():
            db.open()
        else:
            db.create()
            x_ind = WithXIndex(db.path, 'urlidx')
            db.add_index(x_ind)
        #db.destroy()
        self._db = db

    def add(self, url, tags):
        print("add to cache: %s" % url)
        packedUrl = struct.pack("s", url.encode('utf-8'))
        self._db.insert(dict(url=packedUrl, tags = tags))

    def check(self, url):
        packedUrl = struct.pack("s", url.encode('utf-8'))
        item = self._db.get("urlidx", packedUrl)
        return not item is None