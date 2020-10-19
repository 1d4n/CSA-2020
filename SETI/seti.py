import json

with open('first_signal.txt', 'r') as first_file:
    first_signal = json.load(first_file)
with open('second_signal.txt', 'r') as second_file:
    second_signal = json.load(second_file)

first_message = [[''.join(map(str, i)) for i in sub_list] for sub_list in first_signal]
second_message = [[''.join(map(str, i)) for i in sub_list] for sub_list in second_signal]


def is_fit(byte, bits):
    b = 0
    for bit in bits:
        found = False
        while b < len(byte):
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


first_options = [[chr(j) for j in range(32, 126) if chr(j) not in f"/[]^*()=;><+" and is_char_fit(bin(j)[2:].zfill(8), char)] for char in first_message]
print("Options for first message:\n", first_options)

second_options = [[chr(j) for j in range(32, 126) if chr(j) not in f"/[]^*()=;><+" and is_char_fit(bin(j)[2:].zfill(8), char)] for char in second_message]
print("\nOptions for first message:\n", second_options)

print("\nFLAG: CSA{L1ttL3_P30pL3,_WhY_K4'Nt_w3_4LL_Ju5t_93t_4L0N9?}")
#############################################################
#       Little People, Why Can't We All Just Get Along?     #
#############################################################
