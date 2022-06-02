# coding=utf-8

import os
import logging
from PySide2.QtWidgets import QWidget
from cryptography.fernet import Fernet
from ct.encrypto import encrypt_json, decrypt_json


__CONFIG_DIR__ = '../config'
os.makedirs(__CONFIG_DIR__, exist_ok=True)
__ENCRYPT_KEYFILE__ = '../config/encrypt_key'
__DB_ENCRYPT_INFOFILE__ = '../config/dbinfo'


def _write_encrypt_key(key):

    # backup the original file
    if os.path.exists(__ENCRYPT_KEYFILE__):
        for i in range(1000000):
            if not os.path.exists(__ENCRYPT_KEYFILE__ + f'.bak{i}'):
                os.rename(__ENCRYPT_KEYFILE__, __ENCRYPT_KEYFILE__ + f'.bak{i}')
                logging.warning(f'backup the original key file to {__ENCRYPT_KEYFILE__ + f".bak{i}"}')
                break
        else:
            raise RuntimeError('Too many backup files: ' + os.path.realpath(__ENCRYPT_KEYFILE__))

    with open(__ENCRYPT_KEYFILE__, 'wb') as f:
        f.write(b'# please delete this file after confirming and set the environment variable ME_ENCRYPT_KEY\n')
        f.write(key)
    logging.warning(f'write the encrypt key to {os.path.realpath(__ENCRYPT_KEYFILE__)}')

    return key


def _read_encrypt_key():
    key = os.environ.get('ME_ENCRYPT_KEY', None)
    if key is not None:
        return key

    if not os.path.exists(__ENCRYPT_KEYFILE__):
        return None

    with open(__ENCRYPT_KEYFILE__, 'rb') as f:
        for line in f:
            line = line.strip()
            if line.startswith(b'#'):
                continue
            return line
    return None


class _DBConfigWidget(QWidget):
    def __init__(self, parent=None):
        if parent is None:
            super().__init__()
        else:
            super(_DBConfigWidget, self).__init__(parent)
        self.setFixedSize(300, 200)

    @staticmethod
    def _encrypt_connect_info(info):
        """
        加密数据库连接信息
        :param info: 数据库连接信息
        :return: (加密后的数据库连接信息, 加密使用的密钥)
        """
        key = _read_encrypt_key()
        if key is None:
            key = _write_encrypt_key(Fernet.generate_key())
        return encrypt_json(info, key)

    @staticmethod
    def save_db_config(**kwargs):
        """
        保存数据库连接信息
        :param kwargs: 数据库连接信息
        """
        encrypt_info, _ = _DBConfigWidget._encrypt_connect_info(kwargs)
        with open(__DB_ENCRYPT_INFOFILE__, 'wb') as f:
            f.write(encrypt_info)

    @staticmethod
    def load_db_config():
        key = _read_encrypt_key()
        if key is None:
            key = _write_encrypt_key(os.urandom(32))

        if not os.path.exists(__DB_ENCRYPT_INFOFILE__):
            return None

        with open(__DB_ENCRYPT_INFOFILE__, 'rb') as f:
            encrypt_info = f.read()
        try:
            config = decrypt_json(encrypt_info, key)
        except Exception:
            logging.error('decrypt database config failed')
            return None
        return config


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    w = _DBConfigWidget()
    w.show()
    sys.exit(app.exec_())
