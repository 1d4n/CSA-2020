from stegano import lsb
import base64

encoded_flag = lsb.reveal('spy.png')
first_decode = base64.b64decode(encoded_flag.encode())
print("The flag is:", base64.b64decode(first_decode).decode())
