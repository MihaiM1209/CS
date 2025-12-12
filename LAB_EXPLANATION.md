# Lab 4: Distributed Key-Value Store - Complete Explanation

## Table of Contents

1. [What is This Lab About?](#what-is-this-lab-about)
2. [Learning Objectives](#learning-objectives)
3. [Key Concepts Explained](#key-concepts-explained)
4. [System Architecture from Scratch](#system-architecture-from-scratch)
5. [How the Code Works - Step by Step](#how-the-code-works---step-by-step)
6. [What Can We Learn?](#what-can-we-learn)
7. [Real-World Applications](#real-world-applications)

---

## What is This Lab About?

### The Problem

Imagine you have a website that stores user data (like usernames, emails, etc.). If you store this data on a single server, what happens if:

- The server crashes? → **All data is lost!**
- Too many users try to access it? → **Server becomes slow or crashes!**
- The server is in one location? → **Users far away experience slow access!**

**Solution:** Use **multiple servers** (distributed system) that work together!

### What This Lab Implements

This lab implements a **distributed key-value store** - a system where:

1. **One server (Leader)** accepts write requests
2. **Multiple servers (Followers)** keep copies of the data
3. **Data is replicated** to all followers for reliability
4. **Version numbers** ensure data consistency
5. **Quorum consensus** ensures writes are successful

### Real-World Examples

- **Amazon DynamoDB**: Distributed database used by Amazon
- **Apache Cassandra**: Distributed database used by Netflix, Facebook
- **Redis Cluster**: Distributed caching system
- **Google Cloud Spanner**: Globally distributed database

---

## Learning Objectives

By completing this lab, you will learn:

### 1. **Distributed Systems Fundamentals**
   - How multiple servers work together
   - Leader-follower architecture
   - Data replication strategies

### 2. **Consistency Models**
   - Strong consistency vs. eventual consistency
   - Quorum-based consensus
   - Version conflict resolution

### 3. **Concurrency and Threading**
   - Thread-safe data structures
   - Concurrent replication
   - Race condition prevention

### 4. **Network Communication**
   - HTTP-based inter-server communication
   - Network delay simulation
   - Error handling in distributed systems

### 5. **Software Design Principles**
   - SOLID principles in practice
   - Dependency injection
   - Interface-based design

### 6. **Practical Skills**
   - Docker containerization
   - REST API design
   - Testing distributed systems

---

## Key Concepts Explained

### 1. What is a Key-Value Store?

A **key-value store** is like a dictionary or hash map:

```python
# Simple example:
store = {
    "user:1:name": "Alice",
    "user:1:email": "alice@example.com",
    "user:2:name": "Bob"
}

# Get value by key:
name = store["user:1:name"]  # Returns "Alice"

# Set value:
store["user:2:email"] = "bob@example.com"
```

**Why use key-value stores?**
- Simple and fast
- Easy to scale
- Good for caching
- Used by many real systems (Redis, Memcached, DynamoDB)

---

### 2. What is Replication?

**Replication** means keeping copies of data on multiple servers.

**Example:**
```
Original data on Server 1:
  {"user:1": "Alice"}

After replication:
  Server 1: {"user:1": "Alice"}
  Server 2: {"user:1": "Alice"}  ← Copy
  Server 3: {"user:1": "Alice"}  ← Copy
```

**Why replicate?**
- **Reliability**: If one server fails, others have the data
- **Performance**: Users can read from nearest server
- **Availability**: System keeps working even if some servers fail

---

### 3. What is a Leader-Follower Architecture?

In a **leader-follower** (also called master-slave) architecture:

- **Leader (Master)**: 
  - Accepts all write requests
  - Coordinates replication
  - Single source of truth for writes

- **Followers (Slaves)**:
  - Receive copies of data from leader
  - Can serve read requests
  - Cannot accept writes directly

**Visual:**
```
         Client
           │
           │ Write request
           ▼
       ┌────────┐
       │ Leader │ ← Only leader accepts writes
       └───┬────┘
           │
           │ Replicates to
           │
    ┌──────┼──────┐
    ▼      ▼      ▼
┌─────┐ ┌─────┐ ┌─────┐
│ F1  │ │ F2  │ │ F3  │ ← Followers receive copies
└─────┘ └─────┘ └─────┘
```

**Why this design?**
- Simple: Only one server handles writes
- Consistent: All writes go through leader
- Easy to understand and implement

---

### 4. What is Quorum Consensus?

**Quorum** means "majority" or "minimum number required."

**Example with 5 followers:**
- **Quorum = 5**: All 5 followers must acknowledge (strongest consistency)
- **Quorum = 3**: 3 out of 5 followers must acknowledge (balanced)
- **Quorum = 1**: Only 1 follower must acknowledge (weakest, fastest)

**How it works:**
```
1. Leader writes data locally
2. Leader sends replication to all 5 followers
3. Leader waits for acknowledgments
4. If 3+ followers respond "OK" → Write succeeds (quorum met)
5. If < 3 followers respond → Write fails (quorum not met)
```

**Why quorum?**
- **Trade-off**: Consistency vs. Availability
- Higher quorum = Stronger consistency, Slower writes
- Lower quorum = Weaker consistency, Faster writes

This is related to the **CAP Theorem**:
- **Consistency**: All nodes see same data
- **Availability**: System responds to requests
- **Partition tolerance**: System works despite network failures

You can't have all three perfectly - you must choose!

---

### 5. What are Lamport Timestamps?

**Lamport timestamps** are version numbers that ensure ordering of events.

**Key property:** Version numbers are **monotonically increasing** (always go up).

**Example:**
```
Write 1: version = 1
Write 2: version = 2
Write 3: version = 3
Write 4: version = 4
```

**Why use them?**
- **Ordering**: We know version 3 happened after version 2
- **Conflict resolution**: If two writes arrive out of order, we keep the higher version
- **Consistency**: All servers eventually agree on the latest version

**Real scenario:**
```
Network delay causes out-of-order delivery:
  Follower receives: version=3, version=1, version=2
  
Follower processes:
  1. Receives version=3 → Accepts (no existing data)
  2. Receives version=1 → Rejects (1 < 3, stale)
  3. Receives version=2 → Rejects (2 < 3, stale)
  
Result: Follower has version=3 (correct!)
```

---

### 6. What is Semi-Synchronous Replication?

**Synchronous**: Leader waits for ALL followers before responding (slow, but very consistent)

**Asynchronous**: Leader responds immediately, replicates in background (fast, but may lose data)

**Semi-Synchronous**: Leader waits for QUORUM of followers (balanced!)

**Our system uses semi-synchronous:**
```
1. Leader sends to all 5 followers simultaneously
2. Leader waits for 5 acknowledgments (quorum = 5)
3. As soon as 5 respond → Leader responds to client
4. Doesn't wait for remaining followers (if any fail)
```

**Benefits:**
- Faster than fully synchronous
- More consistent than asynchronous
- Good balance!

---

## System Architecture from Scratch

### High-Level Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Client Application                   │
│              (Browser, Mobile App, etc.)               │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ HTTP Requests
                     │
         ┌───────────▼───────────┐
         │                       │
         │   Leader Node         │
         │   (Port 8000)         │
         │                       │
         │  ┌─────────────────┐  │
         │  │  Flask Server   │  │
         │  └────────┬────────┘  │
         │           │           │
         │  ┌────────▼────────┐  │
         │  │  Storage        │  │
         │  │  VersionManager │  │
         │  │  ReplicationMgr │  │
         │  └─────────────────┘  │
         └───────────┬───────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
         │    Replication        │
         │    (HTTP POST)        │
         │           │           │
    ┌────▼────┐ ┌───▼────┐ ┌───▼────┐
    │Follower1│ │Follower2│ │Follower3│
    │Port 8001│ │Port 8002│ │Port 8003│
    └─────────┘ └─────────┘ └─────────┘
```

### Component Breakdown

#### 1. **Leader Node** (`leader.py`)

**Responsibilities:**
- Accepts write requests from clients
- Generates version numbers
- Stores data locally
- Coordinates replication to followers
- Serves read requests

**Key Components:**
```python
storage = MemoryStorage()           # Stores key-value pairs
version_manager = VersionManager()  # Generates version numbers
replication_manager = ReplicationManager(...)  # Handles replication
```

#### 2. **Follower Nodes** (`follower.py`)

**Responsibilities:**
- Receives replication requests from leader
- Stores replicated data
- Resolves version conflicts
- Serves read requests

**Key Components:**
```python
storage = MemoryStorage()           # Stores replicated data
version_manager = VersionManager()  # Checks version conflicts
```

#### 3. **Storage Module** (`src/storage/`)

**Purpose:** Abstract data storage layer

**Implementation:** `MemoryStorage` - stores data in Python dictionary

**Why abstract?** Can swap to Redis, PostgreSQL, etc. without changing other code!

#### 4. **Versioning Module** (`src/versioning/`)

**Purpose:** Manages Lamport timestamps

**Key Function:** `get_next_version()` - returns next version number

#### 5. **Replication Module** (`src/replication/`)

**Purpose:** Handles quorum-based replication

**Key Function:** `replicate_to_followers()` - sends to all followers concurrently

#### 6. **Network Module** (`src/network/`)

**Purpose:** HTTP communication abstraction

**Implementation:** `RequestsHTTPClient` - uses `requests` library

---

## How the Code Works - Step by Step

### Scenario: Client Writes "user:1:name" = "Alice"

Let's trace through the entire code execution:

---

### Step 1: Client Sends Request

**Client code:**
```python
import requests
response = requests.post(
    "http://localhost:8000/write",
    json={"key": "user:1:name", "value": "Alice"}
)
```

**What happens:**
- HTTP POST request sent to leader
- Flask receives request

---

### Step 2: Leader Receives Request

**File:** `leader.py`

**Function:** `write()`

```python
@app.route('/write', methods=['POST'])
def write():
    # Step 2.1: Parse request
    data = request.get_json()  # Gets {"key": "user:1:name", "value": "Alice"}
    key = data.get('key')      # key = "user:1:name"
    value = data.get('value')  # value = "Alice"
    
    # Step 2.2: Validate
    if key is None or value is None:
        return jsonify({"error": "key and value are required"}), 400
    
    # Step 2.3: Generate version number
    current_version = version_manager.get_next_version()
    # This calls VersionManager.get_next_version()
    # Returns: 1 (first write)
    
    # Step 2.4: Store locally
    storage.set(key, value, current_version)
    # This calls MemoryStorage.set("user:1:name", "Alice", 1)
    # Stores: {"user:1:name": {"value": "Alice", "version": 1}}
    
    # Step 2.5: Replicate to followers
    if replication_manager.replicate_to_followers(key, value, current_version):
        # If quorum met, return success
        return jsonify({"status": "success", ...}), 200
    else:
        # If quorum not met, return partial success
        return jsonify({"status": "partial_success", ...}), 200
```

**Let's dive deeper into each step:**

---

### Step 3: Generate Version Number

**File:** `src/versioning/version_manager.py`

**Function:** `get_next_version()`

```python
def get_next_version(self) -> int:
    """Get and increment the version counter."""
    with self._lock:  # Acquire lock (thread-safe)
        self._version_counter += 1  # Increment: 0 → 1
        return self._version_counter  # Return 1
```

**What happens:**
1. Lock acquired (ensures only one thread at a time)
2. Version counter incremented: `0 → 1`
3. Returns `1`
4. Lock released

**Why lock?** Prevents race conditions if multiple writes happen simultaneously!

---

### Step 4: Store Locally

**File:** `src/storage/memory_storage.py`

**Function:** `set()`

```python
def set(self, key: str, value: Any, version: int) -> None:
    """Set a key-value pair with version."""
    with self._lock:  # Acquire lock
        self._data[key] = {
            "value": value,
            "version": version
        }
    # Lock released automatically
```

**What happens:**
1. Lock acquired
2. Data stored: `{"user:1:name": {"value": "Alice", "version": 1}}`
3. Lock released

**Internal state after:**
```python
self._data = {
    "user:1:name": {
        "value": "Alice",
        "version": 1
    }
}
```

---

### Step 5: Replicate to Followers

**File:** `src/replication/replication_manager.py`

**Function:** `replicate_to_followers()`

```python
def replicate_to_followers(self, key: str, value: Any, version: int) -> bool:
    # Step 5.1: Initialize counters
    successful_replications = 0
    failed_replications = 0
    
    # Step 5.2: Create thread pool (for concurrent execution)
    executor = ThreadPoolExecutor(max_workers=5)  # 5 followers
    
    # Step 5.3: Submit all replication tasks concurrently
    future_to_follower = {
        executor.submit(
            self.replicate_to_follower, 
            "http://follower1:5000", 
            "user:1:name", 
            "Alice", 
            1
        ): "http://follower1:5000",
        executor.submit(
            self.replicate_to_follower, 
            "http://follower2:5000", 
            "user:1:name", 
            "Alice", 
            1
        ): "http://follower2:5000",
        # ... same for follower3, follower4, follower5
    }
    
    # Step 5.4: Wait for results (as they complete)
    for future in as_completed(future_to_follower):
        follower = future_to_follower[future]
        if future.result():  # If replication succeeded
            successful_replications += 1
            if successful_replications >= 5:  # Quorum = 5
                return True  # Quorum met!
    
    return successful_replications >= 5
```

**Key point:** All 5 replications happen **concurrently** (at the same time), not one after another!

---

### Step 6: Replicate to Single Follower

**File:** `src/replication/replication_manager.py`

**Function:** `replicate_to_follower()`

```python
def replicate_to_follower(self, follower_url: str, key: str, value: Any, version: int) -> bool:
    # Step 6.1: Simulate network delay
    delay = random.uniform(0.0001, 1.0)  # Random between 0.1ms and 1000ms
    time.sleep(delay)  # Wait (simulates network latency)
    
    # Step 6.2: Send HTTP POST request
    return self._http_client.post(
        f"{follower_url}/replicate",  # "http://follower1:5000/replicate"
        json_data={
            "key": "user:1:name",
            "value": "Alice",
            "version": 1
        },
        timeout=5
    )
```

**What happens:**
1. Random delay: `0.234 seconds` (simulates network)
2. Sleep for 0.234 seconds
3. Send HTTP POST to follower
4. Return `True` if successful, `False` if failed

**Why simulate delay?** Real networks have latency! This tests our system under realistic conditions.

---

### Step 7: HTTP Client Sends Request

**File:** `src/network/requests_client.py`

**Function:** `post()`

```python
def post(self, url: str, json_data: Dict[str, Any], timeout: int = 5) -> bool:
    try:
        # Use requests library to send HTTP POST
        response = requests.post(
            url,                    # "http://follower1:5000/replicate"
            json=json_data,         # {"key": "user:1:name", "value": "Alice", "version": 1}
            timeout=timeout         # 5 seconds
        )
        return response.status_code == 200  # True if success
    except Exception as e:
        logger.error(f"POST request failed: {e}")
        return False  # False if failed
```

**What happens:**
1. `requests.post()` sends HTTP request over network
2. Waits for response from follower
3. Returns `True` if HTTP status code is 200 (success)
4. Returns `False` if error or timeout

---

### Step 8: Follower Receives Replication

**File:** `follower.py`

**Function:** `replicate()`

```python
@app.route('/replicate', methods=['POST'])
def replicate():
    # Step 8.1: Parse request
    data = request.get_json()  # {"key": "user:1:name", "value": "Alice", "version": 1}
    key = data.get('key')
    value = data.get('value')
    version = data.get('version')  # version = 1
    
    # Step 8.2: Get existing data (if any)
    existing_data = storage.get("user:1:name")  # Returns None (key doesn't exist yet)
    current_version = existing_data["version"] if existing_data else None  # None
    
    # Step 8.3: Check if version should be accepted
    if version_manager.should_accept_version(1, None):
        # This checks: 1 > None? → True (no existing data, accept any version)
        
        # Step 8.4: Store the data
        storage.set("user:1:name", "Alice", 1)
        # Now follower has: {"user:1:name": {"value": "Alice", "version": 1}}
        
        return jsonify({"status": "success", "updated": True}), 200
    else:
        return jsonify({"status": "success", "updated": False, "reason": "stale_version"}), 200
```

**What happens:**
1. Follower receives replication request
2. Checks if key exists (doesn't exist yet)
3. Checks version: `1 > None` → Accept!
4. Stores data locally
5. Returns success

---

### Step 9: Version Conflict Resolution

**File:** `src/versioning/version_manager.py`

**Function:** `should_accept_version()`

```python
def should_accept_version(self, incoming_version: int, current_version: Optional[int]) -> bool:
    """Check if incoming version should be accepted."""
    if current_version is None:
        return True  # No existing data, accept any version
    return incoming_version > current_version  # Accept if newer
```

**Example scenarios:**

**Scenario A: No existing data**
```python
should_accept_version(1, None)  # True - accept (no existing data)
```

**Scenario B: Newer version**
```python
# Follower currently has version 5
should_accept_version(10, 5)  # True - accept (10 > 5, newer)
```

**Scenario C: Stale version (reject!)**
```python
# Follower currently has version 10
should_accept_version(3, 10)  # False - reject (3 < 10, stale)
```

**Why this matters:** Prevents out-of-order network delivery from corrupting data!

---

### Step 10: Quorum Check

Back in `replicate_to_followers()`:

```python
# After all 5 followers respond:
successful_replications = 5  # All 5 succeeded!
failed_replications = 0

# Check quorum:
if successful_replications >= 5:  # 5 >= 5 → True
    return True  # Quorum met!
```

**Result:** Leader returns success to client!

---

### Complete Flow Summary

```
1. Client → POST /write {"key": "user:1:name", "value": "Alice"}
2. Leader receives request
3. Leader generates version = 1
4. Leader stores locally: {"user:1:name": {"value": "Alice", "version": 1}}
5. Leader sends replication to all 5 followers (concurrently)
   ├─► Follower1: delay 0.1s → stores data → returns success
   ├─► Follower2: delay 0.3s → stores data → returns success
   ├─► Follower3: delay 0.2s → stores data → returns success
   ├─► Follower4: delay 0.5s → stores data → returns success
   └─► Follower5: delay 0.4s → stores data → returns success
6. Leader counts: 5 successful replications
7. Quorum check: 5 >= 5 → True
8. Leader returns: {"status": "success", "version": 1}
9. Client receives success response
```

---

## What Can We Learn?

### 1. **Distributed Systems Are Complex**

**Challenge:** Multiple servers must agree on data

**Solution:** Quorum consensus, version numbers, replication

**Lesson:** Distributed systems require careful design to handle failures, network delays, and concurrent operations.

---

### 2. **Consistency vs. Availability Trade-off**

**Strong Consistency (Quorum = 5):**
- ✅ All nodes always have same data
- ❌ Slower writes (must wait for all)
- ❌ System fails if too many servers down

**Weak Consistency (Quorum = 1):**
- ✅ Fast writes
- ✅ System works even if servers fail
- ❌ Nodes may have different data temporarily

**Lesson:** You must choose based on your application's needs!

---

### 3. **Thread Safety Matters**

**Problem:** Multiple requests can happen simultaneously

**Solution:** Locks protect shared data

**Example:**
```python
# Without lock (BAD):
self._version_counter += 1  # Race condition possible!

# With lock (GOOD):
with self._lock:
    self._version_counter += 1  # Thread-safe!
```

**Lesson:** Always protect shared state in concurrent systems!

---

### 4. **Design Patterns Help**

**Dependency Injection:**
```python
# Instead of hard-coding:
http_client = requests.post(...)  # BAD - hard to test

# Use dependency injection:
replication_manager = ReplicationManager(http_client=http_client)  # GOOD - testable
```

**Interface Segregation:**
```python
# Define interface:
class StorageInterface:
    def get(key): ...
    def set(key, value, version): ...

# Implement:
class MemoryStorage(StorageInterface): ...
class RedisStorage(StorageInterface): ...  # Can swap easily!
```

**Lesson:** Good design makes code maintainable and testable!

---

### 5. **Network Delays Are Real**

**Problem:** Network requests take time and may arrive out of order

**Solution:** Version numbers ensure correct ordering

**Example:**
```
Write 1 (version=1) sent at time T
Write 2 (version=2) sent at time T+1

Due to network:
  Follower receives: version=2 first, then version=1

With version checking:
  Follower accepts version=2
  Follower rejects version=1 (stale)

Result: Correct! (version=2 is latest)
```

**Lesson:** Distributed systems must handle network unpredictability!

---

### 6. **Testing Distributed Systems**

**Challenges:**
- Multiple servers to test
- Network conditions to simulate
- Concurrent operations to verify
- Failure scenarios to handle

**Our tests cover:**
- Basic operations (write/read)
- Concurrent writes
- Consistency checks
- Race conditions
- Performance analysis

**Lesson:** Testing distributed systems requires comprehensive test suites!

---

## Real-World Applications

### 1. **Database Replication**

**Example:** MySQL Master-Slave Replication
- Master accepts writes
- Slaves replicate data
- Slaves serve read requests
- Similar to our leader-follower design!

---

### 2. **Content Delivery Networks (CDN)**

**Example:** CloudFlare, Akamai
- Origin server (like our leader)
- Edge servers worldwide (like our followers)
- Content replicated to edges
- Users read from nearest edge

---

### 3. **Distributed Databases**

**Example:** Apache Cassandra
- Uses quorum consensus
- Handles network partitions
- Eventual consistency
- Similar concepts to our lab!

---

### 4. **Blockchain Systems**

**Example:** Bitcoin, Ethereum
- Multiple nodes maintain copies
- Consensus mechanisms (like quorum)
- Version control (blockchain = version history)
- Related concepts!

---

## Code Structure Explained

### Why This Structure?

```
src/
├── storage/          # Separated: Can swap storage backends
├── versioning/       # Separated: Version logic isolated
├── replication/      # Separated: Replication logic isolated
└── network/          # Separated: Network abstraction
```

**Benefits:**
- **Single Responsibility**: Each module does one thing
- **Testability**: Can test each module independently
- **Extensibility**: Can swap implementations easily
- **Maintainability**: Changes in one module don't affect others

**This follows SOLID principles!**

---

### Key Design Decisions

#### 1. **Why Write to Leader First?**

```python
# Leader writes immediately:
storage.set(key, value, version)

# Then replicates:
replication_manager.replicate_to_followers(...)
```

**Reason:** Leader always has latest data, even if replication fails

**Trade-off:** Leader may have data followers don't (if quorum fails)

---

#### 2. **Why Early Return on Quorum?**

```python
if successful_replications >= self._write_quorum:
    return True  # Don't wait for remaining followers!
```

**Reason:** Faster response time

**Trade-off:** Some followers may not have data yet (but will eventually)

---

#### 3. **Why Simulate Network Delay?**

```python
delay = random.uniform(0.0001, 1.0)
time.sleep(delay)
```

**Reason:** Tests system under realistic conditions (real networks have delays!)

**Benefit:** Verifies version conflict resolution works correctly

---

#### 4. **Why Version Conflict Resolution?**

```python
if version_manager.should_accept_version(incoming_version, current_version):
    storage.set(...)  # Accept
else:
    return {"updated": False}  # Reject
```

**Reason:** Prevents out-of-order network delivery from corrupting data

**Benefit:** Ensures eventual consistency

---

## Summary

This lab teaches you:

1. ✅ **How distributed systems work** - Multiple servers working together
2. ✅ **Replication strategies** - How to keep data in sync
3. ✅ **Consistency models** - Strong vs. eventual consistency
4. ✅ **Quorum consensus** - How to ensure writes succeed
5. ✅ **Version control** - Lamport timestamps for ordering
6. ✅ **Concurrency** - Thread-safe programming
7. ✅ **Software design** - SOLID principles in practice
8. ✅ **Real-world patterns** - Used in production systems!

**The code implements a real distributed system pattern used by companies like Amazon, Netflix, and Facebook!**

By understanding this lab, you understand the fundamentals of modern distributed systems! 🚀

