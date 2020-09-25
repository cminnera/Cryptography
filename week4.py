# Clare Minnerath
# Week 4 Cryptography assignment
# CBC padding oracle attack on known vulnerable site crypto-class.appspot.com

import urllib.request as urlr
import urllib.error as urle
import urllib.parse as urlp
import sys

TARGET = 'http://crypto-class.appspot.com/po?er='
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):
    def query(self, q):
        target = TARGET + urlp.quote(q)    # Create query URL
        req = urlr.Request(target)         # Send HTTP request to server
        try:
            f = urlr.urlopen(req)          # Wait for response
        except urle.HTTPError as e:          
            # print("We got: %d" % e.code)       # Print response code
            if e.code == 404:
                return True # good padding
            else:
                return False # bad padding

    def bxor(self, b1, b2): # use xor for bytes
        result = b""
        for b1, b2 in zip(b1, b2):
            result += bytes([b1 ^ b2])
        return result

    # pad is out of range unless specified
    # code implementing padding Oracle attack
    def obtain_PT(self, ct, known_pad = 256):
        ct_b = bytes.fromhex(ct)
        pad = 1
        pt_b = b""
        while pad <= 16:
            # print("Hacking" + "."*pad)
            hex_pad = hex(pad)[2:]
            if len(hex_pad) == 1:
                hex_pad = "0" + hex_pad
            hex_pad = hex_pad * pad
            g = 0
            pt_b = bytes(1) + pt_b
            while g < 256:
                g_b = bytes([g]) + bytes(pad-1)
                g_b = self.bxor(g_b, pt_b)
                hex_pad_b = bytes.fromhex(hex_pad)
                xor1 = self.bxor(ct_b[-pad-16:-16], g_b)
                xor2 = self.bxor(xor1, hex_pad_b)
                xor2 = xor2.hex()
                xor2 = ct_b[:-pad-16].hex() + xor2 + ct_b[-16:].hex()
                if pad == known_pad and g == known_pad:
                    pt_b = g_b
                    break
                if self.query(xor2):
                    pt_b = g_b
                    break
                g += 1
            pad += 1
        return pt_b.decode()
    
    # breaks up CT into message blocks before running function to obtain PT
    def break_up_plaintext(self, pt, known_pad, num_blocks):
        offset = 32
        for i in range(num_blocks-1, -1, -1):
            if i != 0:
                print(self.obtain_PT(sys.argv[1][:-i*offset]), end ='')
            else:
                print(self.obtain_PT(sys.argv[1], known_pad), end ='')

if __name__ == "__main__":
    po = PaddingOracle()
    po.query(sys.argv[1])     # Issue HTTP query with the given argument (nothing should occur bc actual CT)
    # padding of 9, 3 blocks of messages
    po.break_up_plaintext(sys.argv[1], 9, 3)

    
    
    