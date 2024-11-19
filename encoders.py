ENCODER_NONE = "None"
ENCODER_SIMPLIFIER = "Simplifier"
ENCODER_CAESAR = "Caesar Cipher"
ENCODER_SUBST = "Substitution Cipher"
ENCODER_ENIGMA = "Enigma Machine"
ENCODER_NAMES = [ENCODER_NONE, ENCODER_SIMPLIFIER, ENCODER_CAESAR, ENCODER_SUBST, ENCODER_ENIGMA]

KEY_NAME_CAESAR = "Character Offset"
KEY_NAME_SUBST = "Character Map"
KEY_NAME_ENIGMA = "Dials maybe?"
KEY_NAMES = [KEY_NAME_CAESAR, KEY_NAME_SUBST, KEY_NAME_ENIGMA]

def encode_simple(original):
    raise Exception("Not implemented")

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