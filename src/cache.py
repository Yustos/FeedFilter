# -*- coding: utf-8 -*-
from CodernityDB.database import Database
from CodernityDB.hash_index import HashIndex
import struct
import CacheIndex

class Cache():
    def __init__(self):
        db = Database('db')
        if db.exists():
            db.open()
        else:
            db.create()
            index = CacheIndex.UrlIndex(db.path, 'urlidx')
            db.add_index(index)
        self._db = db

    def add(self, url, tags):
        packedUrl = struct.pack("s", url.encode('utf-8'))
        self._db.insert(dict(url=packedUrl, tags = tags))

    def check(self, url):
        packedUrl = struct.pack("s", url.encode('utf-8'))
        count = self._db.count(self._db.get_many, "urlidx", packedUrl)
        return count > 0
