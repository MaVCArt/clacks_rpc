import weakref


# -- for the object cache we use a weak value dict, which ensures that any items we store are not kept alive by this
# -- cache. This means the object cache will discard any items whose valued have been garbage collected.
# -- It is worth noting that this may lead to unexpected behaviour. It is therefore possible to store something as a
# -- strong reference.
__OBJECT_CACHE = dict()


# ----------------------------------------------------------------------------------------------------------------------
def store_object(obj: object, guid: str):
    global __OBJECT_CACHE
    __OBJECT_CACHE[guid] = obj


# ----------------------------------------------------------------------------------------------------------------------
def retrieve_object(guid: str):
    # -- assume the object is in the weak cache
    if guid in __OBJECT_CACHE:
        return __OBJECT_CACHE[guid]
    # -- otherwise, raise a key error.
    raise KeyError(f'No object could be found with guid {guid} in the cache!')
