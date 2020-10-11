import string
import socket
import time

original_msg = """
HELLO FIELD AGENT!
COMMANDS:
    SEND-SECRET-DATA
    GET-SECRET-DATA
    GOODBYE
    """
not_understand = "I don't understand you\n"
get_data = "GET-SECRET-DATA"


def process_message(conn):
    mapping = {j: '?'*26 for j in range(26)}
    counter = 0
    print("breaking the ENIGMA... please wait...")
    for i in range(26):
        resp = conn.recv(1024).decode()
        if resp == not_understand:
            resp = conn.recv(1024).decode()

        for char, original_char in zip(resp, original_msg):
            if char in string.ascii_uppercase:
                char_idx = string.ascii_uppercase.index(original_char)
                mapping[counter % 26] = "{}{}{}".format(mapping[counter % 26][:char_idx], char,
                                                        mapping[counter % 26][char_idx + 1:])
                counter += 1

        if i == 25:
            continue

        conn.send(b'\n')
    return mapping


def request_data(conn, mappings):
    counter = 0
    encrypted_req = ''
    for char in get_data:
        if char not in string.ascii_uppercase:
            encrypted_req += char
            continue

        encrypted_req += mappings[counter % 26][string.ascii_uppercase.find(char)]
        counter += 1
    encrypted_req += '\n'
    conn.send(encrypted_req.encode())
    encrypted_data = conn.recv(1024).decode()
    return encrypted_data, counter


def decrypt(encrypted, mappings, counter):
    decrypted = ''
    for char in encrypted:
        if char not in string.ascii_uppercase:
            decrypted += char
            continue
        decrypted += string.ascii_uppercase[mappings[counter % 26].find(char)]
        counter += 1
    return decrypted


if __name__ == '__main__':
    start_time = time.time()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('18.156.68.123', 80))
        s.recv(64)
        m = process_message(s)
        e, c = request_data(s, m)
        flag = decrypt(e, m, c)

    print("The flag is:", flag)
    print("Total time:", time.time() - start_time, "seconds.")  # ~ 4 secs
