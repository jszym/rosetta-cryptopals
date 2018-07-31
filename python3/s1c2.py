# This is free and unencumbered software released into the public domain

from base64 import b16encode

a_hex = "1c0111001f010100061a024b53535009181c"
b_hex = "686974207468652062756c6c277320657965"
expected_hex = "746865206b696420646f6e277420706c6179"

if __name__ == "__main__":
    
    a_bin = bytes.fromhex(a_hex)
    b_bin = bytes.fromhex(b_hex)

    result_bin = bytes([a ^ b for a, b in zip(a_bin, b_bin)])
    result_hex = b16encode(result_bin).decode("utf8")

    print("expect", expected_hex)
    print("result", result_hex)
