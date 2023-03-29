ALPHABET_UPPER = "AÁBCDEÉFGHIÍJKLMNÑOÓPQRSTUÜÚVWXYZ"
ALPHABET_LOWER = "aábcdeéfghiíjklmnñoópqrstuüúvwxyz"

def get_input():
    text = []
    while True:
        try:
            substr = input()
            text.append(substr)
        except EOFError:
            return text

def cypher(text_to_cypher, coding_word):
    coding_str = ""
    i=0
    for char in text_to_cypher:
        if char.upper() in ALPHABET_UPPER:
            coding_str += coding_word[i % len(coding_word)]
            i += 1
        else:
            coding_str += char

    coded_text = ""
    for i, char in enumerate(text_to_cypher):
        if char in ALPHABET_UPPER:
            coded_text += ALPHABET_UPPER[(ALPHABET_UPPER.index(char) \
                            + ALPHABET_UPPER.index(coding_str[i].upper())) % 33]
        elif char in ALPHABET_LOWER:
            coded_text += ALPHABET_LOWER[(ALPHABET_LOWER.index(char) \
                            + ALPHABET_LOWER.index(coding_str[i].lower())) % 33]
        else:
            coded_text += char
        
    return coded_text


input_text = get_input()
code_word = input_text.pop()

print(cypher(input_text[0], code_word))


