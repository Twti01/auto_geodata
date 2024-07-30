import secrets


def key_list():

    def gen_api_keys(number, key_len=16):
        keys = []
        for i in range(number):
            key = secrets.token_hex(key_len)  
            keys.append(key)
        return keys

    keys_list = gen_api_keys(15)

    return keys_list