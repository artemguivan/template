def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    z_number = 122
    a_number = 97
    Z_number = 90
    A_number = 65

    ciphertext = []
    for char in plaintext:
        if char.isalpha():
            if char.isupper():
                ord_of_char = ord(char) + shift
                cycle_num = ord_of_char - Z_number + A_number - 1
                ciphertext.append(chr(ord_of_char) if ord_of_char <= Z_number else chr(cycle_num))
            else:
                ord_of_char = ord(char) + shift
                cycle_num = ord_of_char - z_number + a_number - 1
                ciphertext.append(chr(ord_of_char) if ord_of_char <= z_number else chr(cycle_num))
        else:
            ciphertext.append(char)
    return "".join(ciphertext)


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    z_number = 122
    a_number = 97
    Z_number = 90
    A_number = 65

    plaintext = []
    for char in ciphertext:
        if char.isalpha():
            if char.isupper():
                ord_of_char = ord(char) - shift
                cycle_num = Z_number - (A_number - ord_of_char) + 1
                plaintext.append(chr(ord_of_char) if ord_of_char >= A_number else chr(cycle_num))
            else:
                ord_of_char = ord(char) - shift
                cycle_num = z_number - (a_number - ord_of_char) + 1
                plaintext.append(chr(ord_of_char) if ord_of_char >= a_number else chr(cycle_num))
        else:
            plaintext.append(char)
    return "".join(plaintext)
