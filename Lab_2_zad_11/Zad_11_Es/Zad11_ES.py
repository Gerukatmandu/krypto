ALPHABET_UPPER = "AÁBCDEÉFGHIÍJKLMNÑOÓPQRSTUÜÚVWXYZ"
ALPHABET_LOWER = "aábcdeéfghiíjklmnñoópqrstuüúvwxyz"
OFTEN_SET = "EAOSNR"
RARE_SET = "ÑXÚKWÜ"
PROBABILITY_FACTOR = 3

DICTIONARY = []
with open("spanish_words.txt", "r") as file:
    DICTIONARY = [word.strip() for word in file.readlines()]

def get_input():
    text = ""
    while True:
        try:
            text += input()
        except EOFError:
            return text

def find_repeat(text_to_decode):
    text_to_decode = "".join([char for char in text_to_decode if char.upper() in ALPHABET_UPPER])
    repetitions = {}
    for char_idx in range(0, len(text_to_decode)-2):
        key = text_to_decode[char_idx:char_idx+3]
        possible_match_pos = 0
        for i in range(char_idx+3, len(text_to_decode)-2):
            possible_match_pos = text_to_decode.find(key, possible_match_pos + i)
            if possible_match_pos > 0:
                if key in repetitions.keys():
                    repetitions[key].append(possible_match_pos - char_idx)
                else:
                    repetitions[key] = [possible_match_pos - char_idx]
            elif possible_match_pos < 0:
                break
    return repetitions

def find_common_factors(pattern_with_repetitions):
    seq_with_factors = {}
    for key in pattern_with_repetitions.keys():
        seq_with_factors[key] = list()
        for value in pattern_with_repetitions[key]:
            seq_with_factors[key].extend([i for i in range(2, value+1) if (value % i) == 0])
    common_factors = list()
    for value in seq_with_factors.values():
        common_factors.extend(value)
    return sorted(common_factors)

def find_possible_keylength(factors):
    freq_of_factors = {}
    for factor in factors:
        if factor in freq_of_factors.keys():
            freq_of_factors[factor] += 1
        else:
            freq_of_factors[factor] = 1
    avg_freq_of_factor = -(-sum(freq_of_factors.values()) // len(freq_of_factors.values()) )
    max_freq_factors = set()
    for el in factors:
        if factors.count(el) > avg_freq_of_factor:
            max_freq_factors.add(el)
        if el > len(max(DICTIONARY, key=len)):
            break
    return sorted(max_freq_factors)

def create_substrings(ciphered_text, keylen):
    ciphered_text = "".join([char for char in ciphered_text if char in ALPHABET_UPPER])
    dict_of_substrings = ["" for _ in range(keylen)]
    for idx, char in enumerate(ciphered_text):
        dict_of_substrings[idx % keylen] += char
    return dict_of_substrings

def make_decipher_substrings(substring):
    list_of_deciphered_strings = []
    for i in range (0, len(ALPHABET_UPPER)):
        deciphered_string = ""
        for char in substring:
            deciphered_string += ALPHABET_UPPER[(ALPHABET_UPPER.index(char) - i) % len(ALPHABET_UPPER)]
        list_of_deciphered_strings.append(deciphered_string)
    return list_of_deciphered_strings

def count_freq_to_letters(text):
    letters_counter = {}
    # count frequncy of letter in ciphed text 
    for index_letter in range(0, len(ALPHABET_UPPER)):
        letters_counter[ALPHABET_UPPER[index_letter]] = text.count(ALPHABET_UPPER[index_letter])
    # create dictionary with frequency as key and list of letters as value for fms
    freq_to_letter = {}
    for letter, freq in letters_counter.items():
        if freq in freq_to_letter.keys():
            freq_to_letter[freq].append(letter)
        else:
            freq_to_letter[freq] = [letter]
    for val in freq_to_letter.values():
        val.sort(key=lambda char: 3 if char in OFTEN_SET else 1 if char in RARE_SET else 2)
    return sorted(freq_to_letter.items(), key=lambda x: x[0], reverse=True)

def frequency_match_score(freq_with_letters):
    # get all values (list of letters) in one list
    letters_with_freq = list()
    list(map(lambda e: letters_with_freq.extend(e[1]), freq_with_letters))
    fms_counter = 0
    for item in letters_with_freq[:-len(OFTEN_SET)][:len(OFTEN_SET)]: # often set
        if item in OFTEN_SET:
            fms_counter += 1
    for item in letters_with_freq[-len(OFTEN_SET):]: # rare set
        if item in RARE_SET:
            fms_counter += 1
    return fms_counter

def find_fms_for_all(list_of_sequences):
    scores = []
    for substring in list_of_sequences:
        freq_with_letters = count_freq_to_letters(substring)
        scores.append(frequency_match_score(freq_with_letters))
    return scores

def find_all_popular_subkeys(dict_of_key_substrings):
    list_of_popular_subkeys = []
    for substring in dict_of_key_substrings:
        deciphered_substrings = make_decipher_substrings(substring)
        fms_scores = find_fms_for_all(deciphered_substrings)
        popular_subkeys = [ALPHABET_UPPER[index] for index, score in enumerate(fms_scores) if score == max(fms_scores)]
        list_of_popular_subkeys.append(popular_subkeys)
    return list_of_popular_subkeys

def create_all_possible_keywords(list_with_subkeys):
    list_of_possible_keywords = ['']
    for sublist in list_with_subkeys:
        new_combinations = []
        for letter in sublist:
            for combination in list_of_possible_keywords:
                new_combinations.append(combination + letter)
        list_of_possible_keywords = new_combinations
    return list_of_possible_keywords

def probably_decoded(text):
    text_substrings = [w.upper() for w in text.split(' ')]
    common_words = set(DICTIONARY).intersection(set(text_substrings))
    return (len(common_words) > (len(text_substrings) // PROBABILITY_FACTOR))

def decipher(text_to_cypher, subkeys):
    all_possible_keywords = create_all_possible_keywords(subkeys)
    for keyword in all_possible_keywords:
        decoding_str = ""
        i = 0
        for char in text_to_cypher:
            if char.upper() in ALPHABET_UPPER:
                decoding_str += keyword[i % len(keyword)].lower()
                i += 1
            else:
                decoding_str += char

        decoded_text = ""
        for i, char in enumerate(text_to_cypher):
            if char in ALPHABET_UPPER:
                decoded_text += ALPHABET_UPPER[(ALPHABET_UPPER.index(char) \
                                - ALPHABET_UPPER.index(decoding_str[i].upper())) % len(ALPHABET_UPPER)]
            elif char in ALPHABET_LOWER:
                decoded_text += ALPHABET_LOWER[(ALPHABET_LOWER.index(char) \
                                - ALPHABET_LOWER.index(decoding_str[i].lower())) % len(ALPHABET_LOWER)]
            else:
                decoded_text += char
        if probably_decoded(decoded_text):
            return keyword, decoded_text
    return None, None


def kasiskiExam(text_to_decode):
    dict_repetitions = find_repeat(text_to_decode)
    common_factors = find_common_factors(dict_repetitions)
    possible_keylens = find_possible_keylength(common_factors)
    for keylen in possible_keylens:
        subkey_substrings = create_substrings(text_to_decode.upper(), keylen)
        popular_subkeys = find_all_popular_subkeys(subkey_substrings)
        key, decoded_text = decipher(text_to_decode, popular_subkeys)
        if key != None and decoded_text != None:
            print(decoded_text)
            print(key.lower())
            break

kasiskiExam(get_input())