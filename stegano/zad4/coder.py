import stegano
import time
import os
import optparse

MESSAGE = 'This is a stegano test'
IMAGES = [
    'img/100k.png',
    'img/1m.png',
    'img/10m.png'
]
GENERATORS = {
    'identity': stegano.lsb.generators.identity,
    'triangular_numbers': stegano.lsb.generators.triangular_numbers,
    'eratosthenes': stegano.lsb.generators.eratosthenes,
    'composite': stegano.lsb.generators.composite
}

def timeit(func):
    def wrapper(*args):
        t = time.time_ns()
        func_return = func(*args)
        print(f'  Took {(time.time_ns() - t)/1000000:.2f}ms')
        return func_return
    return wrapper

def get_encoded_name(name, suffix):
    return  name[:name.rfind('.')] + suffix + name[name.rfind('.'):]

@timeit
def encode(image_path, text, encoder):
    print(f'Encoding {image_path} with {encoder.__name__} encoder')
    secret = stegano.lsb.hide(image_path, text, encoder())
    out_name = get_encoded_name(image_path, '-' + encoder.__name__)
    secret.save(out_name)
    print(f'  File size: original={os.stat(image_path).st_size / 1000:.2f}kB, encoded={os.stat(out_name).st_size / 1000:.2f}kB')

@timeit
def decode(image_path, encoder):
    print(f'Decoding {image_path} with {encoder.__name__} decoder')
    return stegano.lsb.reveal(image_path, encoder())

def read_args():
    parser = optparse.OptionParser()
    parser.add_option('-t', '--text', default=MESSAGE, help='Text to encode')
    parser.add_option('-m', '--mode', action='append', type='choice', choices=['encode', 'decode'], default=[],
                      help='Operation to run. One or more from: encode, decode')
    parser.add_option('-e', '--encoder', action='append', type='choice', choices=list(GENERATORS.keys()), default=[],
                      help=f'Encoder/decoder to use. One or more from: {", ".join(GENERATORS.keys())}')
    parser.add_option('-i', '--image', action='append', help='Image(s) to encode/decode', default=[])

    options, _ = parser.parse_args()
    if len(options.mode) == 0:
        options.mode = ['encode', 'decode']
    if len(options.encoder) == 0:
        options.encoder = list(GENERATORS.keys())
    if len(options.image) == 0:
        options.image = IMAGES
    return options


if __name__ == '__main__':
    opt = read_args()

    if 'encode' in opt.mode:
        for encoder in opt.encoder:
            for image in opt.image:
                encode(image, opt.text, GENERATORS[encoder])

    if 'decode' in opt.mode:
        for encoder in opt.encoder:
            for image in opt.image:
                msg = decode(get_encoded_name(image, '-' + encoder), GENERATORS[encoder])
                print('  Found message:', msg)
