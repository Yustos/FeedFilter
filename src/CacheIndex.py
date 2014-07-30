from CodernityDB.hash_index import HashIndex

class UrlIndex(HashIndex):
    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = 's'
        super(UrlIndex, self).__init__(*args, **kwargs)

    def make_key_value(self, data):
        a_val = data.get("url")
        if a_val is not None:
            return a_val, None
        return None

    def make_key(self, key):
        return key