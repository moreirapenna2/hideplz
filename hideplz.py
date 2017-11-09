#!/usr/bin/env python

#this program encrypts and decrypts a entire file, in any extension or size, based on a user given password

import os
import random
import time
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


def encrypt(key, filename):
    chunksize = 64*1024
    outputfile = "(encrypted)" + filename
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = ''

    for i in range(16):
        IV += chr(random.randint(0, 0xFF))

    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, 'rb') as infile:
        with open(outputfile, 'wb') as outfile:
            outfile.write(filesize)
            outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))
    os.remove(filename)


def decrypt(key, filename):
    chunksize = 64 * 1024
    outputfile = filename[11:]

    with open(filename, 'rb') as infile:
        filesize = long(infile.read(16))
        IV = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(outputfile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filesize)
    os.remove(filename)

def getKey(password):
    hasher = SHA256.new(password)
    return hasher.digest()

def Main():
    choice = raw_input("Would you like to (E)ncrypt or (D)ecrypt?\n> ")
    if choice == 'E' or choice == 'e':
        filename = raw_input("File to encrypt:\n> ")
        password = raw_input("Password:\n> ")
        encrypt(getKey(password), filename)
        print "Done"
    elif choice == 'D' or choice == 'd':
        filename = raw_input("File to decrypt:\n> ")
        password = raw_input("Password:\n> ")
        decrypt(getKey(password), filename)
        print "Done"
    else:
        print "Invalid option!"


if __name__ == '__main__':
    Main()
