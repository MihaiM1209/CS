#!/usr/bin/env python3

import random
from Crypto.Util.number import getPrime, GCD, inverse
from Crypto.Random import get_random_bytes


def text_to_decimal(text):

    ascii_bytes = text.encode('ascii')


    hex_string = ascii_bytes.hex()


    decimal_value = int(hex_string, 16)

    return decimal_value, hex_string, ascii_bytes


def decimal_to_text(decimal_value):

    hex_string = hex(decimal_value)[2:]


    if len(hex_string) % 2 != 0:
        hex_string = '0' + hex_string


    ascii_bytes = bytes.fromhex(hex_string)


    text = ascii_bytes.decode('ascii')

    return text, hex_string


def generate_rsa_keys(key_size_bits=2048):
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
    print(f"p = {p}")
    print(f"q = {q}")


    n = p * q
    n_bits = n.bit_length()
    print(f"\nStep 2: Calculate n = p * q")
    print(f"n = {n}")
    print(f"n has {n_bits} bits {'✓' if n_bits >= key_size_bits else '✗'}")

    if n_bits < key_size_bits:
        print(f"Warning: n has only {n_bits} bits, but requirement is at least {key_size_bits} bits")


    phi_n = (p - 1) * (q - 1)
    print(f"\nStep 3: Calculate φ(n) = (p-1) * (q-1)")
    print(f"φ(n) = {phi_n}")



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
    print(f"GCD({e}, {phi_n}) = {GCD(e, phi_n)} ✓")



    print(f"\nStep 5: Calculate private exponent d such that e * d ≡ 1 (mod φ(n))")
    d = inverse(e, phi_n)
    print(f"d = {d}")
    print(f"Verification: (e * d) mod φ(n) = {(e * d) % phi_n} ✓")

    public_key = (n, e)
    private_key = (d, n)

    print("\n" + "=" * 80)
    print("GENERATED KEYS")
    print("=" * 80)
    print(f"Public Key: (n, e) = ({n}, {e})")
    print(f"Private Key: (d, n) = ({d}, {n})")

    return public_key, private_key, p, q


def rsa_encrypt(message_decimal, public_key):
    n, e = public_key

    print("\n" + "=" * 80)
    print("RSA ENCRYPTION")
    print("=" * 80)
    print(f"Message (decimal): m = {message_decimal}")
    print(f"Public key: (n, e) = ({n}, {e})")
    print(f"\nEncryption formula: c = m^e (mod n)")


    if message_decimal >= n:
        print(f"\n⚠️  WARNING: Message ({message_decimal}) is larger than modulus ({n})")
        print("This will cause incorrect decryption. Message must be < n.")
        return None


    ciphertext = pow(message_decimal, e, n)

    print(f"\nCalculation:")
    print(f"  c = {message_decimal}^{e} mod {n}")
    print(f"  c = {ciphertext}")

    return ciphertext


def rsa_decrypt(ciphertext, private_key):
    d, n = private_key

    print("\n" + "=" * 80)
    print("RSA DECRYPTION")
    print("=" * 80)
    print(f"Ciphertext: c = {ciphertext}")
    print(f"Private key: (d, n) = ({d}, {n})")
    print(f"\nDecryption formula: m = c^d (mod n)")


    message_decimal = pow(ciphertext, d, n)

    print(f"\nCalculation:")
    print(f"  m = {ciphertext}^{d} mod {n}")
    print(f"  m = {message_decimal}")

    return message_decimal


def main():
    print("=" * 80)
    print("RSA ALGORITHM IMPLEMENTATION - Lab 5, Task 2.1")
    print("=" * 80)
    print("Requirements:")
    print("- Generate RSA keys with n >= 2048 bits")
    print("- Encrypt and decrypt message: m = 'Nume Prenume'")
    print("- Message encoding: ASCII → Hexadecimal → Decimal")


    message_text = "Nume Prenume"

    print(f"\nOriginal message: '{message_text}'")


    print("\n" + "=" * 80)
    print("MESSAGE ENCODING (ASCII → Hex → Decimal)")
    print("=" * 80)
    message_decimal, hex_string, ascii_bytes = text_to_decimal(message_text)

    print(f"Step 1: ASCII encoding")
    print(f"  ASCII bytes: {ascii_bytes}")
    print(f"  ASCII values: {[b for b in ascii_bytes]}")

    print(f"\nStep 2: Hexadecimal representation")
    print(f"  Hex string: {hex_string}")

    print(f"\nStep 3: Decimal representation")
    print(f"  Decimal value: {message_decimal}")


    public_key, private_key, p, q = generate_rsa_keys(key_size_bits=2048)
    n, e = public_key
    d, _ = private_key


    ciphertext = rsa_encrypt(message_decimal, public_key)

    if ciphertext is None:
        print("\n❌ Encryption failed: Message too large for modulus")
        return


    decrypted_decimal = rsa_decrypt(ciphertext, private_key)


    print("\n" + "=" * 80)
    print("MESSAGE DECODING (Decimal → Hex → ASCII)")
    print("=" * 80)
    decrypted_text, decrypted_hex = decimal_to_text(decrypted_decimal)

    print(f"Step 1: Decimal to hexadecimal")
    print(f"  Decimal value: {decrypted_decimal}")
    print(f"  Hex string: {decrypted_hex}")

    print(f"\nStep 2: Hexadecimal to ASCII bytes")
    print(f"  ASCII bytes: {bytes.fromhex(decrypted_hex)}")

    print(f"\nStep 3: ASCII decoding to text")
    print(f"  Decrypted text: '{decrypted_text}'")


    print("\n" + "=" * 80)
    print("VERIFICATION")
    print("=" * 80)
    print(f"Original message: '{message_text}'")
    print(f"Decrypted message: '{decrypted_text}'")

    if message_text == decrypted_text:
        print("✓ Decryption successful! Messages match.")
    else:
        print("✗ Decryption failed! Messages do not match.")


    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Message: '{message_text}'")
    print(f"Message (decimal): {message_decimal}")
    print(f"Modulus n: {n} ({n.bit_length()} bits)")
    print(f"Public exponent e: {e}")
    print(f"Private exponent d: {d}")
    print(f"Ciphertext: {ciphertext}")
    print(f"Decrypted message: '{decrypted_text}'")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()

