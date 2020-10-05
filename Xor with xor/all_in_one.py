#!usr/bin/env python3
import os
import re
import gzip
import zipfile
import shutil
import speech_recognition as sr


def xor(data, key):
    return bytearray(((data[i] ^ key[i % len(key)]) for i in range(0, len(data))))


def xor_and_unzip():
    os.chdir(FOLDER)
    with open('xor-with-xor.bin', 'rb') as r:
        enc = r.read()
    dec = xor(enc, b'xor')
    with open(DAT_FOLDER + 'xor.zip', 'wb') as w:
        w.write(dec)

    with zipfile.ZipFile(DAT_FOLDER + 'xor.zip', 'r') as z:
        z.extractall(FOLDER + DAT_FOLDER)


def combine():
    os.chdir(FOLDER + DAT_FOLDER)
    file_list = os.listdir()
    for name in file_list:
        new_name = re.sub('[a-zA-Z$\[\]. _]', '', name)
        os.rename(name, new_name)

    with open(f'{FOLDER}' + r'\flag.gz', 'wb') as w:
        for i in range(1000):
            with open(str(i), 'rb') as r:
                w.write(r.read())
    with gzip.open(f'{FOLDER}' + r'\flag.gz', 'r') as f_in, open(f'{FOLDER}' + r'\flag.wav', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


def flag():
    os.chdir(FOLDER)
    audio_file = 'flag.wav'
    r = sr.Recognizer()
    print("listening...")
    with sr.AudioFile(audio_file) as audio:
        audio_data = r.record(audio)
        text = r.recognize_google(audio_data)
    return text


if __name__ == '__main__':
    FOLDER = fr'{input("Please enter the folder path of the .bin file:")}'
    DAT_FOLDER = r'/DAT/'

    xor_and_unzip()
    combine()
    print(flag())
