import traceback
from typing import Type
from clacks_rpc.core.proxy_object import ClacksRPCObjectProxy
from clacks.core.marshaller.marshallers.simple import SimplePackageMarshaller, decode_package, encode_package


# ----------------------------------------------------------------------------------------------------------------------
class ClacksRPCEncoder(object):

    PRIORITY = 0

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def viable(cls, value: object) -> bool:
        raise NotImplementedError

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def encode(cls, value: object) -> tuple[str, bytes]:
        raise NotImplementedError


# ----------------------------------------------------------------------------------------------------------------------
class ClacksRPCDecoder(object):

    PRIORITY = 0

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def viable(cls, type_key: str) -> bool:
        raise NotImplementedError

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def decode(cls, value: bytes) -> object:
        raise NotImplementedError


# ----------------------------------------------------------------------------------------------------------------------
def _collect_decoders() -> list[Type[ClacksRPCDecoder]]:
    from . import encoders
    result = list()
    for cls in dir(encoders):
        cls = encoders.__dict__[cls]
        if not isinstance(cls, type):
            continue
        if not issubclass(cls, ClacksRPCDecoder):
            continue
        result.append(cls)
    return sorted(result, key=lambda x: x.PRIORITY, reverse=True)


DECODERS = list()

# ----------------------------------------------------------------------------------------------------------------------
def collect_decoders() -> list[Type[ClacksRPCDecoder]]:
    global DECODERS
    if DECODERS:
        return DECODERS
    DECODERS = _collect_decoders()
    return DECODERS


# ----------------------------------------------------------------------------------------------------------------------
def _collect_encoders() -> list[Type[ClacksRPCEncoder]]:
    from . import encoders
    result = list()
    for cls in dir(encoders):
        cls = encoders.__dict__[cls]
        if not isinstance(cls, type):
            continue
        if not issubclass(cls, ClacksRPCEncoder):
            continue
        result.append(cls)
    return sorted(result, key=lambda x: x.PRIORITY, reverse=True)


ENCODERS = list()

# ----------------------------------------------------------------------------------------------------------------------
def collect_encoders() -> list[Type[ClacksRPCEncoder]]:
    global ENCODERS
    if ENCODERS:
        return ENCODERS
    ENCODERS = _collect_encoders()
    return ENCODERS


# ----------------------------------------------------------------------------------------------------------------------
def _encode(value: object) -> tuple[str, bytes]:
    encoders = collect_encoders()
    for encoder in encoders:
        if not encoder.viable(value):
            continue
        return encoder.encode(value)
    raise TypeError(f'No viable encoder available for value {value}')


# ----------------------------------------------------------------------------------------------------------------------
def _decode(type_key: str, value: bytes) -> object:
    encoders = collect_decoders()
    for decoder in encoders:
        if not decoder.viable(type_key):
            continue
        return decoder.decode(value)
    raise TypeError(f'No viable decoder available for value {value}')


# ----------------------------------------------------------------------------------------------------------------------
class ClacksRPCMarshaller(SimplePackageMarshaller):

    # ------------------------------------------------------------------------------------------------------------------
    def _encode_package(self, transaction_id, package):
        try:
            return super(ClacksRPCMarshaller, self)._encode_package(transaction_id, package)
        except:
            pass

        data = package.payload
        result = ''

        for key, value in data.items():
            type_key, value = _encode(value)

            hex_value = value.hex()
            encoded_value = f'{type_key}/{key}/{hex_value}'

            result += f'{encoded_value}\n'

        return bytes(result, 'utf-8')

    # ------------------------------------------------------------------------------------------------------------------
    def _decode_package(self, transaction_id, header_data, payload):
        try:
            return super(ClacksRPCMarshaller, self)._decode_package(transaction_id, header_data, payload)
        except:
            pass

        data = str(payload.decode('utf-8'))

        result = dict()

        for line in data.splitlines():
            line = line.strip('\n')
            if not line:
                continue

            value_type, key, value = line.split('/')
            value = bytearray.fromhex(value)

            value = _decode(value_type, value)

            if isinstance(value, ClacksRPCObjectProxy):
                value.server = self.handler.server

            result[key] = value

        return result
