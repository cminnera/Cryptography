# Clare Minnerath
# week 2 assignment
# implementation of AES encryption/decryption in CBC & CTR modes

from Crypto.Cipher import AES
import os

def random_IV():
    print(os.urandom(16))

def random_key():
    return os.urandom(32)

def bxor(b1, b2): # use xor for bytes
    result = b""
    for b1, b2 in zip(b1, b2):
        result += bytes([b1 ^ b2])
    return result

def CBC_encryption(key, msg):
    
    pass

def CTR_encryption(key, msg):
    # encrypt message
    pass

def CBC_decryption(key, ct):
    ct = bytes.fromhex(ct)
    key = bytes.fromhex(key)
    iv = ct[0:16] 
    ct = ct[16:]
    blocks = [ct[i:i+16] for i in range(0, len(ct), 16)] 
    blocks.reverse()
    cipher = AES.new(key, AES.MODE_ECB)
    msg = []
    plaintext = ""
    for i in range(len(blocks)-1):
        block_AES = cipher.decrypt(blocks[i])
        msg.append(bxor(block_AES, blocks[i+1]))
        if i == 0:
            pad = msg[i][15] # final byte
            msg[i] = msg[i][i:len(msg[i])-pad]
    block_AES = cipher.decrypt(blocks[len(blocks)-1])
    msg.append(bxor(block_AES, iv))
    msg.reverse()
    for m in msg:
        plaintext += m.decode()
    return plaintext
        

def CTR_decryption(key, ct):
    ct = bytes.fromhex(ct)
    key = bytes.fromhex(key)
    iv = ct[0:16]
    cipher = AES.new(key, AES.MODE_ECB)
    ct = ct[16:]
    i = 0
    plaintext = ""
    while i < len(ct):
        prf = cipher.encrypt(iv)
        if i + 16 <= len(ct):
            msg = bxor(prf, ct[i:i+16])
            i += 16
        else:
            msg = bxor(prf, ct[i:])
            i += len(msg)
        iv = int.from_bytes(iv, 'big')
        iv += 1
        iv = iv.to_bytes(16, 'big')
        # append decrypted plaintext
        plaintext += msg.decode()
    return plaintext

def main():

    # Home work test cases for decryption:
    CBC_keys = ["140b41b22a29beb4061bda66b6747e14", "140b41b22a29beb4061bda66b6747e14"]
    CBC_cipher_texts = ["4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81", "5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253"]

    CTR_keys = ["36f18357be4dbd77f050515c73fcf9f2", "36f18357be4dbd77f050515c73fcf9f2"]
    CTR_cipher_texts = ["69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329", "770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451"]

    print("Plain text Q1:", CBC_decryption(CBC_keys[0], CBC_cipher_texts[0]))
    print("Plain text Q2:", CBC_decryption(CBC_keys[1], CBC_cipher_texts[1]))
    print("Plain text Q3:", CTR_decryption(CTR_keys[0], CTR_cipher_texts[0]))
    print("Plain text Q4:", CTR_decryption(CTR_keys[1], CTR_cipher_texts[1]))

main()