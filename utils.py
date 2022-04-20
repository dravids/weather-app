from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode


def getBytesFromString(string: str) -> bytes:
    return string.encode('utf-8')


def getStringFromBytes(byte: bytes) -> str:
    return byte.decode('utf-8')


def getCrypt(secret_key: str) -> any:
    key = getBytesFromString(secret_key)
    cipher = AES.new(b64decode(key), AES.MODE_ECB)
    return cipher


def encrypt(secret_key: str, plain_text: str) -> str:
    cipher = getCrypt(secret_key)
    plain_text_padded = pad(getBytesFromString(plain_text), AES.block_size)
    cipher_enc = cipher.encrypt(plain_text_padded)
    encrypted_encoded = b64encode(cipher_enc)
    return encrypted_encoded


def decrypt(secret_key: str, encrypted_text: str) -> str:
    cipher = getCrypt(secret_key)
    encrypted_text_bytes = getBytesFromString(encrypted_text)
    decoded = b64decode(encrypted_text_bytes)
    decrypted = cipher.decrypt(decoded)
    decrypted_unpadded = unpad(decrypted, AES.block_size)
    return decrypted_unpadded


def getResponseHeaders() -> dict:
    return dict({
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Credentials': '*'
    })

## just a utility function for testing
def retry(times):
    """
    Retry Decorator
    Retries the wrapped function/method `times` times if the exceptions listed
    in ``exceptions`` are thrown
    :param times: The number of times to repeat the wrapped function/method
    :type times: Int
    :param Exceptions: Lists of exceptions that trigger a retry attempt
    :type Exceptions: Tuple of Exceptions
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    print(f"Attempt: {attempt}")
                    return func(*args, **kwargs)
                except Exception as e:
                    print(e)
                else:
                    break
            else:
                print(f"all {times} attempts failed")
            return func(*args, **kwargs)
        return wrapper
    return decorator


