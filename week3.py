# Clare Minnerath
# Week 3 Cryptography assignment
# hash video authentication

from Crypto.Hash import SHA256
import binascii

def create_test_file():
    rawhex1 = b'\x11'*1024
    rawhex2 = b'\x22'*1024
    rawhex3 = b'\x33'*1024
    rawhex4 = b'\x44'*773
    e1 = open('b1','wb')
    e2 = open('b2','wb')
    e3 = open('b3','wb')
    e4 = open('b4','wb')
    t1 = open('test11223344','wb')
    e1.write(rawhex1)
    e2.write(rawhex2)
    e3.write(rawhex3)
    e4.write(rawhex4)
    t1.write(rawhex1+rawhex2+rawhex3+rawhex4)
    t1.close()
    e1.close()
    e2.close()
    e3.close()
    e4.close()

def import_data_file(file_name):
    with open(file_name, 'rb') as f:
        content = f.read()
    return content

def hex_to_blocks(hex_string):
    blocks = []
    for i in range(0, len(hex_string), 1024):
        blocks.append(hex_string[i:i+1024])
    return blocks

def compute_h_0(blocks):
    blocks.reverse()
    for i in range(len(blocks)-1):
        h = SHA256.new()
        h.update(blocks[i])
        blocks[i+1] += h.digest()
    h = SHA256.new()
    h.update(blocks[len(blocks)-1])
    return h.hexdigest()


def main():
    file_hex = import_data_file("6.1.intro.mp4_download")
    # file_hex = import_data_file("6.2.birthday.mp4_download")
    # file_hex = import_data_file("test11223344") 
    blocks = hex_to_blocks(file_hex)
    print("h_0 = ", compute_h_0(blocks))

main()