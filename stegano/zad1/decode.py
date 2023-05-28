import stegano
import sys

if len(sys.argv) != 2:
    print('Usage: decode.py "path/to/image.png"')
else:
    path = sys.argv[1]

    try:
        text = stegano.red.reveal(path)
        print("Found message:", text)
    except FileNotFoundError:
        print("Image file not found")
