import re
import random

ENCODER_NONE = "None"
ENCODER_SIMPLIFIER = "Simplifier"
ENCODER_CAESAR = "Caesar Cipher"
ENCODER_SUBST = "Substitution Cipher"
ENCODER_ENIGMA = "Enigma Machine"
ALL_ENCODER_NAMES = [ENCODER_NONE, ENCODER_SIMPLIFIER, ENCODER_CAESAR, ENCODER_SUBST, ENCODER_ENIGMA]
#CIPHER_NAMES = [ENCODER_CAESAR, ENCODER_SUBST, ENCODER_ENIGMA]
CIPHER_NAMES = [ENCODER_CAESAR]

KEY_NAME_CAESAR = "Character Offset"
KEY_NAME_SUBST = "Character Map"
KEY_NAME_ENIGMA = "Rotor Settings"
KEY_NAMES = [KEY_NAME_CAESAR, KEY_NAME_SUBST, KEY_NAME_ENIGMA]

# Key strings for making sense of Project Gutenberg texts:
#!!! I have not confirmed that these are universal
PG_FIRST_LINE_START = "The Project Gutenberg eBook of "
PG_START_CONTENT = "*** START OF THE PROJECT GUTENBERG EBOOK "
PG_END_CONTENT = "*** END OF THE PROJECT GUTENBERG EBOOK "
PG_SENTINEL_LINE_END = " ***"

# Map for converting accented characters to something simpler. This is not good linguistically,
# but it's better than removing these character entirely. This also converts British Pounds and
# Yen symbols to a dollar sign ($), the division symbol to a forward slash, and Windows-stle
# line endings (\r\n) to Unix-style (\n).
SIMPLIFICATION_MAP = {
    'Ç' : 'C', 'ü' : 'u', 'é' : 'e', 'â' : 'a', 'ä' : 'a', 'à' : 'a', 'å' : 'a', 'ç' : 'c', 'ê' : 'e',
    'ë' : 'e', 'è' : 'e', 'ï' : 'i', 'î' : 'i', 'ì' : 'i', 'Ä' : 'a', 'Å' : 'a', 'É' : 'e', 'æ' : 'a',
    'Æ' : 'a', 'ô' : 'o', 'ö' : 'o', 'ò' : 'o', 'û' : 'u', 'ù' : 'u', 'ù' : 'u', 'ÿ' : 'y', 'Ö' : 'o',
    'Ü' : 'u', 'á' : 'a', 'í' : 'i', 'ó' : 'o', 'ú' : 'u', 'ñ' : 'n', 'Ñ' : 'n',
    '£' : '$', '¥' : '$', '÷': '/',
    '\r\n' : '\n'
}

CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-=`!#$%&*()+[];':\",./<>? \n"

def string_to_offsets(in_str:str) -> list[int]:
    return [CHARSET.find(c) for c in in_str ]

def offsets_to_string(offsets: list[int]) -> str:
    return "".join(CHARSET[i] for i in offsets)


# Simplify raw text:
#   Removing Project Gutenberg's boilerplate
#   Applying the character map to remove accented characters and some formatting
#   Shifting to all-uppercase
#   Removing all remaining non-supported characters
#   Removing excessive whitespace
#
# Result is returned as a string
def encode_simple(raw_text: str) -> str:
    # The good part starts on the first line after the "Start" marker
    good_part_start = raw_text.find("\n", raw_text.find(PG_START_CONTENT))

    # And it ends with the start of the "End" marker
    good_part_end = raw_text.find(PG_END_CONTENT)
    result = raw_text[good_part_start:good_part_end]

    # Character map
    result = result.translate(SIMPLIFICATION_MAP)

    # Uppercase
    result = result.upper()

    # Remove all non-supported characters
    # This is quite a slow implementation. Regex would be faster, but also harder to test given the paucity
    # of certain characters in the input and the handling of special characters within the regex string itself.
    result = "".join([c for c in result if c in CHARSET])

    # Remove excessive whitespace by consolidating consequetive spaces and newlines
    # We do this at the end because some of the previous adjustments might result in
    # whitespace characters getting joined up.
    result = re.sub(r'\n\n+', '\n\n', result)
    result = re.sub(r'  +', ' ', result)

    return result


def get_key_caesar() -> int:
    return random.randint(1, len(CHARSET)-1)

def encode_caesar(plaintext: str, key: int) -> str:
    if key < 1 or key >= len(CHARSET):
        raise Exception(f"Bad Caesar offset key: {key}")
    
    return _do_caesar(plaintext, key)

def decode_caesar(plaintext: str, key: int) -> str:
    if key < 1 or key >= len(CHARSET):
        raise Exception(f"Bad Caesar offset key: {key}")
    
    return _do_caesar(plaintext, -key)

# Reversing the Caesar Cipher is just a matter of changing the sign of the key, so it's
# really the same algorithm either way. Encode vs. decode functions above just enforce
# the key sign logic.
def _do_caesar(plaintext: str, key: int) -> str:
    result = "".join([CHARSET[(CHARSET.find(c) + key) % len(CHARSET)] for c in plaintext])
    return result


def encode_substitution(plaintext: str, key: dict) -> str:
    raise Exception("Not implemented")

def decode_substitution(plaintext: str, key: dict) -> str:
    raise Exception("Not implemented")


def encode_enigma(plaintext: str, key):
    raise Exception("Not implemented")

def decode_enigma(plaintext: str, key):
    raise Exception("Not implemented")


def self_test():
    TEST_STR = "ABCDEFG\n"
    TEST_OFFSETS = [0,1,2,3,4,5,6, len(CHARSET)-1]
    KEY = 3
    GOOD_CODED_STR = "DEFGHIJC"

    coded_str = encode_caesar(TEST_STR, KEY)
    print(f"Encode Caesar: {coded_str == GOOD_CODED_STR}")

    decoded_str = decode_caesar(GOOD_CODED_STR, KEY)
    print(f"Encode Caesar: {decoded_str == TEST_STR}")

    offsets = string_to_offsets(TEST_STR)
    print(f"string_to_offsets: {offsets == TEST_OFFSETS}")
    
    string_from_offsets = offsets_to_string(offsets)
    print(f"offsets_to_string: {string_from_offsets == TEST_STR}")

if __name__ == '__main__':
    self_test()