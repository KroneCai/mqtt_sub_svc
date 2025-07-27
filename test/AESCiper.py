from Crypto.Cipher import AES

class AESCiper:
    def __init__(self, key, iv):
        # 确保key和iv是bytes类型
        if isinstance(key, str):
            key = key.encode('utf-8')
        if isinstance(iv, str):
            iv = iv.encode('utf-8')
        self.key = key
        self.iv = iv

    @staticmethod
    def zero_pad(data, block_size):
        # 如果输入是字符串，先转换为bytes
        if isinstance(data, str):
            data = data.encode('utf-8')
        padding_length = block_size - len(data) % block_size
        # 返回bytes类型数据
        return data + b'\x00' * padding_length

    @staticmethod
    def unzero_pad(data):
        # 移除末尾的\x00字节
        return data.rstrip(b'\x00')


    def encrypt(self, data):
        # 确保输入是bytes
        if isinstance(data, str):
            data = data.encode('utf-8')
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        padded_data = self.zero_pad(data, AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)
        return encrypted_data

    def decrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        try:
            decrypted_data = self.unzero_pad(cipher.decrypt(data))
            return decrypted_data.decode('utf-8')  # 解密后转换为字符串
        except:
            return None
