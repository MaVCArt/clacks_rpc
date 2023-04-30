import weakref


# -- for the object cache we use a weak value dict, which ensures that any items we store are not kept alive by this
# -- cache. This means the object cache will discard any items whose valued have been garbage collected.
# -- It is worth noting that this may lead to unexpected behaviour. It is therefore possible to store something as a
# -- strong reference.
__WEAK_OBJECT_CACHE = weakref.WeakValueDictionary()


# ----------------------------------------------------------------------------------------------------------------------
def store_object(obj: object, guid: str):
    global __WEAK_OBJECT_CACHE
    __WEAK_OBJECT_CACHE[guid] = obj


# ----------------------------------------------------------------------------------------------------------------------
def retrieve_object(guid: str):
    # -- assume the object is in the weak cache
    if guid in __WEAK_OBJECT_CACHE:
        result = __WEAK_OBJECT_CACHE[guid]
        if result is None:
            raise ValueError(f'Object with guid {guid} may have been garbage collected!')
        return __WEAK_OBJECT_CACHE[guid]
    # -- otherwise, raise a key error.
    raise KeyError(f'No object could be found with guid {guid} in the cache!')
