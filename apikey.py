import secrets, json, os

def gen_api_keys(number, key_len=16):
    keys = []
    for i in range(number):
        key = secrets.token_hex(key_len)  
        keys.append(key)
    return keys

def save_keys(keys_list):
    with open("api-keys.json", "w") as f:
        json.dump(keys_list, f)

def load_keys():
    if os.path.exists("api-keys.json"):
        with open("api-keys.json", "r")as f:
            keys_list = json.load(f)
    else:
        keys_list =  gen_api_keys(15)
        save_keys(keys_list)

    return keys_list


keys_list = load_keys()

if __name__ == "__main__": 
    print(keys_list)
