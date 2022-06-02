# coding=utf-8

import json
from cryptography.fernet import Fernet


def encrypt_json(data, key=None):
    """
    加密json数据
    :param data: json数据
    :param key: 加密使用的key
    :return: 加密后的json数据, 加密使用的key
    """
    data = json.dumps(data)
    if key is None:
        key = Fernet.generate_key()
    f = Fernet(key)
    encrypted = f.encrypt(data.encode())
    return encrypted, key


def decrypt_json(data, key):
    """
    解密json数据
    :param data: 加密后的json数据
    :param key: 加密使用的key
    :return: 解密后的json数据
    """
    f = Fernet(key)
    decrypted = f.decrypt(data)
    return json.loads(decrypted.decode())


if __name__ == '__main__':
    # test unit
    test_data = {'name': 'ct', 'age': 18}
    encrypted_data, k = encrypt_json(test_data)
    print(encrypted_data)
    print(k)
    decrypted_data = decrypt_json(encrypted_data, k)
    print(decrypted_data)
