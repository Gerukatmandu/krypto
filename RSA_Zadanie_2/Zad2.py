import random
import optparse

def read_args():
    parser = optparse.OptionParser()
    parser.add_option('-s', '--block_size', default=1, help='Size of block of bytes')
    parser.add_option('-b', '--bits', default=2, help="Length of bits to generate the key")
    parser.add_option('-t', '--text', default='ala', help="Text to cipher")
    options, _ = parser.parse_args()
    return options
    
def inverse(a, b):
    u, w, x, z = 1, a, 0, b
    while w != 0:
        if w < z:
            u, x = x, u
            w, z = z, w
        q = w // z
        u -= q * x
        w -= q * z
    if z != 1:
        return 0
    if x < 0:
        x += b
    return x

def nwd(a, b):
    while a * b != 0:
        if a >=b:
            a = a % b
        else:
            b = b % a
    if a > 0:
        return a
    else:
        return b
    
def modulo_power(base, power, modulo):
    number = 1
    while power:
        if power & 1:
            number = number * base % modulo
        power >>= 1
        base = base * base % modulo
    return number

def if_power_of_two(number):
    while number > 1:
        if number % 2:
            return False
        number >>= 1
    return True

def find_max_power_of_two(number):
    max_power = 1
    while (number % (2 ** max_power)) == 0:
        max_power += 1
    return max_power - 1

def rabin_miller(num_k, num_a_, num_n, num_m):
    for i in range(num_k+1):
        if modulo_power(num_a_, num_m*(2**i), num_n) == 1:
            if (modulo_power(num_a_, num_m * (2 ** (i-1)), num_n) - num_n) == -1:
                return True                     # "Liczba pierwsza"
    return False                        # "Liczba zlozona"

def create_prime(rng):
    is_primary = False
    prime = -1
    random_generator = random.Random()
    while not is_primary:
        prime = random.randint(pow(2, rng-1), pow(2, rng))
        if prime % 2 == 0:
            is_primary = (prime == 2)
            continue
        for _ in range(5):
            a = random_generator.randint(2, prime-1)
            if not if_power_of_two(prime):
                k = find_max_power_of_two(prime - 1)    # k = max power of two
                m = (prime-1) // 2 ** k
                if nwd(a, prime) == 1:
                    if modulo_power(a, m, prime) == 1:
                        is_primary = True
                    else:
                        if rabin_miller(k, a, prime, m):
                            is_primary = True
                else:
                    is_primary = False
                    break
            if not is_primary:
                break
    return prime

def merge_blocks(size_of_block, text, multiplier):
    merged_blocks = []
    block = 0
    for i in range(0, len(text), size_of_block):
        block = 0
        for j in range(size_of_block):
            try:
                block += ord(text[i+j]) * (multiplier ** j)
            except Exception:
                block = list(map(ord, text[i:]))
                break
        merged_blocks.append(block) if type(block) == int  else merged_blocks.extend(block)
    return merged_blocks

def cipher(x, iter_pub_key):
    return pow(x, iter_pub_key[1], iter_pub_key[0])

def decipher(y, iter_priv_key):
    return pow(y, iter_priv_key[1], iter_priv_key[0])

def unmerge_blocks(list_of_blocks, size_of_block):
    separate_blocks = []
    for block in list_of_blocks:
        if block > 255:
            for _ in range(size_of_block):
                separate_blocks.append(block & 255) 
                block = block >> 8
        else:
            separate_blocks.append(block & 255) 
    return separate_blocks
    
if __name__ == '__main__':
    opt = read_args()
    n = int(opt.bits)
    if n < 5:
        print("To cipher size of bits should can't be less then 5...")
        print("Setting n to 5...")
        n = 5
    s = int(opt.block_size)
    n = n * s
    text_to_cipher = opt.text
    const_for_cipher = 256
    
    p = create_prime(n)
    q = create_prime(n)
    
    e = random.randint(pow(2, n-1), pow(2, n))
    while not (nwd(e, (p-1)*(q-1)) == 1):
        e = random.randint(pow(2, n-1), pow(2, n))
    
    text_to_cipher_ascii = [ord(char) for char in text_to_cipher]
    pub_key = (p*q, e)
    priv_key = (p*q, inverse(e, (p-1)*(q-1)))
    blocks_of_text = merge_blocks(s, text_to_cipher, const_for_cipher)
    ciphered_blocks = [cipher(char, pub_key) for char in blocks_of_text]
    deciphered_blocks= [decipher(char, priv_key) for char in ciphered_blocks]
    unmerged_ciphered_blocks = unmerge_blocks(deciphered_blocks, s)
    deciphered_text = "".join([chr(char) for char in unmerged_ciphered_blocks])

    with open("data.txt", "w") as output_file:
        output_file.write(f"Text to cipher: {text_to_cipher}\n" 
                    f"Text to cipher ascii: {text_to_cipher_ascii}\n"
                    f"Generated data: p = {p}, q = {q}, e = {e}\n" 
                    f"Generated keys: \n" 
                    f"\t\t\tpub key {pub_key}, \n" 
                    f"\t\t\tpriv key {priv_key}\n" 
                    f"Blocks of text: {blocks_of_text}\n" 
                    f"Ciphered blocks:  {ciphered_blocks}\n"
                    f"Deciphered blocks: {deciphered_blocks}\n"
                    f"unmerged ciphered blocks: {unmerged_ciphered_blocks}\n"
                    f"Deciphered text: {deciphered_text}\n")




# example run:
# python Zad2.py -t "ala ma kota" -s 8 -b 10