# -*- coding: utf-8 -*-
from CodernityDB.database import Database
from CodernityDB.hash_index import HashIndex

class Cache():
    def __init__(self):
        db = Database('db')
        if db.exists():
            db.open()
        else:
            db.create()
            index = UrlIndex(db.path, 'urlidx')
            db.add_index(index)
        self._db = db

    def get(self):
        records = self._db.all("urlidx", with_doc=True)
        return [{'url': r["doc"]["url"], 'tags': r["doc"]["tags"], 'blocked': r["doc"]["blocked"] if "blocked" in r["doc"] else '?'} for r in records]

    def add(self, url, tags, blocked):
        packedUrl = url.encode('utf-8')
        self._db.insert(dict(url=packedUrl, tags = tags, blocked = blocked))

    def check(self, url):
        packedUrl = url.encode('utf-8')
        result = {"Cached": False, "Blocked": False }
        for curr in self._db.get_many("urlidx", packedUrl, with_doc=True):
            result["Cached"] = True
            result["Blocked"] = curr["doc"]["blocked"]
        return result
        #count = self._db.count(self._db.get_many, "urlidx", packedUrl)
        #return count > 0

class UrlIndex(HashIndex):
    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = '32s'
        super(UrlIndex, self).__init__(*args, **kwargs)

    def make_key_value(self, data):
        a_val = data.get("url")
        if a_val is not None:
            return md5(a_val).hexdigest(), None

    def make_key(self, key):
        return md5(key).hexdigest()