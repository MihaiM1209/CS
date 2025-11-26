#!/usr/bin/env python3

import random
import hashlib
from Crypto.Util.number import GCD, inverse


HASH_ALGORITHMS = [
    "NTLM", "MD4", "MD5", "MD2", "MD6-128", "MD6-256", "MD6-512",
    "SHA-1", "SHA-224", "SHA-256", "SHA-384", "SHA-512",
    "SHA3-224", "SHA3-256", "SHA3-384", "SHA3-512",
    "RipeMD-128", "RipeMD-160", "RipeMD-256", "RipeMD-320",
    "Whirlpool", "Haval192,3", "Haval224,4", "Haval256,4"
]


P = 32317006071311007300153513477825163362488057133489075174588434139269806834136210002792056362640164685458556357935330816928829023080573472625273554742461245741026202527916572972862706300325263428213145766931414223654220941111348629991657478268034230553086349050635557712219187890332729569696129743856241741236237225197346402691855797767976823014625397933058015226858730761197532436467475855460715043896844940366130497697812854295958659597567051283852132784468522925504568272879113720098931873959143374175837826000278034973198552060607533234122603254684088120031105907484281003994966956119696956248629032338072839127039
G = 2


def select_hash_algorithm(student_number):
    i = (student_number % 24) + 1
    hash_algorithm = HASH_ALGORITHMS[i - 1]
    return hash_algorithm, i


def compute_hash(message_bytes, hash_algorithm):
    print(f"\nComputing hash using {hash_algorithm}...")


    hash_functions = {
        "SHA-1": hashlib.sha1,
        "SHA-224": hashlib.sha224,
        "SHA-256": hashlib.sha256,
        "SHA-384": hashlib.sha384,
        "SHA-512": hashlib.sha512,
        "SHA3-224": lambda: hashlib.sha3_224(),
        "SHA3-256": lambda: hashlib.sha3_256(),
        "SHA3-384": lambda: hashlib.sha3_384(),
        "SHA3-512": lambda: hashlib.sha3_512(),
        "MD5": hashlib.md5,
        "MD4": lambda: hashlib.new('md4'),
        "MD2": lambda: hashlib.new('md2'),
        "RipeMD-128": lambda: hashlib.new('ripemd128'),
        "RipeMD-160": lambda: hashlib.new('ripemd160'),
        "RipeMD-256": lambda: hashlib.new('ripemd256'),
        "RipeMD-320": lambda: hashlib.new('ripemd320'),
        "Whirlpool": lambda: hashlib.new('whirlpool'),
        "NTLM": lambda: hashlib.new('md4'),
    }

    if hash_algorithm in hash_functions:
        hash_func = hash_functions[hash_algorithm]
        if callable(hash_func) and hash_func.__code__.co_argcount == 0:
            h = hash_func()
        else:
            h = hash_func()
        h.update(message_bytes)
        hash_bytes = h.digest()
    else:

        print(f"Warning: {hash_algorithm} not fully supported, using SHA-256")
        hash_bytes = hashlib.sha256(message_bytes).digest()


    hash_hex = hash_bytes.hex()


    hash_decimal = int(hash_hex, 16)

    print(f"Hash (hex): {hash_hex}")
    print(f"Hash (decimal): {hash_decimal}")

    return hash_bytes, hash_decimal, hash_hex


def generate_elgamal_keys(p, g):
    print("\n" + "=" * 80)
    print("ELGAMAL KEY GENERATION")
    print("=" * 80)

    print(f"\nGiven parameters:")
    print(f"  p = {p}")
    print(f"  p has {p.bit_length()} bits")
    print(f"  g = {g} (generator)")


    print(f"\nStep 1: Choose private key x such that 1 < x < p-1")
    x_min = 2
    x_max = min(p - 2, 2**256)

    x = random.randint(x_min, x_max)
    print(f"Selected private key x = {x}")


    print(f"\nStep 2: Calculate public key y = g^x (mod p)")
    y = pow(g, x, p)
    print(f"  y = {y}")

    public_key = (p, g, y)
    private_key = (x, p)

    print("\n" + "=" * 80)
    print("GENERATED KEYS")
    print("=" * 80)
    print(f"Public Key: (p, g, y) = ({p}, {g}, {y})")
    print(f"Private Key: (x, p) = ({x}, {p})")

    return public_key, private_key


def elgamal_sign(message_bytes, private_key, hash_algorithm):
    x, p = private_key

    print("\n" + "=" * 80)
    print("ELGAMAL SIGNATURE GENERATION")
    print("=" * 80)
    print(f"Message: {message_bytes}")


    hash_bytes, hash_decimal, hash_hex = compute_hash(message_bytes, hash_algorithm)


    hash_mod = hash_decimal % (p - 1)
    print(f"\nHash H(m) mod (p-1): {hash_mod}")


    print(f"\nStep 2: Choose random secret k such that 1 < k < p-1 and GCD(k, p-1) = 1")
    k_min = 2
    k_max = min(p - 2, 2**256)

    while True:
        k = random.randint(k_min, k_max)
        if GCD(k, p - 1) == 1:
            break

    print(f"  Selected k = {k}")
    print(f"  Verification: GCD({k}, {p-1}) = {GCD(k, p-1)} ✓")


    print(f"\nStep 3: Calculate r = g^k (mod p)")
    print(f"  r = {G}^{k} mod {p}")
    r = pow(G, k, p)
    print(f"  r = {r}")


    print(f"\nStep 4: Calculate s = k^(-1) * (H(m) - x*r) (mod (p-1))")


    k_inv = inverse(k, p - 1)
    print(f"  k^(-1) mod (p-1) = {k_inv}")


    temp = (hash_mod - x * r) % (p - 1)
    print(f"  (H(m) - x*r) mod (p-1) = ({hash_mod} - {x}*{r}) mod ({p-1}) = {temp}")


    s = (k_inv * temp) % (p - 1)
    print(f"  s = {k_inv} * {temp} mod ({p-1}) = {s}")

    signature = (r, s)

    print(f"\nSignature: (r, s) = ({r}, {s})")

    return signature, hash_mod, k


def elgamal_verify(message_bytes, signature, public_key, hash_algorithm):
    r, s = signature
    p, g, y = public_key

    print("\n" + "=" * 80)
    print("ELGAMAL SIGNATURE VERIFICATION")
    print("=" * 80)
    print(f"Message: {message_bytes}")
    print(f"Signature: (r, s) = ({r}, {s})")


    hash_bytes, hash_decimal, hash_hex = compute_hash(message_bytes, hash_algorithm)


    hash_mod = hash_decimal % (p - 1)
    print(f"\nHash H(m) mod (p-1): {hash_mod}")


    print(f"\nStep 2: Verify signature")
    print(f"Verification formula: g^H(m) ≡ y^r * r^s (mod p)")


    left_side = pow(g, hash_mod, p)
    print(f"\n  Left side: g^H(m) mod p = {g}^{hash_mod} mod {p} = {left_side}")


    y_power_r = pow(y, r, p)
    r_power_s = pow(r, s, p)
    right_side = (y_power_r * r_power_s) % p

    print(f"  Right side: y^r * r^s mod p")
    print(f"    y^r mod p = {y}^{r} mod {p} = {y_power_r}")
    print(f"    r^s mod p = {r}^{s} mod {p} = {r_power_s}")
    print(f"    y^r * r^s mod p = {right_side}")


    print(f"\nStep 3: Compare")
    is_valid = (left_side == right_side)

    if is_valid:
        print(f"✓ {left_side} ≡ {right_side} (mod p)")
        print("✓ Signature is VALID!")
    else:
        print(f"✗ {left_side} ≠ {right_side} (mod p)")
        print("✗ Signature is INVALID!")

    return is_valid, left_side, right_side


def main():
    print("=" * 80)
    print("ELGAMAL DIGITAL SIGNATURE IMPLEMENTATION - Lab 6, Task 3")
    print("=" * 80)
    print("Requirements:")
    print("- Sign and validate digital signature of message m from Lab 2")
    print("- Use given parameters: p (2048-bit) and g=2")
    print("- Use hash algorithm selected from list: i = (k mod 24) + 1")
    print("- Hash value representation: Decimal")


    print("\n" + "=" * 80)
    print("HASH ALGORITHM SELECTION")
    print("=" * 80)
    try:
        student_number = int(input("Enter your student number (k) in group list: ").strip())
    except (ValueError, KeyboardInterrupt):
        print("Using default student number k = 1")
        student_number = 1

    hash_algorithm, hash_index = select_hash_algorithm(student_number)
    print(f"\nStudent number k = {student_number}")
    print(f"Hash index i = (k mod 24) + 1 = ({student_number} mod 24) + 1 = {hash_index}")
    print(f"Selected hash algorithm: {hash_algorithm}")


    message_text = "Nume Prenume"
    message_bytes = message_text.encode('utf-8')

    print(f"\nMessage from Lab 2: '{message_text}'")


    public_key, private_key = generate_elgamal_keys(P, G)
    p, g, y = public_key
    x, _ = private_key


    signature, hash_value, k = elgamal_sign(message_bytes, private_key, hash_algorithm)
    r, s = signature


    is_valid, left_side, right_side = elgamal_verify(
        message_bytes, signature, public_key, hash_algorithm
    )


    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Message: '{message_text}'")
    print(f"Hash Algorithm: {hash_algorithm} (index {hash_index})")
    print(f"Hash H(m) mod (p-1): {hash_value}")
    print(f"Prime p: {p.bit_length()} bits")
    print(f"Generator g: {g}")
    print(f"Public key y: {y}")
    print(f"Private key x: {x}")
    print(f"Random secret k (used in signing): {k}")
    print(f"Signature: (r, s) = ({r}, {s})")
    print(f"Signature Valid: {'✓ YES' if is_valid else '✗ NO'}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()

