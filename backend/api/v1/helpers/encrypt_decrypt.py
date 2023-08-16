from cryptography.fernet import Fernet
from core.config import Config
import base64


AES_KEY = Config.AES_KEY


# 设置密钥
# 计算剩余部分长度
remaining_length = 32 - len(AES_KEY)
# 将AES_KEY转换为字节串
AES_KEY = AES_KEY.encode()
# 补齐剩余部分
SECRET_KEY_AES = AES_KEY + b' ' * remaining_length

# 将密钥转换为URL-safe的base64编码
SECRET_KEY_AES = base64.urlsafe_b64encode(SECRET_KEY_AES)

# 将密钥转换为字符串格式
SECRET_KEY_AES = SECRET_KEY_AES.decode()


# 加密和解密函数
def encrypt_text(text: str) -> bytes:
    cipher_suite = Fernet(SECRET_KEY_AES)
    encrypted_text = cipher_suite.encrypt(text.encode())
    return encrypted_text

def decrypt_text(encrypted_text: bytes) -> str:
    cipher_suite = Fernet(SECRET_KEY_AES)
    decrypted_text = cipher_suite.decrypt(encrypted_text)
    return decrypted_text.decode()