import stegano
import sys

if len(sys.argv) != 3:
    print('Usage: encode.py "message to code" path/to/image.png')
else:
    text = sys.argv[1]
    path = sys.argv[2]

    if len(text) == 0:
        print("Invalid message length (should be 1-255)")
    else:
        try:
            secret = stegano.red.hide(path, text)
            secret.save(path[:path.rfind('.')] + "-coded" + path[path.rfind('.'):])
            print("Message coded")
        except FileNotFoundError:
            print("Image file not found")
