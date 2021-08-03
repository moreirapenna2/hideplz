#!/usr/bin/env python

#this program encrypts and decrypts a entire file, in any extension or size, based on a user given password

import os, io, struct
import random
import time
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

def decrypt(key, filename, chunk_size=24*1024):
    output_filename = os.path.splitext(filename)[0]
    with open(filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)
        with open(output_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunk_size)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(origsize)
 
 
def encrypt(key, filename, chunk_size=64*1024):
    output_filename = filename + '.encrypted'
    iv = os.urandom(16)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(filename)
    with open(filename, 'rb') as inputfile:
        with open(output_filename, 'wb') as outputfile:
            outputfile.write(struct.pack('<Q', filesize))
            outputfile.write(iv)
            while True:
                chunk = inputfile.read(chunk_size)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += bytes((16 - len(chunk) % 16))
                outputfile.write(encryptor.encrypt(chunk))

def getKey(password):
    password = password.encode('utf-8')
    hasher = SHA256.new(password)
    return hasher.digest()

def Main():
    choice = input("Would you like to (E)ncrypt or (D)ecrypt?\n> ")
    if choice == 'E' or choice == 'e':
        filename = input("File to encrypt:\n> ")
        password = input("Password:\n> ")
        encrypt(getKey(password), filename)
        print("Done")
    elif choice == 'D' or choice == 'd':
        filename = input("File to decrypt:\n> ")
        password = input("Password:\n> ")
        decrypt(getKey(password), filename)
        print("Done")
    else:
        print("Invalid option!")


if __name__ == '__main__':
    Main()
