#!/usr/bin/env python3

import random
from Crypto.Util.number import GCD, inverse



P = 32317006071311007300153513477825163362488057133489075174588434139269806834136210002792056362640164685458556357935330816928829023080573472625273554742461245741026202527916572972862706300325263428213145766931414223654220941111348629991657478268034230553086349050635557712219187890332729569696129743856241741236237225197346402691855797767976823014625397933058015226858730761197532436467475855460715043896844940366130497697812854295958659597567051283852132784468522925504568272879113720098931873959143374175837826000278034973198552060607533234122603254684088120031105907484281003994966956119696956248629032338072839127039
G = 2


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
    print(f"Verification: 1 < {x} < {p-1} ✓")


    print(f"\nStep 2: Calculate public key y = g^x (mod p)")
    print(f"  y = {g}^{x} mod {p}")

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


def elgamal_encrypt(message_decimal, public_key):
    p, g, y = public_key

    print("\n" + "=" * 80)
    print("ELGAMAL ENCRYPTION")
    print("=" * 80)
    print(f"Message (decimal): m = {message_decimal}")
    print(f"Public key: (p, g, y) = ({p}, {g}, {y})")


    if message_decimal >= p:
        print(f"\n⚠️  WARNING: Message ({message_decimal}) is larger than modulus ({p})")
        print("This will cause incorrect decryption. Message must be < p.")
        return None, None


    print(f"\nStep 1: Choose random secret k such that 1 < k < p-1 and GCD(k, p-1) = 1")


    k_min = 2
    k_max = min(p - 2, 2**256)

    while True:
        k = random.randint(k_min, k_max)
        if GCD(k, p - 1) == 1:
            break

    print(f"  Selected k = {k}")
    print(f"  Verification: GCD({k}, {p-1}) = {GCD(k, p-1)} ✓")


    print(f"\nStep 2: Calculate c1 = g^k (mod p)")
    print(f"  c1 = {g}^{k} mod {p}")
    c1 = pow(g, k, p)
    print(f"  c1 = {c1}")


    print(f"\nStep 3: Calculate c2 = (y^k * m) mod p")
    print(f"  y^k mod p = {y}^{k} mod {p}")
    y_power_k = pow(y, k, p)
    print(f"  y^k mod p = {y_power_k}")
    print(f"  c2 = ({y_power_k} * {message_decimal}) mod {p}")
    c2 = (y_power_k * message_decimal) % p
    print(f"  c2 = {c2}")

    ciphertext = (c1, c2)

    print(f"\nCiphertext: (c1, c2) = ({c1}, {c2})")

    return ciphertext, k


def elgamal_decrypt(ciphertext, private_key):
    c1, c2 = ciphertext
    x, p = private_key

    print("\n" + "=" * 80)
    print("ELGAMAL DECRYPTION")
    print("=" * 80)
    print(f"Ciphertext: (c1, c2) = ({c1}, {c2})")
    print(f"Private key: (x, p) = ({x}, {p})")


    print(f"\nStep 1: Calculate s = c1^x (mod p)")
    print(f"  s = {c1}^{x} mod {p}")
    s = pow(c1, x, p)
    print(f"  s = {s}")


    print(f"\nStep 2: Calculate s_inv = s^(-1) (mod p)")
    print(f"  s_inv = {s}^(-1) mod {p}")
    s_inv = inverse(s, p)
    print(f"  s_inv = {s_inv}")
    print(f"  Verification: (s * s_inv) mod p = {(s * s_inv) % p} ✓")


    print(f"\nStep 3: Calculate m = (c2 * s_inv) mod p")
    print(f"  m = ({c2} * {s_inv}) mod {p}")
    message_decimal = (c2 * s_inv) % p
    print(f"  m = {message_decimal}")

    return message_decimal


def main():
    print("=" * 80)
    print("ELGAMAL ALGORITHM IMPLEMENTATION - Lab 5, Task 2.2")
    print("=" * 80)
    print("Requirements:")
    print("- Generate ElGamal keys with given p (2048-bit) and g=2")
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


    public_key, private_key = generate_elgamal_keys(P, G)
    p, g, y = public_key
    x, _ = private_key


    ciphertext, k = elgamal_encrypt(message_decimal, public_key)

    if ciphertext[0] is None:
        print("\n❌ Encryption failed: Message too large for modulus")
        return

    c1, c2 = ciphertext


    decrypted_decimal = elgamal_decrypt(ciphertext, private_key)


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
    print(f"Prime p: {p} ({p.bit_length()} bits)")
    print(f"Generator g: {g}")
    print(f"Public key y: {y}")
    print(f"Private key x: {x}")
    print(f"Random secret k (used in encryption): {k}")
    print(f"Ciphertext: (c1, c2) = ({c1}, {c2})")
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

