import socket
import time
from Crypto.Cipher import ARC4
from itertools import product


def get_perms():
    with open('dictionary.txt', 'r') as d:
        words_len = dict()
        for w in d.read().split('\n'):
            if len(w) not in words_len.keys():
                words_len[len(w)] = [w]
                continue
            words_len[len(w)].append(w)
    with open('packets.txt', 'r') as p:
        options = list()
        for packet in p.read().split('\n'):
            options.append((words_len[len(bytes.fromhex(packet)) - 1]))
    poss_perm = list()
    for o in product(*options):
        poss_perm.append(o)
    return poss_perm


perms = get_perms()
start_time = time.time()

# the correct sequence is in perms[37] 
for i in range(0, len(perms)):
    attempt_time = time.time()
    with socket.socket() as conn:
        conn.connect(('3.126.154.76', 80))
        key = conn.recv(128).decode()
        print(key, end="")
        key = (key[key.find(':') + 2: -1]).encode()  # csa-mitm-key
        cipher = ARC4.new(key)
        message = conn.recv(128)
        print(cipher.decrypt(message).decode(), end="")

        
        for j in range(10):
            word = perms[i][j] + '\n'
            print(word, end='')
            enc_word = cipher.encrypt(word.encode())
            conn.send(enc_word)
        print("please wait...")
        resp = conn.recv(128)
        flag = cipher.decrypt(resp).decode()
        print(flag)

        print("----------------------------------")
        print("Total attempts", i + 1)
        print("Time for this attempt:", time.time() - attempt_time, "seconds")
        print("Total time:", round(time.time() - start_time), "seconds.")
        print("----------------------------------\n")
        if 'CSA' in flag:
            break
