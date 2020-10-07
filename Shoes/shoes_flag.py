import socket
from zlib import crc32
from struct import pack


def get_crc32(msg):
    return pack(">I", crc32(msg) % 2 ** 32)


def xor(long, short):
    result = b''
    for j in range(1, len(short)):
        result += bytes([long[j + 1] ^ short[j]])
    return result


FIRST_PACKET = bytes.fromhex('5a01fedd749c2e')
FIRST_RESP_PACKET = bytes.fromhex('5afe67a6f193f4769864')
SECOND_PACKET = bytes.fromhex('5a67e5a2d249b59015')
THIRD_PACKET = bytes.fromhex("5a010001c0a8ad0a005074f2be19")
host, port = "52.28.255.56", 1080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    # --------------------------------------------- FIRST ---------------------------------------------
    print("\nSending first request:", FIRST_PACKET.hex())
    s.send(FIRST_PACKET)
    first_response = s.recv(32)
    print("First response from the server:", first_response.hex())
    print("--")

    # --------------------------------------------- SECOND ---------------------------------------------
    second_packet = bytes.fromhex('5a')
    key = xor(FIRST_RESP_PACKET[:-4], SECOND_PACKET[:-4])
    key = b'0' + key
    print("First response without checksum:", first_response[:-4].hex())
    second_packet += xor(first_response[:-4], key)
    print("Second request (after xor):", second_packet.hex())
    second_packet += get_crc32(second_packet)
    print("Sending second Request:", second_packet.hex())
    s.send(second_packet)
    print('--')

    # --------------------------------------------- THIRD ---------------------------------------------
    # file moved from 192.168.173.10 to 192.168.173.20
    third_packet = bytes([20 if byte == 10 else byte for byte in THIRD_PACKET[:-4]])
    third_packet += get_crc32(third_packet)
    print("Sending third request:", third_packet.hex())
    s.send(third_packet)
    print("Response from the server for the third request:\t", s.recv(32).hex())

    # --------------------------------------------- HTTP ---------------------------------------------
    request = b"GET /Flag.jpg HTTP/1.1\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
              b"(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36\r\nHost: www.tutorialspoint.com\r\n" \
              b"Accept-Language:en-us\r\nConnection: Keep-Alive\r\n\r\n"
    print("--\nSending HTTP request please wait...")
    s.send(request)
    print(s.recv(290).decode())  # until \r\n\r\n

    # --------------------------------------------- FLAG ---------------------------------------------
    print("Getting the flag file...")
    data = s.recv(4096)
    while len(data) < 80590:  # Content-Length: 80590
        data += s.recv(4096)
    with open('Flag.jpg', 'wb') as flag:
        flag.write(data)
    print("The flag is in the file Flag.jpg")
