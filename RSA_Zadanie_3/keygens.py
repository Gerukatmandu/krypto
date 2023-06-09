import random

def reverse(a, b):
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
        if pow(num_a_, num_m*(2**i), num_n) == 1:
            if (pow(num_a_, num_m * (2 ** (i-1)), num_n) - num_n) == -1:
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
                    if pow(a, m, prime) == 1:
                        is_primary = True
                    else:
                        if rabin_miller(k, a, prime, m):
                            is_primary = True
                else:
                    is_primary = False
                    break
    return prime

def gen_rsa_key_pair(n):
    p = create_prime(n)
    q = create_prime(n)

    e = random.randint(pow(2, n-1), pow(2, n))
    while not (nwd(e, (p-1)*(q-1)) == 1):
        e = random.randint(pow(2, n-1), pow(2, n))

    if n in [10, 100, 1024, 2048]:
        e = random.randint(pow(2, n-1), pow(2, n))
        while not (nwd(e, (p-1)*(q-1)) == 1):
            e = random.randint(pow(2, n-1), pow(2, n))
    d = reverse(e, (p-1)*(q-1))
    return ((p * q, e), (p * q, d))

def gen_elgamal_key_pair(n):
    p = create_prime(n)
    x = random.randint(1, (p - 1) // 2)
    y = pow(2, x, p)
    return ((p, y), (p, x))
