def encrypt_vigenere(plaintext: str, keyword: str) -> str:

    mask = [value.isupper() for value in plaintext]
    encrypt_vigenere_text = [char for char in plaintext]
    keyword = keyword.upper()
    plaintext = plaintext.upper()

    if len(plaintext) > len(keyword):
        new_keyword = [char for char in keyword]
        for char in range(len(keyword), len(plaintext)):
            new_keyword.append(keyword[char % len(keyword)])
        keyword = "".join(new_keyword)

    for num, key in enumerate(keyword):
        if plaintext[num].isalpha():
            num_key = ord(plaintext[num]) + ord(key) - ord("A")
            encrypt_char_num = (
                num_key if num_key < ord("Z") else (num_key - ord("Z") - 1 + ord("A"))
            )
            encrypt_char = chr(encrypt_char_num)
            encrypt_vigenere_text[num] = encrypt_char if mask[num] else encrypt_char.lower()

    return "".join(encrypt_vigenere_text)


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:

    mask = [value.isupper() for value in ciphertext]
    encrypt_vigenere_text = [char for char in ciphertext]
    keyword = keyword.upper()
    ciphertext = ciphertext.upper()

    if len(ciphertext) > len(keyword):
        new_keyword = [char for char in keyword]
        for char in range(len(keyword), len(ciphertext)):
            new_keyword.append(keyword[char % len(keyword)])
        keyword = "".join(new_keyword)

    for num, key in enumerate(keyword):
        # plaintext[num] - (ciphertext[num]
        if ciphertext[num].isalpha():
            num_key = ord(ciphertext[num]) - ord(key) + ord("A")
            encrypt_char_num = num_key if num_key >= ord("A") else (num_key + 26)
            encrypt_char = chr(encrypt_char_num)
            encrypt_vigenere_text[num] = encrypt_char if mask[num] else encrypt_char.lower()

    return "".join(encrypt_vigenere_text)
