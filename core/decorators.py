# ----------------------------------------------------------------------------------------------------------------------
def rpc_hidden(fn):
    """
    This is a Clacks-RPC specific decorator that lets our server know that methods decorated with it are not to be
    accessible through the __getattr__ method.
    """
    if not hasattr(fn, 'extra_attrs'):
        fn.extra_attrs = dict()
    fn.extra_attrs['rpc_hidden'] = True
    return fn
