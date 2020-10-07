import json

with open('first_signal.txt', 'r') as first_file:
    first_message = json.load(first_file)
with open('second_signal.txt', 'r') as second_file:
    second_message = json.load(second_file)

for i in range(len(first_message)):
    first_message[i] = [''.join(map(str, first_message[i][j])) for j in range(len(first_message[i]))]
for i in range(len(second_message)):
    second_message[i] = [''.join(map(str, second_message[i][j])) for j in range(len(second_message[i]))]


def is_fit(byte, bits):
    b = 0
    for bit in bits:
        found = False
        while b < 8:
            if byte[b] == bit:
                b += 1
                found = True
                break
            b += 1
        if not found:
            return False
    return True


def is_char_fit(byte, bits_list):
    for bits in bits_list:
        if not is_fit(byte, bits):
            return False
    return True


first_options = dict()
for i in range(len(first_message)):
    first_options[i] = [chr(j) for j in range(32, 126)
                        if chr(j) not in f"/[]^*()=;><+" and is_char_fit(bin(j)[2:].zfill(8), first_message[i])]
print("options for first message:", first_options)

second_options = dict()
for i in range(len(second_message)):
    second_options[i] = [chr(j) for j in range(32, 126)
                         if chr(j) not in f"/[]^*()=;><+" and is_char_fit(bin(j)[2:].zfill(8), second_message[i])]
print("\noptions for second message:", second_options)
print("CSA{L1ttL3_P30pL3,_WhY_K4'Nt_w3_4LL_Ju5t_93t_4L0N9?}")
#############################################################
#       Little People, Why Can't We All Just Get Along?     #
#############################################################
