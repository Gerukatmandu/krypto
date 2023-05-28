import sys
import re

class CoderBase:
    def __init__(self, input_text):
        self.hex_table = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
        self.text = input_text

    def setup(self, pattern, zero, one, keep_pattern=False):
        self.pattern = pattern
        self.zero = zero
        self.one = one
        self.keep_pattern = keep_pattern

    def save(self, outname):
        with open(outname, 'w') as outfile:
            outfile.write(self.text)

class Coder(CoderBase):
    def process(self, message):
        message = self.to_binary(message)
        message = ('0' * (self.slots() - len(message))) + message
        parts = re.split(self.pattern, self.text)
        patterns = parts
        if self.keep_pattern:
            patterns = [parts[p] for p in range(1, len(parts), 2)]
            parts = [parts[p] for p in range(0, len(parts), 2)]
        self.text = parts[0]
        for part, char, pattern in zip(parts[1:], message, patterns):
            if self.keep_pattern:
                self.text += self.zero + pattern if char == '0' else pattern + self.one
            else:
                self.text += self.zero if char == '0' else self.one
            self.text += part

    def to_binary(self, message):
        return ''.join([bin(self.hex_table.index(c))[2:].rjust(4, "0") for c in message])

    def slots(self):
        return len(re.findall(self.pattern, self.text))

    def replace(self, pattern, replacement):
        self.text = re.sub(pattern, replacement, self.text)

class Decoder(CoderBase):
    def process(self):
        entries = re.findall(self.pattern, self.text)
        self.text = ''.join(['0' if c == self.zero else '1' for c in entries])
        print(self.text)
        self.text = self.from_binary(self.text)

    def from_binary(self, text):
        output = ''
        index = text.find('1')
        index -= 4 - (len(text) - index) % 4    # adjust for 4-bit numbers
        while index < len(text):
            num = int(text[index:index+4], 2)
            output += self.hex_table[num]
            index += 4
        return output


def encode(algorithm):
    with open('cover.html', 'r') as infile, open('mess.txt', 'r') as txtfile:
        text = txtfile.read().replace('\n','')
        coder = Coder(infile.read())

        if algorithm == '-1':
            coder.replace(' +\n', '\n')
            coder.setup('\n', '\n', ' \n')
        elif algorithm == '-2':
            coder.replace('  +', ' ')
            coder.setup(' ', ' ', '  ')
        elif algorithm == '-3':
            coder.replace('stno', '')
            coder.replace('stgn', '')
            coder.setup('class="', 'class="stno ', 'class="stgn ')
        else:   # '-4'
            coder.replace('<div></div>', '')
            coder.replace('(<div[^>]*>)(<div[^>]*>)', '\g<1>\n\g<2>')
            coder.setup('(<div[^>]*>)', '<div></div>', '<div></div>', True)

        if len(text) > coder.slots():
            print('Message to long for this algorithm.')
        else:
            coder.process(text)
            coder.save('watermark.html')
            print('Message coded')

def decode(algorithm):
    with open('watermark.html', 'r') as infile:
        decoder = Decoder(infile.read())

        if algorithm == '-1':
            decoder.setup(' *\n', '\n', ' \n')
        elif algorithm == '-2':
            decoder.setup(' +', ' ', '  ')
        elif algorithm == '-3':
            decoder.setup('class=".....', 'class="stno ', 'class="stgn ')
        else:   # '-4'
            decoder.setup('(<div></div>)?<div[^>]*>(<div></div>)?', ('<div></div>', ''), ('', '<div></div>'))

        decoder.process()
        decoder.save('detect.txt')
        print('Message decoded')


if len(sys.argv) != 3 or \
   sys.argv[1] not in ['-e', '-d'] or \
   sys.argv[2] not in ['-1', '-2', '-3', '-4']:
    print('Usage: stegano  <-e|-d>  <-1|-2|-3|-4>')
else:
    if sys.argv[1] == '-e':
        encode(sys.argv[2])
    else:   # -d
        decode(sys.argv[2])
