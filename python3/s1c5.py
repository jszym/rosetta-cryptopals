# This is free and unencumbered software released into the public domain

def repeating_xor(plain, key):
    return bytes([c ^ key[i % len(key)] for i, c in enumerate(plain)])

if __name__ == "__main__":
    plain = b"""Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""
    key = b"ICE"
    cipher = repeating_xor(plain, key)
    print(bytes(cipher).hex())