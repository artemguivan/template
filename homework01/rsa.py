import random
import typing as tp


def is_prime(n: int) -> bool:

    for num in range(2, int(n**1 / 2) + 1):
        if n % num == 0:
            return True
    return False


def gcd(a: int, b: int) -> int:

    while b:
        a, b = b, a % b
    return a


def multiplicative_inverse(e: int, phi: int) -> int:

    max_el = max(e, phi)
    for i in range(max_el):
        if (i * e) % phi == 1:
            return i
    return 1


def generate_keypair(p: int, q: int) -> tp.Tuple[tp.Tuple[int, int], tp.Tuple[int, int]]:

    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both numbers must be prime.")
    elif p == q:
        raise ValueError("p and q cannot be equal")

    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(1, phi)
    g = gcd(e, phi)

    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    d = multiplicative_inverse(e, phi)

    return ((e, n), (d, n))


def encrypt(pk: tp.Tuple[int, int], plaintext: str) -> tp.List[int]:
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on
    # the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    # Return the array of bytes
    return cipher


def decrypt(pk: tp.Tuple[int, int], ciphertext: tp.List[int]) -> str:
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char**key) % n) for char in ciphertext]
    # Return the array of bytes as a string
    return "".join(plain)


if __name__ == "__main__":

    print("RSA Encrypter/ Decrypter")
    p = int(input("Enter a prime number (17, 19, 23, etc): "))
    q = int(input("Enter another prime number (Not one you entered above): "))
    print("Generating your public/private keypairs now . . .")
    public, private = generate_keypair(p, q)
    print("Your public key is ", public, " and your private key is ", private)
    message = input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(private, message)
    print("Your encrypted message is: ")
    print("".join(map(lambda x: str(x), encrypted_msg)))
    print("Decrypting message with public key ", public, " . . .")
    print("Your message is:")
    print(decrypt(public, encrypted_msg))
