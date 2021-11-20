import RPi.GPIO as GPIO
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from binascii import hexlify, unhexlify
import gmpy2
from gmpy2 import mpz
 
from tqdm import tqdm
 
message = b'Hello World'
key = RSA.importKey(open('test.key').read())
h = SHA256.new(message)
 
print("Loaded SECRET KEY:")
print("  SECRET KNOWN p: {}".format(key._key['p']))
print("  SECRET KNOWN q: {}".format(key._key['q']))
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
 
p = PKCS1_v1_5.new(key)
 
GPIO.output(18, GPIO.LOW)
GPIO.output(18, GPIO.HIGH)
known_good = p.sign(h)
GPIO.output(18, GPIO.LOW)
 
pbar = tqdm(total=0)
 
while True:
	GPIO.output(18, GPIO.LOW)
	GPIO.output(18, GPIO.HIGH)
	output = p.sign(h)
	GPIO.output(18, GPIO.LOW)
 
	#output = b'\x93\x07\xc0\x02\xc9\x85\n\xb3lY\xad\xb4hY\xf1\x18\x8c\x05\xc0\xa7\xf5\x02y\xd907/\xb7\xc8>\x99d\xba\xdf\xda_\xb29\x9ao\xf2\x11X\x883u\xa0Wm\x921\xb3_H\x89T\x8c\xd2\xb9\xa0\xeb7\xa2\x14\xd4&y\x88Xf\xfb\xb0%\xbb2\x08`\xb8l\xaa\x93\x85\x8965\x17\xef(\x07\x04P\xb9\xc0E\x14\xeeD\x9e2\xd2"\x93i\xd3$x\x82\xdd\x81*g\xd8\x7f\xf7\xf3\x91\x913\x04\xffL\x89<\x9f\x1d\xeb:x\xf4\x86\xcf\x8b\xa8\xf1\xf8"G!\xcf\x15\xee\xd63\xe0js\x17t@\x84{\xc8\x0f\xe7:q\xccn\xf7\xeey<\x0e\xab\x01\x19 \xe8{a\xb4\xa1\x8b\x19~\x87\xb1\xe2W9\xa2HC\x1c\x9fOU\x1f\x8d\xcdk\\]\t\x8e(\xe2\x1c\x96\xed]\xb1M\xb5F\xa3\xca\xd6\xbe\xccb\x87C\xbfE>\xbbU\xe6\xf4\xba\xe5\x95K!\xce\xad\nW{+0\xca\x0eX\x92<\x91\x89\rK\xdb\x00]\x0c\xe1\x04"\x1c\xf8/\xcd\x96\xc3\xfa\x9f'
	#output = b'\xc9\xa0\x14\x0f\xad\xd3\xb2\x9dK\x15\xe7Zg{\x98\x04n{\xedP\xbc\xb2Ek\x04\xa4\x14\x00\xe5wEg}\x13\x98\x9e\xfe\x82\x90\xbdl\x81\n!\xf9\xf1uAE\x8e\x13\xf6\xb0[\xaab\x89d\x10\xfc\x91\x19s6\xaaRz\xa9\x06F\xc8\xf3\xd4+\x14*!S3\x93hU\xf7\xf12i,\xbdq\x1dS*&\xac\xab\xdc\xad\xbe\xa0\x0e\xef\xa6\xb1\xb1\x95r\xa1\xd8\x95\xcb)\x02\xcd\xc1\xe4\x98\xfeD\xbd\xb1\xa2\x13\xa8\\\xedSt^\xb72k\x89\x08%\x7fy+B\xc7\xe5>A1f\x05h\xec\xfc53\xb1\xb1\xa4\xbc-\x9bI\x7f\xb0V\xccw\x9f\x96\xe8\x83\xef\x1cq-\x1b+\x16\xa6n\x0e\xa6\x98V\xf0\xcf\x93\x97WO\t\xe4/\xeb8\xf4\xb5:\x1bc\x02\x1fz\x1fb\x8d\xcf\xac\xf0\xd2|\xb8\x13\xa62h\x85\x10\xa5\xc61\xe4em\xdcT=1*\x1a\xa2v;\x862<-\x8d\xbdJ\xd32\n\x96\xbb\xac\xb13\xda\xf6A\x00\xc9\x01\xcb\x10\xe4R\xee\xaeE'
 
	if output != known_good:
		print(output)
		break
	pbar.update(1)
 
pbar.close()
 
def build_message(m, n):
    sha_id = "3031300d060960864801650304020105000420"
    pad_len = (len(hex(n)) - 2) // 2 - 3 - len(m)//2 - len(sha_id)//2
    padded_m = "0001" + "ff" * pad_len + "00" + sha_id + m
    return padded_m
 
e = mpz(int.from_bytes(key._key['e'].to_bytes(), "big"))
n = mpz(int.from_bytes(key._key['n'].to_bytes(), "big"))
 
print("PUBLIC e: {}".format(e))
 
hashed_m = hexlify(h.digest()).decode()
padded_m = build_message(hashed_m, n)
print("Hashed: {}".format(hashed_m))
print("Padded: {}".format(padded_m))
 
sig = output
 
sig_int = mpz(int.from_bytes(sig, "big"))
m_int = mpz(int.from_bytes(unhexlify(padded_m), "big"))
p_test = gmpy2.gcd(m_int - sig_int ** e, n)
 
print("RECOVERED 0: {}".format(p_test))
print("RECOVERED 1: {}".format(n//p_test))