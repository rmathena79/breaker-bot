import re
import random

ENCODER_NONE = "None"
ENCODER_SIMPLIFIER = "Simplifier"
ENCODER_CAESAR = "Caesar Cipher"
ENCODER_SUBST = "Substitution Cipher"
ALL_ENCODER_NAMES = [ENCODER_NONE, ENCODER_SIMPLIFIER, ENCODER_CAESAR, ENCODER_SUBST]
AVAILABLE_CIPHERS = [ENCODER_CAESAR] # Add additional ciphers as they are available

KEY_NAME_CAESAR = "Character Offset"
KEY_NAME_SUBST = "Character Map"
KEY_NAMES = [KEY_NAME_CAESAR, KEY_NAME_SUBST]

# Key strings for making sense of Project Gutenberg texts:
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

# Character set -- this defines the characters the encoders will actually handle. Text files need to
# be simplified to exclude any character outside this set before a cipher will work correctly.
#
# This is the character set I'd prefer to use, but resource limitations make it impractical:
# CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-=`!#$%&*()+[];':\",./<>? \n"
#
# This reduced character set has the most commonly used characters from the first several files I checked,
# notably including the space character:
CHARSET = " ETAONIRSH"


# Convert a string to a list of offsets in the character set
def string_to_offsets(in_str:str) -> list[int]:
    return [CHARSET.find(c) for c in in_str ]

# Convert a list of character set offsets to a string
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
    # and ends with the start of the "End" marker
    good_part_start = raw_text.find("\n", raw_text.find(PG_START_CONTENT))
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


# Get a key for the substitution cypher, in a form of a string where each character corresponds
# to the same index in the original character set.
def get_key_substitution() -> str:
    key = list(CHARSET)
    random.shuffle(key)
    return key

def encode_substitution(plaintext: str, key: str) -> str:
    return _do_substitution(plaintext, CHARSET, key)

def decode_substitution(plaintext: str, key: str) -> str:
    return _do_substitution(plaintext, key, CHARSET)

def _do_substitution(plaintext: str, key_from: str, key_to: str) -> str:
    result = "".join([key_to[key_from.find(c)] for c in plaintext])
    return result



def self_test():
    TEST_STR = "ABCDEFG\n"
    TEST_OFFSETS = [0,1,2,3,4,5,6, len(CHARSET)-1]

    # Hard-coded keys to bump everything by 3
    CAESAR_KEY = 3    
    SUBST_KEY = "DEFGHIJKLMNOPQRSTUVWXYZ1234567890-=`!#$%&*()+[];':\",./<>? \nABC"
    GOOD_CODED_STR = "DEFGHIJC"

    offsets = string_to_offsets(TEST_STR)
    print(f"string_to_offsets: {offsets == TEST_OFFSETS}")
    
    string_from_offsets = offsets_to_string(offsets)
    print(f"offsets_to_string: {string_from_offsets == TEST_STR}")


    c_coded_str = encode_caesar(TEST_STR, CAESAR_KEY)
    print(f"Encode Caesar: {c_coded_str == GOOD_CODED_STR}")

    c_decoded_str = decode_caesar(GOOD_CODED_STR, CAESAR_KEY)
    print(f"Decode Caesar: {c_decoded_str == TEST_STR}")

    
    s_coded_str = encode_substitution(TEST_STR, SUBST_KEY)
    print(f"Encode Substitution: {s_coded_str == GOOD_CODED_STR}")

    s_decoded_str = decode_substitution(GOOD_CODED_STR, SUBST_KEY)
    print(f"Decode Substitution: {s_decoded_str == TEST_STR}")

if __name__ == '__main__':
    self_test()