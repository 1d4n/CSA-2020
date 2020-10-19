import socket
import time
from Crypto.Cipher import ARC4
from itertools import product, groupby


def sequence_perms():
    with open('dictionary.txt', 'r') as d:
        words = [word for word in d.read().split('\n')]
    with open('packets.txt', 'r') as p:
        packets_len = [(len(packet) // 2 - 1) for packet in p.read().split('\n')]
    words.sort(key = len)
    words_len = {length: list(set(items)) for length, items in groupby(words, key=len) if length in packets_len}
    possible_words = [words_len[packet_len] for packet_len in packets_len]
    print(possible_words)
    return [x for x in product(*possible_words)]


perms = sequence_perms()
start_time = time.time()
# The correct sequence is: 'particularly administration a as I environmental about across ability according'

for i in range(len(perms)):
    with socket.socket() as conn:
        print(f"--------------- {i + 1} ----------------")
        print("Total time:", round(time.time() - start_time), "seconds.")
        conn.connect(('3.126.154.76', 80))
        
        msg = conn.recv(64).decode()
        print(msg[:-1])  # Welcome! your RC4 key is: csa-mitm-key
        key = (msg[msg.find('csa'):-1]).encode()  # csa-mitm-key
        cipher = ARC4.new(key)
        print(cipher.decrypt(conn.recv(32)).decode(), end="")  # Hi! what's the secret sequence?
        
        sequence = ' '.join(perms[i])
        print(sequence)
        conn.send(cipher.encrypt(sequence.encode()))
        print("please wait...")
        
        flag = cipher.decrypt(conn.recv(128))
        if b'CSA' in flag:
            print("The flag is:", flag.decode())
            break
        else:
            print("Wrong sequence - reconnecting...\n")
