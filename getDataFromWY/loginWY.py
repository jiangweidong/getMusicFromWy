import json
from getDataFromWY import encryptForWy


class loginWY(object):
    def __init__(self):
        self.modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.nonce = '0CoJUm6Qyw8W8jud'
        self.pub_key = '010001'
        self.enc = encryptForWy.encryptForWy()

    def loginwy(self, username, password):
        text = {
            'username': username,
            'password': password,
            'rememberLogin': 'true',
        }
        text = json.dumps(text)
        secKey = self.enc.createSecretKey()
        encText = self.enc.aes_encrypt(self.enc.aes_encrypt(text, self.nonce), secKey)
        encSecKey = self.enc.rsaEncrypt(secKey, self.pub_key, self.modulus)
        data = {
            'params':encText,
            'encSecKey': encSecKey
        }
        return data
        pass





