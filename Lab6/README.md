# Lab 6 - Digital Signatures

This laboratory implements two fundamental digital signature algorithms: RSA and ElGamal. Digital signatures provide authentication, integrity, and non-repudiation for digital messages. Each task demonstrates key generation, signature creation, and signature verification processes with detailed step-by-step explanations.

## 📋 Table of Contents

1. [Requirements](#requirements)
2. [Task 2: RSA Digital Signature](#task-2-rsa-digital-signature)
3. [Task 3: ElGamal Digital Signature](#task-3-elgamal-digital-signature)
4. [Hash Algorithm Selection](#hash-algorithm-selection)
5. [Installation](#installation)
6. [Usage](#usage)

---

## Requirements

### Python Dependencies
```bash
pip install -r requirements.txt
```

Or directly:
```bash
pip install pycryptodome
```

### Common Parameters
- **Message**: Message `m` from Lab 2 (used for signing and verification)
- **Hash Representation**: Decimal numerical representation of hash value
- **Key Size**: 3072 bits minimum for RSA (Task 2), 2048-bit prime modulus for ElGamal (Task 3)
- **Hash Selection**: Based on formula `i = (k mod 24) + 1`, where `k` is student's order number

---

## Task 2: RSA Digital Signature

### 1. Theory Explanation

**RSA Digital Signature** is a digital signature scheme based on the RSA cryptosystem. It provides authentication, integrity, and non-repudiation for digital messages.

#### How RSA Digital Signatures Work:

**Key Generation:**
Same as RSA encryption:
1. Generate two large prime numbers `p` and `q`
2. Calculate modulus `n = p × q` (must be ≥ 3072 bits for this task)
3. Calculate Euler's totient `φ(n) = (p-1) × (q-1)`
4. Choose public exponent `e` such that `GCD(e, φ(n)) = 1`
5. Calculate private exponent `d` where `e × d ≡ 1 (mod φ(n))`

**Public Key**: `(n, e)` - used for verification  
**Private Key**: `(d, n)` - used for signing (must be kept secret)

**Signing Process:**
1. Compute hash `H(m)` of the message using a cryptographic hash function
2. Sign the hash: `s = H(m)^d (mod n)`

The signature `s` proves that the message was signed by the holder of the private key.

**Verification Process:**
1. Compute hash `H(m)` of the original message
2. Recover hash from signature: `H'(m) = s^e (mod n)`
3. Compare: If `H(m) ≡ H'(m) (mod n)`, the signature is valid

**Mathematical Proof:**
```
Signature: s = H(m)^d mod n
Verification: H'(m) = s^e mod n
             = (H(m)^d)^e mod n
             = H(m)^(de) mod n
             = H(m)^1 mod n  (since e*d ≡ 1 mod φ(n))
             = H(m) mod n ✓
```

**Security:**
- **Authentication**: Verifier can confirm the message came from the signer
- **Integrity**: Any modification to the message invalidates the signature
- **Non-repudiation**: Signer cannot deny signing (only they have private key `d`)
- **Hash Function**: Ensures signatures work for messages of any length

**Important**: RSA signatures typically sign the **hash** of the message, not the message itself. This is because:
- Messages can be larger than the modulus
- Signing a hash is computationally efficient
- Hash functions provide fixed-size output

### 2. Important Functions

#### Function 1: Key Generation

```python
def generate_rsa_keys(key_size_bits=3072):
    """
    Generate RSA public and private keys.
    
    Algorithm steps:
    1. Generate two large prime numbers p and q such that n = p * q >= 2^(key_size_bits-1)
    2. Calculate n = p * q (modulus, part of public key)
    3. Calculate φ(n) = (p-1) * (q-1) (Euler's totient function)
    4. Choose e such that 1 < e < φ(n) and GCD(e, φ(n)) = 1 (public exponent)
    5. Calculate d such that e * d ≡ 1 (mod φ(n)) (private exponent)
    """
    # Step 1: Generate two large prime numbers
    p_bits = key_size_bits // 2
    q_bits = key_size_bits - p_bits
    p = getPrime(p_bits)
    q = getPrime(q_bits)
    
    # Step 2: Calculate modulus n
    n = p * q
    
    # Step 3: Calculate Euler's totient function
    phi_n = (p - 1) * (q - 1)
    
    # Step 4: Choose public exponent e
    e_candidates = [65537, 3, 17, 257]
    e = None
    for candidate in e_candidates:
        if candidate < phi_n and GCD(candidate, phi_n) == 1:
            e = candidate
            break
    
    # Step 5: Calculate private exponent d
    d = inverse(e, phi_n)
    
    public_key = (n, e)
    private_key = (d, n)
    return public_key, private_key, p, q
```

#### Function 2: Hash Computation

```python
def compute_hash(message_bytes, hash_algorithm):
    """
    Compute hash of message using specified hash algorithm.
    
    Returns hash as bytes, decimal integer, and hexadecimal string.
    """
    # Map hash algorithm names to hashlib functions
    hash_functions = {
        "SHA-1": hashlib.sha1,
        "SHA-256": hashlib.sha256,
        "SHA-512": hashlib.sha512,
        "MD5": hashlib.md5,
        # ... other hash algorithms
    }
    
    hash_func = hash_functions[hash_algorithm]
    h = hash_func()
    h.update(message_bytes)
    hash_bytes = h.digest()
    
    # Convert to hexadecimal and decimal
    hash_hex = hash_bytes.hex()
    hash_decimal = int(hash_hex, 16)
    
    return hash_bytes, hash_decimal, hash_hex
```

#### Function 3: Signature Generation

```python
def rsa_sign(message_bytes, private_key, hash_algorithm):
    """
    Sign a message using RSA private key.
    
    Algorithm:
    1. Compute hash H(m) of the message
    2. Sign the hash: s = H(m)^d (mod n)
    """
    d, n = private_key
    
    # Step 1: Compute hash
    hash_bytes, hash_decimal, hash_hex = compute_hash(message_bytes, hash_algorithm)
    
    # Reduce hash modulo n if needed
    if hash_decimal >= n:
        hash_decimal = hash_decimal % n
    
    # Step 2: Sign the hash: s = H(m)^d (mod n)
    signature = pow(hash_decimal, d, n)
    
    return signature, hash_decimal
```

#### Function 4: Signature Verification

```python
def rsa_verify(message_bytes, signature, public_key, hash_algorithm):
    """
    Verify RSA digital signature.
    
    Algorithm:
    1. Compute hash H(m) of the message
    2. Recover hash from signature: H'(m) = s^e (mod n)
    3. Compare: if H(m) ≡ H'(m) (mod n), signature is valid
    """
    n, e = public_key
    
    # Step 1: Compute hash of original message
    hash_bytes, hash_decimal, hash_hex = compute_hash(message_bytes, hash_algorithm)
    hash_decimal_mod = hash_decimal % n
    
    # Step 2: Recover hash from signature
    recovered_hash = pow(signature, e, n)
    
    # Step 3: Compare
    is_valid = (recovered_hash == hash_decimal_mod)
    
    return is_valid, hash_decimal_mod, recovered_hash
```

### 3. Function Descriptions

#### `generate_rsa_keys(key_size_bits=3072)`

**Purpose**: Generates RSA key pair for digital signatures.

**Algorithm Breakdown:**
1. **Prime Generation**: Generates two large primes `p` and `q`, each approximately half the key size
2. **Modulus Calculation**: Computes `n = p × q` (must be ≥ 3072 bits for this task)
3. **Euler's Totient**: Calculates `φ(n) = (p-1) × (q-1)`
4. **Public Exponent**: Selects `e` (typically 65537) that is coprime with `φ(n)`
5. **Private Exponent**: Computes `d` as modular inverse of `e` modulo `φ(n)`

**Key Difference from Encryption**: Same key generation process, but keys are used differently:
- **Encryption**: Public key encrypts, private key decrypts
- **Signatures**: Private key signs, public key verifies

**Returns:**
- `public_key`: Tuple `(n, e)` - shared publicly for verification
- `private_key`: Tuple `(d, n)` - kept secret for signing

**Security Note**: 3072-bit keys provide stronger security than 2048-bit keys, recommended for long-term security.

---

#### `compute_hash(message_bytes, hash_algorithm)`

**Purpose**: Computes cryptographic hash of a message using specified hash algorithm.

**Algorithm Selection**: Based on formula `i = (k mod 24) + 1`, where `k` is student's order number in group.

**Supported Hash Algorithms**:
- MD family: MD4, MD5, MD2, MD6-128/256/512
- SHA family: SHA-1, SHA-224, SHA-256, SHA-384, SHA-512
- SHA-3 family: SHA3-224, SHA3-256, SHA3-384, SHA3-512
- RipeMD family: RipeMD-128, RipeMD-160, RipeMD-256, RipeMD-320
- Others: Whirlpool, NTLM, Haval variants

**Process:**
1. Maps algorithm name to hashlib function
2. Computes hash digest of message bytes
3. Converts to hexadecimal string
4. Converts to decimal integer (as required)

**Returns:**
- `hash_bytes`: Raw hash as bytes
- `hash_decimal`: Hash as decimal integer (for signing)
- `hash_hex`: Hash as hexadecimal string

**Why Hash?**: 
- Messages can be arbitrarily long, but hash is fixed size
- Hash provides integrity - any change to message changes hash
- Signing hash is more efficient than signing entire message

---

#### `rsa_sign(message_bytes, private_key, hash_algorithm)`

**Purpose**: Creates RSA digital signature for a message.

**Mathematical Formula**: `s = H(m)^d (mod n)`

**Algorithm Steps:**
1. **Hash Computation**: Computes `H(m)` using specified hash algorithm
2. **Hash Reduction**: Reduces hash modulo `n` if hash ≥ modulus
3. **Signature Creation**: Signs hash using private exponent: `s = H(m)^d mod n`

**Parameters:**
- `message_bytes`: Message as bytes
- `private_key`: Tuple `(d, n)` containing private exponent and modulus
- `hash_algorithm`: Name of hash algorithm to use

**Process:**
1. Computes hash of message (returns decimal representation)
2. Ensures hash < modulus `n` (reduces modulo `n` if needed)
3. Signs hash using private key: `signature = pow(hash_decimal, d, n)`

**Returns:**
- `signature`: Digital signature (integer)
- `hash_decimal`: Hash value used for signing

**Important**: Only the holder of private key `d` can create a valid signature. The signature proves authenticity and integrity of the message.

**Security Properties**:
- **Authentication**: Verifier knows message came from signer
- **Integrity**: Any modification invalidates signature
- **Non-repudiation**: Signer cannot deny signing

---

#### `rsa_verify(message_bytes, signature, public_key, hash_algorithm)`

**Purpose**: Verifies RSA digital signature.

**Mathematical Formula**: `H'(m) = s^e (mod n)`, then check `H(m) ≡ H'(m) (mod n)`

**Algorithm Steps:**
1. **Hash Computation**: Computes `H(m)` of original message
2. **Hash Recovery**: Recovers hash from signature: `H'(m) = s^e mod n`
3. **Comparison**: Checks if `H(m) ≡ H'(m) (mod n)`

**Mathematical Proof**:
```
H'(m) = s^e mod n
      = (H(m)^d)^e mod n
      = H(m)^(de) mod n
      = H(m)^1 mod n  (since e*d ≡ 1 mod φ(n))
      = H(m) mod n ✓
```

**Parameters:**
- `message_bytes`: Original message as bytes
- `signature`: Digital signature to verify
- `public_key`: Tuple `(n, e)` containing modulus and public exponent
- `hash_algorithm`: Hash algorithm name (must match signing)

**Process:**
1. Computes hash `H(m)` of original message using same hash algorithm
2. Recovers hash from signature using public exponent: `recovered_hash = pow(signature, e, n)`
3. Compares recovered hash with computed hash

**Returns:**
- `is_valid`: Boolean - True if signature is valid, False otherwise
- `hash_decimal_mod`: Computed hash modulo n
- `recovered_hash`: Hash recovered from signature

**Verification Logic**:
- If `H(m) ≡ H'(m) (mod n)`: Signature is **VALID** ✓
- If `H(m) ≠ H'(m) (mod n)`: Signature is **INVALID** ✗

**Security**: Verification uses only public key, so anyone can verify signatures. Only the signer (with private key) can create valid signatures.

---

## Task 3: ElGamal Digital Signature

### 1. Theory Explanation

**ElGamal Digital Signature** is a digital signature scheme based on the discrete logarithm problem. It was invented by Taher ElGamal in 1984 and provides authentication and integrity for digital messages.

#### How ElGamal Digital Signatures Work:

**Key Generation:**
1. Choose a large prime `p` and a generator `g` (primitive root modulo `p`)
2. Choose a private key `x` randomly such that `1 < x < p-1`
3. Calculate public key `y = g^x (mod p)`

**Public Key**: `(p, g, y)` - used for verification  
**Private Key**: `(x, p)` - used for signing (must be kept secret)

**Signing Process:**
1. Compute hash `H(m)` of the message
2. Choose random `k` such that `1 < k < p-1` and `GCD(k, p-1) = 1`
3. Calculate `r = g^k (mod p)`
4. Calculate `s = k^(-1) × (H(m) - x×r) (mod (p-1))`

**Signature**: `(r, s)` - a pair of integers

**Verification Process:**
1. Compute hash `H(m)` of the original message
2. Verify: `g^H(m) ≡ y^r × r^s (mod p)`

If this congruence holds, the signature is valid.

**Mathematical Proof**:
```
During signing:
  r = g^k mod p
  s = k^(-1) * (H(m) - x*r) mod (p-1)

During verification:
  Left side: g^H(m) mod p
  Right side: y^r * r^s mod p
             = (g^x)^r * (g^k)^s mod p
             = g^(xr) * g^(ks) mod p
             = g^(xr + ks) mod p

Since: s = k^(-1) * (H(m) - x*r) mod (p-1)
We get: ks = H(m) - x*r mod (p-1)
So: xr + ks = xr + (H(m) - x*r) = H(m) mod (p-1)

Therefore: y^r * r^s = g^H(m) mod p ✓
```

**Security:**
- Based on discrete logarithm problem: finding `x` from `y = g^x mod p` is hard
- Each signature uses fresh random `k`, providing security
- Hash function ensures signatures work for messages of any length

**Key Advantages:**
- Probabilistic signatures (different signatures for same message)
- Security based on well-studied discrete logarithm problem
- Widely used in practice

### 2. Important Functions

#### Function 1: Key Generation

```python
def generate_elgamal_keys(p, g):
    """
    Generate ElGamal key pair for digital signatures.
    
    Algorithm steps:
    1. Choose a private key x such that 1 < x < p-1
    2. Calculate public key y = g^x (mod p)
    """
    # Step 1: Choose private key x
    x_min = 2
    x_max = min(p - 2, 2**256)  # Limit to 256 bits for computation
    x = random.randint(x_min, x_max)
    
    # Step 2: Calculate public key y = g^x (mod p)
    y = pow(g, x, p)
    
    public_key = (p, g, y)
    private_key = (x, p)
    return public_key, private_key
```

#### Function 2: Signature Generation

```python
def elgamal_sign(message_bytes, private_key, hash_algorithm):
    """
    Sign a message using ElGamal digital signature.
    
    Algorithm:
    1. Compute hash H(m) of the message
    2. Choose random k such that 1 < k < p-1 and GCD(k, p-1) = 1
    3. Calculate r = g^k (mod p)
    4. Calculate s = k^(-1) * (H(m) - x*r) (mod (p-1))
    """
    x, p = private_key
    
    # Step 1: Compute hash
    hash_bytes, hash_decimal, hash_hex = compute_hash(message_bytes, hash_algorithm)
    hash_mod = hash_decimal % (p - 1)
    
    # Step 2: Choose random k
    while True:
        k = random.randint(2, min(p - 2, 2**256))
        if GCD(k, p - 1) == 1:
            break
    
    # Step 3: Calculate r = g^k (mod p)
    r = pow(G, k, p)
    
    # Step 4: Calculate s
    k_inv = inverse(k, p - 1)
    temp = (hash_mod - x * r) % (p - 1)
    s = (k_inv * temp) % (p - 1)
    
    signature = (r, s)
    return signature, hash_mod, k
```

#### Function 3: Signature Verification

```python
def elgamal_verify(message_bytes, signature, public_key, hash_algorithm):
    """
    Verify ElGamal digital signature.
    
    Algorithm:
    1. Compute hash H(m) of the message
    2. Verify: g^H(m) ≡ y^r * r^s (mod p)
    """
    r, s = signature
    p, g, y = public_key
    
    # Step 1: Compute hash
    hash_bytes, hash_decimal, hash_hex = compute_hash(message_bytes, hash_algorithm)
    hash_mod = hash_decimal % (p - 1)
    
    # Step 2: Verify: g^H(m) ≡ y^r * r^s (mod p)
    left_side = pow(g, hash_mod, p)
    y_power_r = pow(y, r, p)
    r_power_s = pow(r, s, p)
    right_side = (y_power_r * r_power_s) % p
    
    is_valid = (left_side == right_side)
    
    return is_valid, left_side, right_side
```

### 3. Function Descriptions

#### `generate_elgamal_keys(p, g)`

**Purpose**: Generates ElGamal key pair for digital signatures.

**Algorithm Breakdown:**
1. **Private Key Selection**: Randomly chooses `x` from range `[2, min(p-2, 2^256)]`
   - Range limited for computational efficiency while maintaining security
2. **Public Key Calculation**: Computes `y = g^x mod p` using modular exponentiation

**Parameters:**
- `p`: Large prime modulus (2048 bits, as given)
- `g`: Generator/base (2, as given)

**Returns:**
- `public_key`: Tuple `(p, g, y)` - all values are public
- `private_key`: Tuple `(x, p)` - `x` must remain secret

**Key Insight**: The public key `y` can be computed from private key `x`, but finding `x` from `y` requires solving the discrete logarithm problem, which is computationally infeasible for large `p`.

---

#### `elgamal_sign(message_bytes, private_key, hash_algorithm)`

**Purpose**: Creates ElGamal digital signature for a message.

**Mathematical Formulas:**
- `r = g^k (mod p)` - ephemeral public key
- `s = k^(-1) × (H(m) - x×r) (mod (p-1))` - signature component

**Algorithm Steps:**
1. **Hash Computation**: Computes `H(m)` and reduces modulo `(p-1)`
2. **Random Secret**: Chooses random `k` with `GCD(k, p-1) = 1`
3. **First Component**: Calculates `r = g^k mod p`
4. **Second Component**: Calculates `s = k^(-1) × (H(m) - x×r) mod (p-1)`

**Parameters:**
- `message_bytes`: Message as bytes
- `private_key`: Tuple `(x, p)` containing private key and modulus
- `hash_algorithm`: Hash algorithm name

**Process:**
1. Computes hash `H(m)` and reduces modulo `(p-1)`
2. Chooses random `k` that is coprime with `(p-1)`
3. Calculates `r = g^k mod p` (first signature component)
4. Finds modular inverse `k^(-1) mod (p-1)`
5. Calculates `s = k^(-1) × (H(m) - x×r) mod (p-1)` (second signature component)

**Returns:**
- `signature`: Tuple `(r, s)` - digital signature
- `hash_mod`: Hash value modulo (p-1)
- `k`: Random secret used (for reference)

**Probabilistic Nature**: Each signature uses a fresh random `k`, so signing the same message twice produces different signatures `(r, s)`. This provides security against certain attacks.

**Security**: The random `k` must be kept secret and never reused. Reusing `k` allows attackers to recover the private key `x`.

---

#### `elgamal_verify(message_bytes, signature, public_key, hash_algorithm)`

**Purpose**: Verifies ElGamal digital signature.

**Mathematical Formula**: `g^H(m) ≡ y^r × r^s (mod p)`

**Algorithm Steps:**
1. **Hash Computation**: Computes `H(m)` and reduces modulo `(p-1)`
2. **Left Side Calculation**: Computes `g^H(m) mod p`
3. **Right Side Calculation**: Computes `y^r × r^s mod p`
4. **Comparison**: Checks if left side equals right side

**Mathematical Proof**:
```
Left side: g^H(m) mod p

Right side: y^r * r^s mod p
           = (g^x)^r * (g^k)^s mod p
           = g^(xr) * g^(ks) mod p
           = g^(xr + ks) mod p

From signing: s = k^(-1) * (H(m) - x*r) mod (p-1)
Therefore: ks = H(m) - x*r mod (p-1)
So: xr + ks = H(m) mod (p-1)

By Fermat's little theorem: g^(xr + ks) ≡ g^H(m) mod p ✓
```

**Parameters:**
- `message_bytes`: Original message as bytes
- `signature`: Tuple `(r, s)` to verify
- `public_key`: Tuple `(p, g, y)` containing public parameters
- `hash_algorithm`: Hash algorithm name (must match signing)

**Process:**
1. Computes hash `H(m)` of original message and reduces modulo `(p-1)`
2. Calculates left side: `left_side = pow(g, hash_mod, p)`
3. Calculates right side components:
   - `y_power_r = pow(y, r, p)`
   - `r_power_s = pow(r, s, p)`
   - `right_side = (y_power_r * r_power_s) % p`
4. Compares left and right sides

**Returns:**
- `is_valid`: Boolean - True if signature is valid, False otherwise
- `left_side`: Computed value `g^H(m) mod p`
- `right_side`: Computed value `y^r × r^s mod p`

**Verification Logic**:
- If `g^H(m) ≡ y^r × r^s (mod p)`: Signature is **VALID** ✓
- If `g^H(m) ≠ y^r × r^s (mod p)`: Signature is **INVALID** ✗

**Security**: Verification uses only public key, so anyone can verify signatures. The security relies on the discrete logarithm problem and the random secret `k` used during signing.

---

## Hash Algorithm Selection

Both tasks use hash algorithm selection based on the formula:

**Formula**: `i = (k mod 24) + 1`

Where:
- `k` = Student's order number in group list
- `i` = Index of hash function in list (1-24)

### Hash Algorithm Lists

**Task 2 (RSA) Hash Algorithms:**
1. MD4, 2. MD5, 3. MD2, 4. MD6-128, 5. MD6-256, 6. MD6-512,
7. SHA-1, 8. SHA-224, 9. SHA-256, 10. SHA-384, 11. SHA-512,
12. SHA3-224, 13. SHA3-256, 14. SHA3-384, 15. SHA3-512,
16. RipeMD-128, 17. RipeMD-160, 18. RipeMD-256, 19. RipeMD-320,
20. Whirlpool, 21. NTLM, 22. Haval192,3, 23. Haval224,4, 24. Haval256,4

**Task 3 (ElGamal) Hash Algorithms:**
1. NTLM, 2. MD4, 3. MD5, 4. MD2, 5. MD6-128, 6. MD6-256, 7. MD6-512,
8. SHA-1, 9. SHA-224, 10. SHA-256, 11. SHA-384, 12. SHA-512,
13. SHA3-224, 14. SHA3-256, 15. SHA3-384, 16. SHA3-512,
17. RipeMD-128, 18. RipeMD-160, 19. RipeMD-256, 20. RipeMD-320,
21. Whirlpool, 22. Haval192,3, 23. Haval224,4, 24. Haval256,4

**Note**: Lists differ slightly (NTLM is first in Task 3, second-to-last in Task 2).

### Hash Value Representation

As per requirements, hash values must be represented in **decimal** numerical format:
- Hash is computed as bytes
- Converted to hexadecimal string
- Converted to decimal integer for use in signature algorithms

This decimal representation is used throughout the signing and verification processes.

---

## Installation

1. **Navigate to the project:**
   ```bash
   cd Lab6
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   python3 -c "from Crypto.Util.number import getPrime; print('OK')"
   ```

---

## Usage

### Task 2: RSA Digital Signature
```bash
python3 Task2.py
```

**Expected Output:**
- Hash algorithm selection (based on student number)
- Key generation steps (n ≥ 3072 bits)
- Hash computation of message
- Signature generation process
- Signature verification process
- Verification result

**Interactive Input:**
- Student number `k` for hash algorithm selection

### Task 3: ElGamal Digital Signature
```bash
python3 Task3.py
```

**Expected Output:**
- Hash algorithm selection (based on student number)
- Key generation (using given p and g=2)
- Hash computation of message
- Signature generation process (r, s)
- Signature verification process
- Verification result

**Interactive Input:**
- Student number `k` for hash algorithm selection

---

## Common Parameters

**Task 3 uses given parameters:**

```python
P = 32317006071311007300153513477825163362488057133489075174588434139269806834136210002792056362640164685458556357935330816928829023080573472625273554742461245741026202527916572972862706300325263428213145766931414223654220941111348629991657478268034230553086349050635557712219187890332729569696129743856241741236237225197346402691855797767976823014625397933058015226858730761197532436467475855460715043896844940366130497697812854295958659597567051283852132784468522925504568272879113720098931873959143374175837826000278034973198552060607533234122603254684088120031105907484281003994966956119696956248629032338072839127039
G = 2
```

- **P**: 2048-bit prime number (modulus)
- **G**: Generator (base) = 2

---

## Algorithm Comparison

| Feature | RSA Digital Signature | ElGamal Digital Signature |
|---------|----------------------|---------------------------|
| **Signature Size** | Single integer | Two integers (r, s) |
| **Probabilistic?** | No (deterministic) | Yes (random k each time) |
| **Key Size** | 3072+ bits (Task 2) | 2048-bit prime p |
| **Security Basis** | Integer factorization | Discrete logarithm |
| **Computation** | Moderate | Moderate |
| **Hash Requirement** | Yes | Yes |

---

## Security Notes

1. **Key Sizes**: RSA uses 3072+ bit keys for enhanced security; ElGamal uses 2048-bit prime
2. **Hash Functions**: Always use cryptographically secure hash functions
3. **Random Secrets**: ElGamal requires fresh random `k` for each signature
4. **Hash Representation**: Decimal representation used as per requirements
5. **Message Source**: Message `m` should be from Lab 2 as specified

---

## References

- **RSA**: Rivest, Shamir, Adleman (1978) - "A Method for Obtaining Digital Signatures"
- **ElGamal**: Taher ElGamal (1984) - "A Public Key Cryptosystem and a Signature Scheme Based on Discrete Logarithms"
- **PKCS#1**: RSA Cryptography Specifications

---

## Troubleshooting

**Import Error: `No module named 'Crypto'`**
```bash
pip install pycryptodome
```

**Hash Algorithm Not Supported**
- Some hash algorithms may not be available in all Python environments
- The code falls back to SHA-256 if an algorithm is unavailable
- Check Python's hashlib documentation for supported algorithms

**Large Number Computation Takes Time**
- RSA with 3072-bit keys requires significant computation
- This is normal and demonstrates real-world cryptographic operations
- ElGamal also involves large modular exponentiations

**Hash Selection Issues**
- Ensure student number `k` is entered correctly
- Formula: `i = (k mod 24) + 1`
- Index `i` selects from the appropriate list (Task 2 or Task 3)

---

## License

This is an educational implementation for learning purposes. Do not use in production systems without security audit.

