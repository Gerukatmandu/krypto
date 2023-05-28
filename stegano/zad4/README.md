

# Prerequisites
 - Python 3.10
 - Pillow
 - piexif
 - Stegano

## Running

Usage: coder.py *[options]*

**Options:**
||||
|-|-|-|
| -h | - -help | show this help message and exit |
| -m MODE | - -mode=MODE | Operation to run. One or more from: encode, decode |
| -t TEXT | - -text=TEXT | Text to encode |
| -e ENCODER | - -encoder=ENCODER | Encoder/decoder to use.<br/>One or more from: identity,                triangular_numbers, eratosthenes, composite |
| -i IMAGE | - -image=IMAGE | Image(s) to encode/decode |

By default, all encoders are used to encode and then decode 3 files from the *img* folder: *100k.png, 1m.png* and *10m.png*, using a *"This is a stegano test"* message.

## Example results

    Encoding img/100k.png with identity encoder
      File size: original=105.31kB, encoded=102.70kB
      Took 50.56ms
    Encoding img/1m.png with identity encoder
      File size: original=1098.41kB, encoded=1120.45kB
      Took 402.58ms
    Encoding img/10m.png with identity encoder
      File size: original=10622.53kB, encoded=10263.33kB
      Took 3992.00ms
    Encoding img/100k.png with triangular_numbers encoder
      File size: original=105.31kB, encoded=102.76kB
      Took 31.00ms
    Encoding img/1m.png with triangular_numbers encoder
      File size: original=1098.41kB, encoded=1120.43kB
      Took 396.27ms
    Encoding img/10m.png with triangular_numbers encoder
      File size: original=10622.53kB, encoded=10263.34kB
      Took 4012.94ms
    Encoding img/100k.png with eratosthenes encoder
      File size: original=105.31kB, encoded=102.77kB
      Took 30.00ms
    Encoding img/1m.png with eratosthenes encoder
      File size: original=1098.41kB, encoded=1120.43kB
      Took 401.57ms
    Encoding img/10m.png with eratosthenes encoder
      File size: original=10622.53kB, encoded=10263.35kB
      Took 4001.27ms
    Encoding img/100k.png with composite encoder
      File size: original=105.31kB, encoded=102.69kB
      Took 30.26ms
    Encoding img/1m.png with composite encoder
      File size: original=1098.41kB, encoded=1120.45kB
      Took 391.18ms
    Encoding img/10m.png with composite encoder
      File size: original=10622.53kB, encoded=10263.34kB
      Took 4028.04ms
    Decoding img/100k-identity.png with identity decoder
      Took 4.00ms
      Found message: This is a stegano test
    Decoding img/1m-identity.png with identity decoder
      Took 24.50ms
      Found message: This is a stegano test
    Decoding img/10m-identity.png with identity decoder
      Took 244.58ms
      Found message: This is a stegano test
    Decoding img/100k-triangular_numbers.png with triangular_numbers decoder
      Took 7.27ms
      Found message: This is a stegano test
    Decoding img/1m-triangular_numbers.png with triangular_numbers decoder
      Took 23.97ms
      Found message: This is a stegano test
    Decoding img/10m-triangular_numbers.png with triangular_numbers decoder
      Took 242.13ms
      Found message: This is a stegano test
    Decoding img/100k-eratosthenes.png with eratosthenes decoder
      Took 10.37ms
      Found message: This is a stegano test
    Decoding img/1m-eratosthenes.png with eratosthenes decoder
      Took 24.00ms
      Found message: This is a stegano test
    Decoding img/10m-eratosthenes.png with eratosthenes decoder
      Took 246.64ms
      Found message: This is a stegano test
    Decoding img/100k-composite.png with composite decoder
      Took 8.69ms
      Found message: This is a stegano test
    Decoding img/1m-composite.png with composite decoder
      Took 24.00ms
      Found message: This is a stegano test
    Decoding img/10m-composite.png with composite decoder
      Took 275.59ms
      Found message: This is a stegano test
