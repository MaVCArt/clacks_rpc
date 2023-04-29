object_cache = dict()

def store_object(obj, guid):
    global object_cache
    object_cache[guid] = obj


def retrieve_object(guid):
    return object_cache[guid]
