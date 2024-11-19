import re

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


# Simplify raw text:
#   Removing Project Gutenberg's boilerplate
#   Applying the character map to remove accented characters and some formatting
#   Shifting to all-uppercase
#   Removing all remaining non-supported characters
#   Removing excessive whitespace
#
# Result is returned as a string
def encode_simple(raw_text: str):
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
    result = re.sub(r' \t+', ' ', result)
    result = re.sub(r'\n\n+', '\n\n', result)

    return result


# Returns result as a string
def encode_caesar(plaintext: str, key: int):
    if key < 1 or key >= len(CHARSET):
        raise Exception(f"Bad Caesar offset key: {key}")
    
    #!!!
    result = "".join([CHARSET[CHARSET.find(c)] for c in plaintext])
    return result    

# Returns result as a string
def decode_caesar(plaintext: str, key: int):
    raise Exception("Not implemented")


# Returns result as a string
def encode_substitution(plaintext: str, key: dict):
    raise Exception("Not implemented")

# Returns result as a string
def decode_substitution(plaintext: str, key: dict):
    raise Exception("Not implemented")


def encode_enigma(plaintext: str, key):
    raise Exception("Not implemented")

def decode_enigma(plaintext: str, key):
    raise Exception("Not implemented")