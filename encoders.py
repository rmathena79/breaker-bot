import re

ENCODER_NONE = "None"
ENCODER_SIMPLIFIER = "Simplifier"
ENCODER_CAESAR = "Caesar Cipher"
ENCODER_SUBST = "Substitution Cipher"
ENCODER_ENIGMA = "Enigma Machine"
ALL_ENCODER_NAMES = [ENCODER_NONE, ENCODER_SIMPLIFIER, ENCODER_CAESAR, ENCODER_SUBST, ENCODER_ENIGMA]
CIPHER_NAMES = [ENCODER_CAESAR, ENCODER_SUBST, ENCODER_ENIGMA]

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

SIMPLIFICATION_MAP = {
    'Ç' : 'C',
    'ü' : 'u',
    'é' : 'e',
    'â' : 'a',
    'ä' : 'a',
    'à' : 'a',
    'å' : 'a',
    'ç' : 'c',
    'ê' : 'e',
    'ë' : 'e',
    'è' : 'e',
    'ï' : 'i',
    'î' : 'i',
    'ì' : 'i',
    'Ä' : 'a',
    'Å' : 'a',
    'É' : 'e',
    'æ' : 'a',
    'Æ' : 'a',
    'ô' : 'o',
    'ö' : 'o',
    'ò' : 'o',
    'û' : 'u',
    'ù' : 'u',
    'ù' : 'u',
    'ÿ' : 'y',
    'Ö' : 'o',
    'Ü' : 'u',
    'á' : 'a',
    'í' : 'i',
    'ó' : 'o',
    'ú' : 'u',
    'ñ' : 'n',
    'Ñ' : 'n'
}


# Simplify raw text:
#   Removing Project Gutenberg's boilerplate
#   Removing excessive whitespace
#   Applying the character map to remove accented characters and some formatting
#   Shifting to all-uppercase
#   Removing all remaining non-supported characters
def encode_simple(raw_text):
    print(f"Simplifying; original length {len(raw_text)}")
    # The good part starts on the first line after the "Start" marker
    good_part_start = raw_text.find("\n", raw_text.find(PG_START_CONTENT))

    # And it ends with the start of the "End" marker
    good_part_end = raw_text.find(PG_END_CONTENT)
    result = raw_text[good_part_start:good_part_end]
    print(f"Trimmed boilerplate; length {len(result)}")

    # Remove excessive whitespace by consolidating consequetive spaces and newlines
    result = re.sub(r' \t+', ' ', result)
    print(f"Squished spaces; length {len(result)}")

    result = re.sub(r'\n\n+', '\n\n', result)
    print(f"Squished newlines; length {len(result)}")

    # Character map
    result = result.translate(SIMPLIFICATION_MAP)

    # Uppercase

    # Remove all non-supported characters

    return result


def encode_caesar(plaintext, key: int):
    raise Exception("Not implemented")

def decode_caesar(plaintext, key: int):
    raise Exception("Not implemented")


def encode_substitution(plaintext, key: dict):
    raise Exception("Not implemented")

def decode_substitution(plaintext, key: dict):
    raise Exception("Not implemented")


def encode_enigma(plaintext, key):
    raise Exception("Not implemented")

def decode_enigma(plaintext, key):
    raise Exception("Not implemented")