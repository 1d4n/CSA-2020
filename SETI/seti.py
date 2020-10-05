import json
import random

with open('first_signal.txt', 'r') as first_file:
    first_message = json.load(first_file)

with open('second_signal.txt', 'r') as second_file:
    second_message = json.load(second_file)

first_message_list = []
for i in range(len(first_message)):
    first_message_list.append([])
    for j in range(len(first_message[i])):
        first_message_list[i].append(''.join(map(str, first_message[i][j])))


second_message_list = []
for i in range(len(second_message)):
    second_message_list.append([])
    for j in range(len(second_message[i])):
        second_message_list[i].append(''.join(map(str, second_message[i][j])))

###################################
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


#############################################################
first_options = []
for i in range(len(first_message_list)):
    first_options.append([])
    for j in range(32, 126):
        if is_char_fit(bin(j)[2:].zfill(8), first_message_list[i]):
            if chr(j) not in f"/[]^*()=;><+":
                first_options[i].append(chr(j))

print("options for first message:", first_options)

#############################################################
second_options = []
for i in range(len(second_message_list)):
    second_options.append([])
    for j in range(32, 126):
        if is_char_fit(bin(j)[2:].zfill(8), second_message_list[i]):
            if chr(j) not in f"/[]^*()=;><+":
                second_options[i].append(chr(j))

print("\noptions for second message:", second_options)

#############################################################
#       Little People, Why Can't We All Just Get Along?     #
#############################################################
flag = '\nCSA{'
for i in range(4, len(second_options) - 1):
    flag += random.choice(second_options[i])
flag += '}'
print(flag)
