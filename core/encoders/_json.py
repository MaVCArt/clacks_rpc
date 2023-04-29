import json
from ..rpc_marshaller import ClacksRPCDecoder, ClacksRPCEncoder


# ----------------------------------------------------------------------------------------------------------------------
class ClacksRPCJsonDecoder(ClacksRPCDecoder):

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def viable(cls, type_key: str):
        return type_key == 'json'

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def decode(cls, value: bytes):
        return json.loads(str(value.decode('utf-8')))


# ----------------------------------------------------------------------------------------------------------------------
class ClacksRPCJsonEncoder(ClacksRPCEncoder):

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def viable(cls, value: object):
        try:
            _ = json.dumps(value)
            return True
        except:
            return False

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def encode(cls, value: dict):
        return 'json', bytes(json.dumps(value), 'utf-8')
