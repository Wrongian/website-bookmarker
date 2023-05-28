import base64
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

KDF_ALGORITHM = hashes.SHA256()
KDF_LENGTH = 32
KDF_ITERATIONS = 120000

def encrypt_str(string, password):
    bytes_to_encrypt = string.encode("utf-8")
    return encrypt_bytes(bytes_to_encrypt,password)

def decrypt_str(encrypted_bytes,password,salt):
    str_bytes = decrypt_bytes(encrypted_bytes,password,salt)
    return str_bytes.decode("utf-8")
    
def encrypt_bytes(bytes_to_encrypt: bytes, password: str):
    # Derive a symmetric key using the passsword and a fresh random salt.
    salt = secrets.token_bytes(16)
    kdf = PBKDF2HMAC(
        algorithm=KDF_ALGORITHM, length=KDF_LENGTH, salt=salt,
        iterations=KDF_ITERATIONS)
    key = kdf.derive(password.encode("utf-8"))

    # Encrypt the message.
    f = Fernet(base64.urlsafe_b64encode(key))
    #ciphertext = f.encrypt(plaintext.encode("utf-8"))
    ciphertext = f.encrypt(bytes_to_encrypt)

    return ciphertext, salt

def decrypt_bytes(bytes_to_decrypt: bytes, password: str, salt: bytes):
    # Derive the symmetric key using the password and provided salt.
    kdf = PBKDF2HMAC(
        algorithm=KDF_ALGORITHM, length=KDF_LENGTH, salt=salt,
        iterations=KDF_ITERATIONS)
    key = kdf.derive(password.encode("utf-8"))

    # Decrypt the message
    f = Fernet(base64.urlsafe_b64encode(key))
    decrypted_bytes = f.decrypt(bytes_to_decrypt)

    #return plaintext.decode("utf-8")
    return decrypted_bytes

"""
def main():
    FILE_PATH = "life.txt"
    password = "aStrongPassword"
    message = "a secret message"

    encrypted, salt = encrypt(message, password)
    write_file(encrypted,FILE_PATH)
    text = read_file(FILE_PATH)
    decrypted = decrypt(text, password, salt)

    print(f"message: {message}")
    print(f"encrypted: {encrypted}")
    print(f"decrypted: {decrypted}")

def write_file(text,path):
    with open(path,"wb") as file:
        file.write(text)

def read_file(path):
    with open(path, "rb") as file:
        return file.read()
""" 