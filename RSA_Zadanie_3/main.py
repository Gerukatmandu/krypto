import hashlib
import random
import sys
import keygens

def get_digest(msg):
    return int.from_bytes(hashlib.sha256(msg.encode()).digest(), byteorder='big')

def sign(method, msg, key):
    if method == 'rsa':
        return (pow(msg, key[1], key[0]),)
    else: # elgamal
        k = keygens.create_prime(min(256, key[0] - 2))
        k_inverse = pow(k, -1, key[0] - 1)
        r = pow(2, k, key[0])
        s = ((msg - key[1] * r) * k_inverse) % (key[0] - 1)
        return (r, s)

def verify(method, msg, sig, key):
    if method == 'rsa':
        left  = pow(sig[0], key[1], key[0])
        right = msg % key[0]
        return left == right
    else:   # elgamal
        left  = pow(2, msg, key[0])
        right = (pow(key[1], sig[0], key[0]) * pow(sig[0], sig[1], key[0])) % key[0]
        return left == right

usage = 'Usage: main.py -g|-s|-v method [filename]\n\t \
          -g - generate public and private keys\n\t \
          -s - sign file\n\t \
          -v - verify signature\n\t \
          method - signature method - rsa or elgamal (not used for generation)\n\t \
          filename - name of the file to sign/verify (not used for generation)'
if len(sys.argv) < 2 or sys.argv[1] not in ['-g', '-s', '-v']:
    print('Invalid or missing operation - expected -g, -s or -v')
    print(usage)
elif len(sys.argv) < 3 or sys.argv[2] not in ['rsa', 'elgamal']:
    print('Invalid or missing method - expected rsa or elgamal')
    print(usage)
else:
    _, operation, method, *args = sys.argv

    try:
        if operation == '-g':
            if len(args) != 0:
                print('Too many arguments provided')
                print(usage)
            else:
                if method == 'rsa':
                    pub, priv = keygens.gen_rsa_key_pair(random.randint(20, 40))
                else:   # elgamal
                    pub, priv = keygens.gen_elgamal_key_pair(random.randint(20, 40))
                with open('key.priv', 'w') as f_priv, open('key.pub', 'w') as f_pub:
                    f_priv.write('\n'.join(map(str, priv)))
                    f_pub.write( '\n'.join(map(str, pub )))
                    print('Keys generated')
        else:
            if len(args) != 1:
                print('Invalid number of arguments provided')
                print(usage)
            else:
                filename = args[0]
                if operation == '-s':
                    with open('key.priv', 'r') as f_key, open(filename, 'r') as f_input, open(filename + '.sig', 'w') as f_sign:
                        privkey = list(map(int, f_key.read().split()))
                        message = get_digest(f_input.read())
                        signature = sign(method, message, privkey)
                        f_sign.write(' '.join(map(str, signature)))
                        print('File signed')
                elif operation == '-v':
                    with open('key.pub', 'r') as f_key, open(filename, 'r') as f_input, open(filename + '.sig', 'r') as f_sign:
                        pubkey = list(map(int, f_key.read().split()))
                        message = get_digest(f_input.read())
                        signature = list(map(int, f_sign.read().split(' ')))
                        verified = verify(method, message, signature, pubkey)
                        print('Verification', 'successful' if verified else 'failed')
    except IOError as e:
        print('Error while processing request:', e)
