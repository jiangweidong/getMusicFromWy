import os

from crypto.Cipher import AES
import base64
from random import Random
from binascii import b2a_hex, a2b_hex
import binascii
import struct


class encryptForWy(object):
    def __init__(self):
        pass

    # # aes加密
    # def aesEncrypt(self, text, secKey):
    #     cryptor = AES.new(secKey, 2, secKey)
    #     text = text.encode("utf-8")
    #     # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
    #     length = 16
    #     count = len(text)
    #     add = length - (count % length)
    #     text = text + (b'\0' * add)
    #     ciphertext = cryptor.encrypt(text)
    #     # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
    #     # 所以这里统一把加密后的字符串转化为16进制字符串
    #     return b2a_hex(ciphertext).decode("ASCII")
    #     # return ciphertext

    def aes_encrypt(self, text, secKey):
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(secKey, 2, '0102030405060708')
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.b64encode(ciphertext)
        return str(ciphertext, encoding="utf-8")

    # 创建指定长度随机字符串
    def createSecretKey(self, strsize=16):
        str = ''
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        length = len(chars) - 1
        random = Random()
        for i in range(strsize):
            str += chars[random.randint(0, length)]
        return str

    def create_secret_key(self, size=16):
        return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16]

    # rsa 加密
    def rsaEncrypt(self, text, pubKey, modulus):
        text = text[::-1]
        a = ''
        for i in list(text):
            a = a + (hex(ord(i))[2:])
        rs = int(a, 16) ** int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

