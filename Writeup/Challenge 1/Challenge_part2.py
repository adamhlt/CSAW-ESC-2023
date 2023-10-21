import hashlib
import itertools
import string
import time

def generate_keypass_hash_list(count=1024):
    hashs = {}
    s = time.time()
    for keypass in itertools.combinations_with_replacement("0123456789", 10):
        if len(hashs)>=count: break
        keypass_str     = str(''.join(keypass))
        hash_hex        = hashlib.sha1(keypass_str.encode('ascii', 'replace')).hexdigest()[:10]
        hashs[hash_hex] = keypass_str
    print(f"Generate {count} pincodes and hashes in {(time.time()-s)*1000:0.2f} ms !")
    return hashs

def try_collide(hashs):
    c = 0
    temp_speed = time.time()
    s = time.time()
    for i in range(30):
        for passcode in itertools.combinations_with_replacement(string.ascii_lowercase, i):
            passcode_str = "Barry" + str(''.join(passcode))
            hash_hex = hashlib.sha1(passcode_str.encode('ascii', 'replace')).hexdigest()[:10]
            if hash_hex in hashs:
                print(f'\033[0GCollide ! hash={hash_hex} pin_code={hashs[hash_hex]} username={passcode_str} it took {(time.time()-s):0.2f} s !')
                return
            
            if c==100000:
                print(f"\033[0G{100000/(time.time()-temp_speed):0.2f} it/s    ",end='',flush=True)
                temp_speed=time.time()
                c=0

            c += 1
            

    print("Nothing")

if __name__ =='__main__':
    hashs = generate_keypass_hash_list(2**16)
    try_collide(hashs)