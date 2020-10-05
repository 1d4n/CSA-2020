from zlib import crc32
from struct import pack
import time
import socket


def get_crc32(msg):
    return pack(">I", crc32(msg) % 2 ** 32)


def xor(long, short):
    result = b''
    for j in range(1, len(short)):
        result += bytes([long[j + 1] ^ short[j]])
    return result


original_first_packet = bytes.fromhex('5a01fedd749c2e')
original_first_response_packet = bytes.fromhex('5afe67a6f193f4769864')
original_second_packet = bytes.fromhex('5a67e5a2d249b59015')
original_third_packet = bytes.fromhex("5a010001c0a8ad0a005074f2be19")
host, port = "52.28.255.56", 1080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    start_time = time.time()
    # --------------------------------------------- FIRST ---------------------------------------------
    print("\nSending first request:" + 7 * "\t", original_first_packet.hex())
    s.send(original_first_packet)
    first_response = s.recv(32)
    print("First response from the server:" + 5 * "\t", first_response.hex())
    print("--")

    # --------------------------------------------- SECOND ---------------------------------------------
    second_packet = bytes.fromhex('5a')
    key = xor(original_first_response_packet[:-4], original_second_packet[:-4])
    key = b'0' + key
    print("First response without checksum:" + 4 * "\t", first_response[:-4].hex())
    second_packet += xor(first_response[:-4], key)
    print("Second request (after xor):" + 6 * "\t", second_packet.hex())
    second_packet += get_crc32(second_packet)
    print("Sending second Request:" + 7 * "\t", second_packet.hex())
    s.send(second_packet)

    # --------------------------------------------- THIRD ---------------------------------------------
    print('--')
    third_packet = b''
    # file moved from 192.168.173.10 to 192.168.173.20
    for byte in original_third_packet[:-4]:
        if byte == 10:
            byte = 20
        third_packet += bytes([byte])
        print(byte, end=" ")
    third_packet += get_crc32(third_packet)
    print("\nSending third request:" + 7 * "\t", third_packet.hex())
    s.send(third_packet)
    print("Response from the server for the third request:\t", s.recv(32).hex())

    # --------------------------------------------- HTTP ---------------------------------------------
    request = b"""GET /Flag.jpg HTTP/1.1\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36\r\nHost: www.tutorialspoint.com\r\nAccept-Language: en-us\r\nConnection: Keep-Alive\r\n\r\n"""
    print("--\nSending HTTP request please wait...")
    s.send(request)
    print(s.recv(290).decode())  # until \r\n\r\n

    # --------------------------------------------- FLAG ---------------------------------------------
    print("getting flag...")
    data = s.recv(4096)
    while len(data) < 80590:
        data += s.recv(4096)
    with open('Flag.jpg', 'wb') as flag:
        flag.write(data)
    print("The flag is in the file Flag.jpg")
    print("Total time:", time.time() - start_time, "seconds.")
