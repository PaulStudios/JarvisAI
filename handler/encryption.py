# pylint: disable=E0401
# skipcq
"""
Password Encryption Handler
"""

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .config import sec_config
from handler.logger import Logger

KDF_ALGORITHM = hashes.SHA256()
KDF_LENGTH = 32
KDF_ITERATIONS = 120000

priv = sec_config()

LOGGER: Logger = Logger("JarvisAI.encryptor")


def encrypt(plaintext: str, password: str = priv['pass']) -> bytes:
    """Encrypt the message"""
    salt = int(priv['salt']).to_bytes(5)
    kdf = PBKDF2HMAC(algorithm=KDF_ALGORITHM,
                     length=KDF_LENGTH,
                     salt=salt,
                     iterations=KDF_ITERATIONS)
    key = kdf.derive(password.encode("utf-8"))
    # Encrypt the message.
    f = Fernet(base64.urlsafe_b64encode(key))
    ciphertext = f.encrypt(plaintext.encode("utf-8"))
    LOGGER.info("Encrytion Completed")
    return ciphertext


def decrypt(
    ciphertext: bytes,
    password: str = priv['pass'],
    salt: bytes = int(priv['salt']).to_bytes(5)
) -> str:
    """Decrypt Message"""
    # Derive the symmetric key using the password and provided salt.
    kdf = PBKDF2HMAC(algorithm=KDF_ALGORITHM,
                     length=KDF_LENGTH,
                     salt=salt,
                     iterations=KDF_ITERATIONS)
    key = kdf.derive(password.encode("utf-8"))
    # Decrypt the message
    f = Fernet(base64.urlsafe_b64encode(key))
    plaintext = f.decrypt(ciphertext)
    LOGGER.info("Decryption Completed")
    return plaintext.decode("utf-8")
