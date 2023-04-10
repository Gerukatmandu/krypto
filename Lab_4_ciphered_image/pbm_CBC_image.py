def read_picture(name):
    with open(name, 'rb') as f:
        while True:
            try:
                line = f.readline().decode('ascii').strip()
                width, height = map(int, line.split(' '))
                break
            except ValueError:
                pass
        picture = ''
        b = f.read(1)
        i = 0
        while b != b'':
            i += 1
            b_int = int(b.hex(), 16)
            picture += format(b_int, '08b')
            b = f.read(1)
        return picture, width, height

def write_picture(name, width, height, picture):
    with open(name, 'wb') as f:
        f.write(b'P4\n')
        f.write(f'{width} {height}\n'.encode('ascii'))
        pos = 0
        while pos < len(picture):
            binary_str = picture[pos:pos + 8]
            f.write(int(binary_str, 2).to_bytes(1, 'big'))
            pos += 8

def remove_padding(text, width, height):
    padding = 8 - (width % 8)
    out = ''
    for h in range(height):
        pos = h * (width + padding)
        out += text[pos:pos + width]
    return out

def fill_padding(text, width, height):
    padding = 8 - (width % 8)
    out = ''
    for h in range(height):
        pos = h * width
        out += text[pos:pos+width] + '0' * padding
    return out

def split_text(text_to_split):
    splitted_text = [text_to_split[char:char+12] for char in range(0, len(text_to_split), 12)]
    if len(splitted_text[-1]) < 12:
        splitted_text[-1] += '0' * (8 - len(splitted_text[-1]))
        splitted_text[-1] += '1100'
    return splitted_text

def make_R_permutation(right, permutation):
    return "".join(right[int(pos)] for pos in permutation)

def find_xor(right, key):
    return "".join(map(str, [int(r) ^ int(k) for r, k in zip(right, key)]))

def make_decimals(binary_string):
    return int(binary_string[:len(binary_string)//2], 2), \
           int(binary_string[len(binary_string)//2:], 2)

def mini_des(text_to_code, key, permutation, sbox1, sbox2):
    left, right = text_to_code[:len(text_to_code)//2], text_to_code[len(text_to_code)//2:]
    for i in range(1, 8):
        prepared_r = make_R_permutation(right, permutation)
        xor_result = find_xor(prepared_r, key[i:] + key[:i])
        index_sbox_1, index_sbox_2 = make_decimals(xor_result)
        right, left = find_xor(left, sbox1[index_sbox_1] + sbox2[index_sbox_2]), right
    return  (right + left)

# --------------------------------------------

input_permutation = "01323245"
sbox_1 = ["101", "010", "001", "110", "011", "100", "111", "000", "001", "100", "110", "010", "000", "111", "101", "011"]
sbox_2 = ["100", "000", "110", "101", "111", "001", "011", "010", "101", "011", "000", "111", "110", "010", "001", "100"]
input_key = "10101010"
seq_4 = "111011010010"

binary_picture, width, height = read_picture('washington.pbm')
binary_picture = remove_padding(binary_picture, width, height)
splitted_binary_picture = split_text(binary_picture)

xor_with_first_block = find_xor(splitted_binary_picture[0], seq_4)
second_block = mini_des(xor_with_first_block, input_key, input_permutation, sbox_1, sbox_2)
ciphered_image = [second_block]

for part in splitted_binary_picture[1:]:
    xor_with_first_block = find_xor(part, second_block)
    second_block = mini_des(xor_with_first_block, input_key, input_permutation, sbox_1,sbox_2)
    ciphered_image.append(second_block)

ciphered_image = "".join(ciphered_image)

ciphered_image = fill_padding(ciphered_image, width, height)
write_picture('ciphed_CBC.pbm', width, height, ciphered_image)
