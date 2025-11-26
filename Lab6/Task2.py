#!/usr/bin/env python3

import random
import hashlib
from Crypto.Util.number import getPrime, GCD, inverse


HASH_ALGORITHMS = [
    "MD4", "MD5", "MD2", "MD6-128", "MD6-256", "MD6-512",
    "SHA-1", "SHA-224", "SHA-256", "SHA-384", "SHA-512",
    "SHA3-224", "SHA3-256", "SHA3-384", "SHA3-512",
    "RipeMD-128", "RipeMD-160", "RipeMD-256", "RipeMD-320",
    "Whirlpool", "NTLM", "Haval192,3", "Haval224,4", "Haval256,4"
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


def generate_rsa_keys(key_size_bits=3072):
    print("\n" + "=" * 80)
    print("RSA KEY GENERATION")
    print("=" * 80)


    print(f"\nStep 1: Generating two large prime numbers p and q...")
    print(f"Target: n = p * q must be at least {key_size_bits} bits")

    p_bits = key_size_bits // 2
    q_bits = key_size_bits - p_bits

    p = getPrime(p_bits)
    q = getPrime(q_bits)

    print(f"Generated p: {p_bits}-bit prime")
    print(f"Generated q: {q_bits}-bit prime")


    n = p * q
    n_bits = n.bit_length()
    print(f"\nStep 2: Calculate n = p * q")
    print(f"n has {n_bits} bits {'✓' if n_bits >= key_size_bits else '✗'}")


    phi_n = (p - 1) * (q - 1)
    print(f"\nStep 3: Calculate φ(n) = (p-1) * (q-1)")


    print(f"\nStep 4: Choose public exponent e such that GCD(e, φ(n)) = 1")
    e_candidates = [65537, 3, 17, 257]
    e = None

    for candidate in e_candidates:
        if candidate < phi_n and GCD(candidate, phi_n) == 1:
            e = candidate
            break

    if e is None:
        while True:
            e = random.randint(3, phi_n - 1)
            if GCD(e, phi_n) == 1:
                break

    print(f"Selected e = {e}")


    print(f"\nStep 5: Calculate private exponent d such that e * d ≡ 1 (mod φ(n))")
    d = inverse(e, phi_n)
    print(f"Verification: (e * d) mod φ(n) = {(e * d) % phi_n} ✓")

    public_key = (n, e)
    private_key = (d, n)

    print("\n" + "=" * 80)
    print("GENERATED KEYS")
    print("=" * 80)
    print(f"Public Key: (n, e) = (n with {n_bits} bits, {e})")
    print(f"Private Key: (d, n) = (d with {d.bit_length()} bits, n with {n_bits} bits)")

    return public_key, private_key, p, q


def rsa_sign(message_bytes, private_key, hash_algorithm):
    d, n = private_key

    print("\n" + "=" * 80)
    print("RSA SIGNATURE GENERATION")
    print("=" * 80)
    print(f"Message: {message_bytes}")


    hash_bytes, hash_decimal, hash_hex = compute_hash(message_bytes, hash_algorithm)


    if hash_decimal >= n:
        print(f"\n⚠️  WARNING: Hash ({hash_decimal}) is larger than modulus ({n})")
        print("Hash must be reduced modulo n for signing.")
        hash_decimal = hash_decimal % n


    print(f"\nStep 2: Sign hash using private key")
    print(f"Signature formula: s = H(m)^d (mod n)")
    print(f"  s = {hash_decimal}^{d} mod {n}")

    signature = pow(hash_decimal, d, n)

    print(f"\nSignature: s = {signature}")

    return signature, hash_decimal


def rsa_verify(message_bytes, signature, public_key, hash_algorithm):
    n, e = public_key

    print("\n" + "=" * 80)
    print("RSA SIGNATURE VERIFICATION")
    print("=" * 80)
    print(f"Message: {message_bytes}")
    print(f"Signature: s = {signature}")


    hash_bytes, hash_decimal, hash_hex = compute_hash(message_bytes, hash_algorithm)


    hash_decimal_mod = hash_decimal % n


    print(f"\nStep 2: Recover hash from signature")
    print(f"Recovery formula: H'(m) = s^e (mod n)")
    print(f"  H'(m) = {signature}^{e} mod {n}")

    recovered_hash = pow(signature, e, n)

    print(f"Recovered hash: H'(m) = {recovered_hash}")
    print(f"Original hash: H(m) = {hash_decimal_mod}")


    print(f"\nStep 3: Compare hashes")
    is_valid = (recovered_hash == hash_decimal_mod)

    if is_valid:
        print("✓ H(m) ≡ H'(m) (mod n)")
        print("✓ Signature is VALID!")
    else:
        print("✗ H(m) ≠ H'(m) (mod n)")
        print("✗ Signature is INVALID!")

    return is_valid, hash_decimal_mod, recovered_hash


def main():
    print("=" * 80)
    print("RSA DIGITAL SIGNATURE IMPLEMENTATION - Lab 6, Task 2")
    print("=" * 80)
    print("Requirements:")
    print("- Generate RSA keys with n >= 3072 bits")
    print("- Sign and validate digital signature of message m from Lab 2")
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


    public_key, private_key, p, q = generate_rsa_keys(key_size_bits=3072)
    n, e = public_key
    d, _ = private_key


    signature, hash_value = rsa_sign(message_bytes, private_key, hash_algorithm)


    is_valid, original_hash, recovered_hash = rsa_verify(
        message_bytes, signature, public_key, hash_algorithm
    )


    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Message: '{message_text}'")
    print(f"Hash Algorithm: {hash_algorithm} (index {hash_index})")
    print(f"Hash (decimal): {hash_value}")
    print(f"Modulus n: {n.bit_length()} bits")
    print(f"Public exponent e: {e}")
    print(f"Signature: {signature}")
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

