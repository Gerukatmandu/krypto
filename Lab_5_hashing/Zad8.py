import hashlib
import random
import time

def generate_sequence(size):
    list_of_sequnces = []
    for i in range(10000):
        sequence = ""
        for j in range(size):
            sequence += chr(random.randint(97, 122))
        list_of_sequnces.append(sequence)
    return list_of_sequnces
        
def hash_md5(list_of_str_to_hash):
    start_time = time.time()
    return [hashlib.md5(sequence.encode()).hexdigest() for sequence in list_of_str_to_hash], (time.time() - start_time)

def hash_sha256(list_of_str_to_hash):
    start_time = time.time()
    return [hashlib.sha256(sequence.encode()).hexdigest() for sequence in list_of_str_to_hash], (time.time() - start_time)

def hash_sha3(list_of_str_to_hash):
    start_time = time.time()
    return [hashlib.sha3_256(sequence.encode()).hexdigest() for sequence in list_of_str_to_hash], (time.time() - start_time)

def hash_sha1(list_of_str_to_hash):
    start_time = time.time()
    return [hashlib.sha1(sequence.encode()).hexdigest() for sequence in list_of_str_to_hash], (time.time() - start_time)

def hash_blake2s(list_of_str_to_hash):
    start_time = time.time()
    return [hashlib.blake2s(sequence.encode()).hexdigest() for sequence in list_of_str_to_hash], (time.time() - start_time)

def hashing(list_of_sequences):
    time_measurements = {}
    hash_dict = {}
    hash_dict["md5"], time_measurements['md5'] = hash_md5(list_of_sequences)
    hash_dict["sha256"], time_measurements['sha256'] = hash_sha256(list_of_sequences)
    hash_dict["sha3"], time_measurements['sha3'] = hash_sha3(list_of_sequences)
    hash_dict["sha1"], time_measurements['sha1'] = hash_sha1(list_of_sequences)
    hash_dict["blake2s"], time_measurements['blake2s'] = hash_blake2s(list_of_sequences)
    return(hash_dict, time_measurements)

def if_collisions(type_of_hasing, dict_of_hashes):
    return True if len(set(dict_of_hashes[type_of_hasing])) != len(dict_of_hashes[type_of_hasing]) else False

def count_collisions(list_of_hashes):
    return len(list_of_hashes) - len(set(list_of_hashes))

def execute_calculation(hashes_dict):
    dict_of_collisions = {}
    for key in hashes_dict.keys():
        if if_collisions(key, hashes_dict):
            dict_of_collisions[key] = count_collisions(hashes_dict[key])
        else:
            dict_of_collisions[key] = 0
    return dict_of_collisions

    
def print_results(length, counters_dict, times_dict):
    print(f"String Length: {length}\n" + \
        "MD5 - Time: " + format(times_dict['md5'], ".4f") + f" seconds, Collisions: {counters_dict['md5']}\n" + \
        "SHA-256 - Time: " + format(times_dict['sha256'], ".4f") + f" second, Collisions: {counters_dict['sha256']}\n" + \
        "SHA3-256 - Time:  " + format(times_dict['sha3'], ".4f") + f" seconds, Collisions: {counters_dict['sha3']}\n" + \
        "BLAKE2S - Time: " + format(times_dict['blake2s'], ".4f") + f" seconds, Collisions: {counters_dict['blake2s']}\n" + \
        "SHA1 - Time: " + format(times_dict['sha1'], ".4f") + f" seconds, Collisions: {counters_dict['sha1']}")


lengths_of_sequences = [1, 10, 100, 1000, 10000]
for length in lengths_of_sequences:
    dict_of_hashes, dict_of_timings = hashing(generate_sequence(length))
    print_results(length, execute_calculation(dict_of_hashes), dict_of_timings)

