import stegano
import sys

if len(sys.argv) < 3:
    print('Usage: coder.py encode/decode path/to/image.png ["message to code"]')
else:
    oper = sys.argv[1]
    path = sys.argv[2]

    if oper == 'decode':
        try:
            text = stegano.lsb.reveal(path)
            print("Found message:", text)
        except FileNotFoundError:
            print("Image file not found")
    elif oper == 'encode':
        if len(sys.argv) != 4:
            print('Usage: coder.py encode path/to/image.png "message to code"')
        else:
            text = sys.argv[3]
            try:
                secret = stegano.lsb.hide(path, text)
                secret.save(path[:path.rfind('.')] + "-coded" + path[path.rfind('.'):])
                print("Message coded")
            except FileNotFoundError:
                print("Image file not found")
    else:
        print('Usage: coder.py encode/decode path/to/image.png ["message to code"]')
