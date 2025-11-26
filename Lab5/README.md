# Lab 5 - Public Key Cryptography

This laboratory implements three fundamental public key cryptographic algorithms used in modern secure communications. Each task demonstrates key generation, encryption, and decryption processes with detailed step-by-step explanations.

## 📋 Table of Contents

1. [Requirements](#requirements)
2. [Task 2.1: RSA Algorithm](#task-21-rsa-algorithm)
3. [Task 2.2: ElGamal Algorithm](#task-22-elgamal-algorithm)
4. [Task 3: Diffie-Hellman Key Exchange + AES](#task-3-diffie-hellman-key-exchange--aes)
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
- **Message**: `"Nume Prenume"` (encrypted/decrypted in all tasks)
- **Message Encoding**: ASCII → Hexadecimal → Decimal
- **Key Size**: 2048 bits minimum (RSA), 2048-bit prime modulus (ElGamal, DH)

---

## Task 2.1: RSA Algorithm

### 1. Theory Explanation

**RSA (Rivest-Shamir-Adleman)** is one of the first and most widely used public-key cryptosystems. It was invented in 1977 and is based on the mathematical difficulty of factoring the product of two large prime numbers.

#### How RSA Works:

**Key Generation:**
1. Generate two large prime numbers `p` and `q`
2. Calculate modulus `n = p × q`
3. Calculate Euler's totient function `φ(n) = (p-1) × (q-1)`
4. Choose public exponent `e` such that `1 < e < φ(n)` and `GCD(e, φ(n)) = 1`
5. Calculate private exponent `d` as the modular inverse: `e × d ≡ 1 (mod φ(n))`

**Public Key**: `(n, e)` - can be shared publicly  
**Private Key**: `(d, n)` - must be kept secret

**Encryption:**
- Formula: `c = m^e (mod n)`
- Where `m` is the plaintext message and `c` is the ciphertext

**Decryption:**
- Formula: `m = c^d (mod n)`
- Only the holder of the private key `d` can decrypt

**Security:** RSA security relies on the difficulty of factoring large integers. If an attacker can factor `n` into `p` and `q`, they can compute `φ(n)` and find `d`, breaking the encryption.

### 2. Important Functions

#### Function 1: Key Generation

```python
def generate_rsa_keys(key_size_bits=2048):
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

#### Function 2: Encryption

```python
def rsa_encrypt(message_decimal, public_key):
    """
    Encrypt a message using RSA public key.
    
    Encryption formula: c = m^e (mod n)
    """
    n, e = public_key
    
    # Check if message is smaller than modulus
    if message_decimal >= n:
        return None
    
    # Perform encryption: c = m^e mod n
    ciphertext = pow(message_decimal, e, n)
    return ciphertext
```

#### Function 3: Decryption

```python
def rsa_decrypt(ciphertext, private_key):
    """
    Decrypt a ciphertext using RSA private key.
    
    Decryption formula: m = c^d (mod n)
    """
    d, n = private_key
    
    # Perform decryption: m = c^d mod n
    message_decimal = pow(ciphertext, d, n)
    return message_decimal
```

#### Function 4: Message Encoding

```python
def text_to_decimal(text):
    """
    Convert text to decimal representation via ASCII encoding.
    Steps: Text → ASCII bytes → Hexadecimal → Decimal
    """
    # Step 1: Convert to ASCII bytes
    ascii_bytes = text.encode('ascii')
    
    # Step 2: Convert to hexadecimal string
    hex_string = ascii_bytes.hex()
    
    # Step 3: Convert hexadecimal to decimal
    decimal_value = int(hex_string, 16)
    
    return decimal_value, hex_string, ascii_bytes
```

### 3. Function Descriptions

#### `generate_rsa_keys(key_size_bits=2048)`

**Purpose**: Generates a complete RSA key pair following the RSA algorithm.

**Algorithm Breakdown:**
1. **Prime Generation**: Uses `getPrime()` to generate two large primes `p` and `q`, each approximately half the key size to ensure `n = p × q` is at least `key_size_bits` long.
2. **Modulus Calculation**: Multiplies the primes to get `n`, which is part of both public and private keys.
3. **Euler's Totient**: Calculates `φ(n) = (p-1) × (q-1)`, needed for key generation.
4. **Public Exponent Selection**: Tries common values (65537, 3, 17, 257) that are coprime with `φ(n)`. 65537 is preferred for efficiency.
5. **Private Exponent Calculation**: Uses modular multiplicative inverse to find `d` such that `e × d ≡ 1 (mod φ(n))`.

**Returns:**
- `public_key`: Tuple `(n, e)` - shared publicly
- `private_key`: Tuple `(d, n)` - kept secret
- `p, q`: Original primes (for verification)

**Security Note**: The security depends on keeping `p`, `q`, and `d` secret. If `n` is factored, the entire system is compromised.

---

#### `rsa_encrypt(message_decimal, public_key)`

**Purpose**: Encrypts a message using RSA public key encryption.

**Mathematical Formula**: `c = m^e (mod n)`

**Parameters:**
- `message_decimal`: Plaintext as a decimal integer (must be < n)
- `public_key`: Tuple `(n, e)` containing modulus and public exponent

**Process:**
1. Validates that message is smaller than modulus `n`
2. Uses modular exponentiation `pow(m, e, n)` for efficient computation
3. Returns encrypted ciphertext as an integer

**Important**: The message must be smaller than `n`. For longer messages, use hybrid encryption (encrypt a symmetric key with RSA, then use symmetric encryption for the message).

---

#### `rsa_decrypt(ciphertext, private_key)`

**Purpose**: Decrypts RSA ciphertext using the private key.

**Mathematical Formula**: `m = c^d (mod n)`

**Mathematical Proof**: 
```
c^d = (m^e)^d = m^(ed) = m^1 = m (mod n)
```
This works because during key generation: `e × d ≡ 1 (mod φ(n))`, so `m^(ed) ≡ m^1 ≡ m (mod n)` by Euler's theorem.

**Parameters:**
- `ciphertext`: Encrypted message (integer)
- `private_key`: Tuple `(d, n)` containing private exponent and modulus

**Process:**
1. Uses modular exponentiation `pow(c, d, n)`
2. Returns decrypted message as decimal integer

**Security**: Only someone with the private key `d` can decrypt. The security relies on the difficulty of computing `d` from `e` and `n` without knowing `p` and `q`.

---

#### `text_to_decimal(text)` & `decimal_to_text(decimal_value)`

**Purpose**: Convert between text messages and decimal representation required by RSA.

**Encoding Process**:
```
Text → ASCII bytes → Hexadecimal → Decimal
"Nume Prenume" → [78, 117, 109, 101, 32, 80, ...] → "4e756d652050..." → (large decimal number)
```

**Why This Conversion?**
- RSA operates on integers, not text
- The entire message is converted to a single large number
- ASCII provides a standard byte encoding
- Hexadecimal is an intermediate representation
- Decimal is the final numeric format for RSA operations

**Limitations**: The message (as decimal) must be smaller than the modulus `n`. For "Nume Prenume" with 2048-bit keys, this is easily satisfied.

---

## Task 2.2: ElGamal Algorithm

### 1. Theory Explanation

**ElGamal** is a public-key cryptosystem based on the Diffie-Hellman key exchange, invented by Taher ElGamal in 1985. Unlike RSA, ElGamal provides **probabilistic encryption**, meaning the same plaintext produces different ciphertexts each time it's encrypted.

#### How ElGamal Works:

**Key Generation:**
1. Choose a large prime `p` and a generator `g` (primitive root modulo `p`)
2. Choose a private key `x` randomly such that `1 < x < p-1`
3. Calculate public key `y = g^x (mod p)`

**Public Key**: `(p, g, y)` - shared publicly  
**Private Key**: `(x, p)` - kept secret

**Encryption:**
1. Choose a random secret `k` such that `1 < k < p-1` and `GCD(k, p-1) = 1`
2. Calculate `c1 = g^k (mod p)`
3. Calculate `c2 = (y^k × m) mod p`

**Ciphertext**: `(c1, c2)` - a pair of integers

**Decryption:**
1. Calculate `s = c1^x (mod p)`
2. Calculate `s_inv = s^(-1) (mod p)` (modular multiplicative inverse)
3. Calculate `m = (c2 × s_inv) mod p`

**Security:** ElGamal security relies on the **discrete logarithm problem**: given `g`, `p`, and `y = g^x mod p`, it's computationally infeasible to find `x`.

**Key Advantage**: Probabilistic encryption provides semantic security - the same message encrypted twice produces different ciphertexts, preventing pattern analysis.

### 2. Important Functions

#### Function 1: Key Generation

```python
def generate_elgamal_keys(p, g):
    """
    Generate ElGamal public and private keys.
    
    Algorithm steps:
    1. Choose a private key x such that 1 < x < p-1
    2. Calculate public key y = g^x (mod p)
    """
    # Step 1: Choose private key x
    x_min = 2
    x_max = min(p - 2, 2**256)  # Limit to 256 bits for practical computation
    x = random.randint(x_min, x_max)
    
    # Step 2: Calculate public key y = g^x (mod p)
    y = pow(g, x, p)
    
    public_key = (p, g, y)
    private_key = (x, p)
    return public_key, private_key
```

#### Function 2: Encryption

```python
def elgamal_encrypt(message_decimal, public_key):
    """
    Encrypt a message using ElGamal public key.
    
    Encryption algorithm:
    1. Choose a random secret k such that 1 < k < p-1 and GCD(k, p-1) = 1
    2. Calculate c1 = g^k (mod p)
    3. Calculate c2 = (y^k * m) mod p
    """
    p, g, y = public_key
    
    # Step 1: Choose random secret k
    k_min = 2
    k_max = min(p - 2, 2**256)
    
    while True:
        k = random.randint(k_min, k_max)
        if GCD(k, p - 1) == 1:
            break
    
    # Step 2: Calculate c1 = g^k (mod p)
    c1 = pow(g, k, p)
    
    # Step 3: Calculate c2 = (y^k * m) mod p
    y_power_k = pow(y, k, p)
    c2 = (y_power_k * message_decimal) % p
    
    ciphertext = (c1, c2)
    return ciphertext, k
```

#### Function 3: Decryption

```python
def elgamal_decrypt(ciphertext, private_key):
    """
    Decrypt a ciphertext using ElGamal private key.
    
    Decryption algorithm:
    1. Calculate s = c1^x (mod p)
    2. Calculate s_inv = s^(-1) (mod p)
    3. Calculate m = (c2 * s_inv) mod p
    """
    c1, c2 = ciphertext
    x, p = private_key
    
    # Step 1: Calculate s = c1^x (mod p)
    s = pow(c1, x, p)
    
    # Step 2: Calculate modular multiplicative inverse of s
    s_inv = inverse(s, p)
    
    # Step 3: Calculate m = (c2 * s_inv) mod p
    message_decimal = (c2 * s_inv) % p
    
    return message_decimal
```

### 3. Function Descriptions

#### `generate_elgamal_keys(p, g)`

**Purpose**: Generates ElGamal key pair for encryption/decryption.

**Algorithm Breakdown:**
1. **Private Key Selection**: Randomly chooses `x` from a large range `[2, min(p-2, 2^256)]`. The range is limited to 256 bits for computational efficiency while maintaining security.
2. **Public Key Calculation**: Computes `y = g^x mod p` using modular exponentiation.

**Parameters:**
- `p`: Large prime modulus (2048 bits in this implementation)
- `g`: Generator/base (2 in this implementation)

**Returns:**
- `public_key`: Tuple `(p, g, y)` - all three values are public
- `private_key`: Tuple `(x, p)` - `x` must remain secret

**Key Insight**: The public key `y` can be computed from private key `x`, but finding `x` from `y` requires solving the discrete logarithm problem, which is computationally hard.

---

#### `elgamal_encrypt(message_decimal, public_key)`

**Purpose**: Encrypts a message using ElGamal public key encryption.

**Mathematical Formulas**:
- `c1 = g^k (mod p)` - masks the random secret `k`
- `c2 = (y^k × m) mod p` - encrypts the message using shared secret `y^k`

**Parameters:**
- `message_decimal`: Plaintext as decimal integer (must be < p)
- `public_key`: Tuple `(p, g, y)`

**Process:**
1. **Random Secret Selection**: Chooses random `k` such that `GCD(k, p-1) = 1`. This condition ensures `k` has a multiplicative inverse modulo `p-1`.
2. **First Component**: Calculates `c1 = g^k mod p`, which serves as an ephemeral public key.
3. **Second Component**: Calculates `c2 = (y^k × m) mod p`, which is the actual encrypted message.

**Probabilistic Nature**: Each encryption uses a fresh random `k`, so encrypting the same message twice produces different ciphertexts `(c1, c2)`. This provides **semantic security**.

**Returns**: Tuple `(c1, c2)` - both components are needed for decryption.

---

#### `elgamal_decrypt(ciphertext, private_key)`

**Purpose**: Decrypts ElGamal ciphertext using the private key.

**Mathematical Formula**: `m = c2 × (c1^x)^(-1) mod p`

**Mathematical Proof**:
```
During encryption:
  c1 = g^k mod p
  c2 = (y^k × m) mod p
  where y = g^x mod p

During decryption:
  s = c1^x = (g^k)^x = g^(kx) mod p
  s_inv = (g^(kx))^(-1) mod p
  
  m = c2 × s_inv
    = (y^k × m) × (g^(kx))^(-1) mod p
    = ((g^x)^k × m) × (g^(kx))^(-1) mod p
    = (g^(xk) × m) × (g^(kx))^(-1) mod p
    = m mod p
```

**Parameters:**
- `ciphertext`: Tuple `(c1, c2)`
- `private_key`: Tuple `(x, p)`

**Process:**
1. **Shared Secret Recovery**: Calculates `s = c1^x mod p`, which equals `g^(kx) mod p`. This is the same as `y^k` used in encryption.
2. **Inverse Calculation**: Finds modular multiplicative inverse `s_inv = s^(-1) mod p`.
3. **Message Recovery**: Multiplies `c2` by `s_inv` to recover the original message.

**Key Insight**: The decryption works because `c1^x = (g^k)^x = g^(kx) = (g^x)^k = y^k`, recovering the shared secret used during encryption.

---

## Task 3: Diffie-Hellman Key Exchange + AES

### 1. Theory Explanation

This task combines **asymmetric cryptography** (Diffie-Hellman) with **symmetric cryptography** (AES) to create a practical secure communication system.

#### Diffie-Hellman Key Exchange:

**Purpose**: Allows two parties (Alice and Bob) to establish a shared secret over an insecure channel without prior communication.

**How It Works:**
1. **Alice** chooses secret `a`, calculates `A = g^a (mod p)`, sends `A` to Bob
2. **Bob** chooses secret `b`, calculates `B = g^b (mod p)`, sends `B` to Alice
3. **Alice** computes shared secret: `K = B^a (mod p) = g^(ab) (mod p)`
4. **Bob** computes shared secret: `K = A^b (mod p) = g^(ab) (mod p)`

Both arrive at the same shared secret `K` without ever transmitting it!

**Security**: An attacker who intercepts `A` and `B` cannot compute `K` without solving the discrete logarithm problem to find `a` or `b`.

#### AES (Advanced Encryption Standard):

**Purpose**: Fast, efficient symmetric encryption for bulk data.

**AES-256**: Uses a 256-bit key and operates on 128-bit (16-byte) blocks.

**CBC Mode (Cipher Block Chaining)**:
- Each plaintext block is XORed with the previous ciphertext block before encryption
- First block is XORed with an Initialization Vector (IV)
- Same plaintext produces different ciphertexts (semantic security)

#### Combining Both:

1. **Diffie-Hellman**: Establishes a shared secret securely
2. **SHA-256**: Derives a fixed 256-bit key from the variable-size shared secret
3. **AES-256-CBC**: Encrypts the actual message quickly and securely

This is the foundation of modern protocols like **TLS/SSL**!

### 2. Important Functions

#### Function 1: Diffie-Hellman Key Exchange

```python
def diffie_hellman_key_exchange(p, g):
    """
    Perform Diffie-Hellman key exchange between Alice and Bob.
    
    Algorithm steps:
    For Alice:
    1. Choose secret a (random number: 1 < a < p-1)
    2. Calculate A = g^a (mod p)
    3. Send A to Bob
    
    For Bob:
    1. Choose secret b (random number: 1 < b < p-1)
    2. Calculate B = g^b (mod p)
    3. Send B to Alice
    
    Shared secret:
    - Alice calculates: K = B^a (mod p) = g^(ab) (mod p)
    - Bob calculates: K = A^b (mod p) = g^(ab) (mod p)
    """
    # Alice's side
    a = generate_diffie_hellman_secret(p)
    A = pow(g, a, p)  # A = g^a mod p
    
    # Bob's side
    b = generate_diffie_hellman_secret(p)
    B = pow(g, b, p)  # B = g^b mod p
    
    # Shared secret calculation
    K_alice = pow(B, a, p)  # Alice: K = B^a = g^(ab) mod p
    K_bob = pow(A, b, p)    # Bob: K = A^b = g^(ab) mod p
    
    # They match!
    shared_secret = K_alice
    
    return {
        'a': a, 'b': b,
        'A': A, 'B': B,
        'shared_secret': shared_secret
    }
```

#### Function 2: AES Key Derivation

```python
def derive_aes_key(shared_secret, key_size_bytes=32):
    """
    Derive an AES-256 key from the shared secret.
    
    Use SHA-256 hash of the shared secret to get exactly 32 bytes (256 bits).
    """
    # Convert shared secret to bytes (big-endian)
    secret_bytes = shared_secret.to_bytes(
        (shared_secret.bit_length() + 7) // 8, 'big'
    )
    
    # Use SHA-256 to derive exactly 32 bytes (256 bits)
    aes_key = hashlib.sha256(secret_bytes).digest()
    
    return aes_key
```

#### Function 3: AES Encryption

```python
def aes_encrypt(plaintext, key):
    """
    Encrypt plaintext using AES-256 in CBC mode.
    """
    # Generate random IV (Initialization Vector) for CBC mode
    iv = get_random_bytes(16)  # 16 bytes = 128 bits
    
    # Create AES cipher in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Pad plaintext to block size (AES block size is 16 bytes)
    padded_plaintext = pad(plaintext, AES.block_size)
    
    # Encrypt
    ciphertext = cipher.encrypt(padded_plaintext)
    
    return ciphertext, iv
```

#### Function 4: AES Decryption

```python
def aes_decrypt(ciphertext, key, iv):
    """
    Decrypt ciphertext using AES-256 in CBC mode.
    """
    # Create AES cipher in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Decrypt
    padded_plaintext = cipher.decrypt(ciphertext)
    
    # Unpad
    plaintext = unpad(padded_plaintext, AES.block_size)
    
    return plaintext
```

### 3. Function Descriptions

#### `diffie_hellman_key_exchange(p, g)`

**Purpose**: Performs the complete Diffie-Hellman key exchange protocol between Alice and Bob.

**Algorithm Breakdown:**

**Alice's Operations:**
1. Chooses secret `a` randomly (using `generate_diffie_hellman_secret()`)
2. Computes `A = g^a mod p` (public value to send to Bob)
3. Receives `B` from Bob
4. Computes shared secret `K = B^a mod p = g^(ab) mod p`

**Bob's Operations:**
1. Chooses secret `b` randomly
2. Computes `B = g^b mod p` (public value to send to Alice)
3. Receives `A` from Alice
4. Computes shared secret `K = A^b mod p = g^(ab) mod p`

**Key Insight**: Both parties independently compute the same shared secret `K = g^(ab) mod p` without ever transmitting it directly!

**Security**: Even if an attacker intercepts `A` and `B`, they cannot compute `K` without solving the discrete logarithm problem to find `a` (from `A = g^a`) or `b` (from `B = g^b`).

**Returns**: Dictionary with all intermediate values:
- `a`, `b`: Private secrets
- `A`, `B`: Public values (safe to transmit)
- `shared_secret`: The shared key `K`

---

#### `derive_aes_key(shared_secret, key_size_bytes=32)`

**Purpose**: Derives a fixed-size AES-256 key from the Diffie-Hellman shared secret.

**Why Needed?**
- The shared secret `K` is a variable-size integer (could be hundreds of bits)
- AES-256 requires exactly 32 bytes (256 bits)
- We need a deterministic way to convert the secret to a key

**Process:**
1. **Byte Conversion**: Converts the shared secret integer to bytes using big-endian encoding
2. **Hash Function**: Applies SHA-256 hash function to produce exactly 32 bytes
3. **Key Output**: The hash output becomes the AES-256 key

**Why SHA-256?**
- **Fixed Output Size**: Always produces 256 bits, perfect for AES-256
- **Uniform Distribution**: Hash functions provide uniform key distribution
- **One-Way Function**: Even if key is compromised, original secret remains hidden
- **Deterministic**: Same input always produces same output

**Security Note**: SHA-256 is cryptographically secure and provides strong key derivation.

---

#### `aes_encrypt(plaintext, key)`

**Purpose**: Encrypts plaintext using AES-256 in CBC (Cipher Block Chaining) mode.

**Algorithm Breakdown:**

**CBC Mode Operation:**
1. **IV Generation**: Creates a random 16-byte Initialization Vector
   - Ensures same plaintext produces different ciphertexts
   - IV is not secret but must be random and unique
2. **Padding**: Adds PKCS7 padding to align plaintext to 16-byte blocks
   - AES operates on fixed 16-byte (128-bit) blocks
   - Padding adds 1-16 bytes to make length a multiple of 16
3. **Block Encryption**:
   - First block: `C1 = AES_Encrypt(P1 ⊕ IV)`
   - Subsequent blocks: `Ci = AES_Encrypt(Pi ⊕ C(i-1))`
   - Each ciphertext block depends on previous blocks

**Parameters:**
- `plaintext`: Message as bytes
- `key`: AES-256 key (32 bytes)

**Returns**: Tuple `(ciphertext, iv)`
- `ciphertext`: Encrypted bytes
- `iv`: Initialization Vector (needed for decryption)

**Security Features:**
- **Semantic Security**: Same plaintext → different ciphertexts (due to random IV)
- **Error Propagation**: One bit error affects all subsequent blocks
- **Confidentiality**: Strong encryption provides data protection

---

#### `aes_decrypt(ciphertext, key, iv)`

**Purpose**: Decrypts AES-256-CBC ciphertext to recover original plaintext.

**Algorithm Breakdown:**

**CBC Mode Decryption:**
1. **Block Decryption**:
   - First block: `P1 = AES_Decrypt(C1) ⊕ IV`
   - Subsequent blocks: `Pi = AES_Decrypt(Ci) ⊕ C(i-1)`
   - XOR with previous ciphertext block (or IV for first block)
2. **Unpadding**: Removes PKCS7 padding to recover original message length

**Parameters:**
- `ciphertext`: Encrypted bytes
- `key`: AES-256 key (32 bytes) - must match encryption key
- `iv`: Initialization Vector - must match encryption IV

**Returns**: Decrypted plaintext as bytes

**Important**: 
- Must use the **same** `key` and `iv` as used in encryption
- The IV is typically sent alongside the ciphertext (it's not secret)
- Padding removal verifies correct decryption (invalid padding = wrong key)

**Mathematical Proof**:
```
Encryption: C1 = AES_Encrypt(P1 ⊕ IV)
Decryption: P1' = AES_Decrypt(C1) ⊕ IV
            = AES_Decrypt(AES_Encrypt(P1 ⊕ IV)) ⊕ IV
            = (P1 ⊕ IV) ⊕ IV
            = P1 ✓
```

---

## Installation

1. **Navigate to the project:**
   ```bash
   cd Lab5
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

### Task 2.1: RSA
```bash
python3 Task2.1.py
```

**Expected Output:**
- Key generation steps (p, q, n, φ(n), e, d)
- Message encoding (ASCII → Hex → Decimal)
- Encryption process with formula
- Decryption process with formula
- Verification that original = decrypted

### Task 2.2: ElGamal
```bash
python3 Task2.2.py
```

**Expected Output:**
- Key generation (private x, public y)
- Message encoding
- Encryption with random k producing (c1, c2)
- Decryption steps showing shared secret recovery
- Verification

### Task 3: Diffie-Hellman + AES
```bash
python3 Task3.py
```

**Expected Output:**
- Alice's secret `a` and public `A`
- Bob's secret `b` and public `B`
- Shared secret calculation (both sides match)
- AES key derivation using SHA-256
- AES encryption with IV generation
- AES decryption with padding removal
- Verification

---

## Common Parameters

Tasks 2.2 and 3 share the same public parameters:

```python
P = 32317006071311007300153513477825163362488057133489075174588434139269806834136210002792056362640164685458556357935330816928829023080573472625273554742461245741026202527916572972862706300325263428213145766931414223654220941111348629991657478268034230553086349050635557712219187890332729569696129743856241741236237225197346402691855797767976823014625397933058015226858730761197532436467475855460715043896844940366130497697812854295958659597567051283852132784468522925504568272879113720098931873959143374175837826000278034973198552060607533234122603254684088120031105907484281003994966956119696956248629032338072839127039
G = 2
```

- **P**: 2048-bit prime number (modulus)
- **G**: Generator (base) = 2

---

## Algorithm Comparison

| Feature | RSA | ElGamal | Diffie-Hellman + AES |
|---------|-----|---------|---------------------|
| **Type** | Public-key encryption | Public-key encryption | Key exchange + Symmetric |
| **Ciphertext** | Single integer | Two integers (c1, c2) | Binary (AES blocks) |
| **Deterministic?** | Yes | No (probabilistic) | No (random IV) |
| **Speed** | Moderate | Moderate | Fast (AES) |
| **Key Size** | 2048+ bits | 2048+ bits | 2048-bit DH, 256-bit AES |
| **Use Case** | Data encryption, signatures | Encryption, signatures | Secure key establishment |

---

## Security Notes

1. **Key Sizes**: All implementations use 2048+ bit keys, meeting current security standards
2. **Random Secrets**: All random values are generated using cryptographically secure methods
3. **Message Encoding**: ASCII encoding used for text-to-number conversion
4. **Modular Arithmetic**: All exponentiation uses efficient modular arithmetic (`pow(base, exp, mod)`)
5. **Padding**: AES uses PKCS7 padding for block alignment
6. **IV**: AES-CBC uses random IVs for semantic security

---

## References

- **RSA**: Rivest, Shamir, Adleman (1978) - "A Method for Obtaining Digital Signatures"
- **ElGamal**: Taher ElGamal (1985) - "A Public Key Cryptosystem and a Signature Scheme"
- **Diffie-Hellman**: Diffie & Hellman (1976) - "New Directions in Cryptography"
- **AES**: Advanced Encryption Standard (FIPS 197)

---

## Troubleshooting

**Import Error: `No module named 'Crypto'`**
```bash
pip install pycryptodome
```

**Large Number Computation Takes Time**
- RSA and ElGamal with 2048-bit keys require significant computation
- This is normal and demonstrates real-world cryptographic operations
- Diffie-Hellman also involves large modular exponentiations

**Message Too Large Error**
- Ensure message (in decimal) is smaller than modulus `n` or `p`
- For longer messages, use hybrid encryption (RSA/ElGamal for key exchange + AES for data)

---

## License

This is an educational implementation for learning purposes. Do not use in production systems without security audit.
