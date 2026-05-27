# FastAPI Security Guide

Complete guide to implementing authentication and authorization in FastAPI applications.

---

## Table of Contents

1. [Security Overview](#security-overview)
2. [Core Concepts](#core-concepts)
3. [OAuth2 Explained](#oauth2-explained)
4. [First Steps](#first-steps)
5. [Getting Current User](#getting-current-user)
6. [Password Flow with Bearer Tokens](#password-flow-with-bearer-tokens)
7. [JWT Tokens with Password Hashing](#jwt-tokens-with-password-hashing)
8. [Advanced Topics](#advanced-topics)
9. [Best Practices](#best-practices)

---

## Security Overview

Security is a fundamental aspect of API development. FastAPI provides built-in tools to handle authentication and authorization efficiently.

### Why Security Matters

- **Protection**: Secures user data and prevents unauthorized access
- **Compliance**: Meets industry standards and regulations
- **Trust**: Builds confidence in your application
- **Flexibility**: FastAPI allows customization without compromising security

### Key Statistics

- Security and authentication typically account for 50%+ of development effort in many frameworks
- FastAPI abstracts this complexity while maintaining flexibility
- OpenAPI integration provides automatic documentation of security schemes

---

## Core Concepts

### Authentication vs Authorization

| Concept | Definition | Example |
|---------|-----------|---------|
| **Authentication** | Verifying who you are | Login with username/password |
| **Authorization** | Determining what you can do | User can view their profile but not admin panel |

### Common Security Schemes

FastAPI supports multiple security schemes through OpenAPI:

#### 1. **API Key**
- Simple key-based authentication
- Source: Query parameter, header, or cookie
- Use case: Internal APIs, third-party integrations

#### 2. **HTTP Authentication**
- **Basic**: Username and password (Base64 encoded)
- **Bearer**: Token-based (OAuth2, JWT)
- **Digest**: More complex HTTP standard

#### 3. **OAuth2**
- Industry standard for delegation
- Enables "Login with Google/Facebook/GitHub"
- Multiple flows for different use cases

#### 4. **OpenID Connect**
- Built on OAuth2
- Adds standardized identity layer
- Used by Google, Microsoft

---

## OAuth2 Explained

### What is OAuth2?

OAuth2 is a specification defining how to handle authentication and authorization. It's designed so your backend API can be independent of the authentication server.

### OAuth2 Flows

| Flow | Use Case | Best For |
|------|----------|----------|
| **Implicit** | Browser-based apps | Legacy (not recommended) |
| **Client Credentials** | Server-to-server | Machine-to-machine |
| **Authorization Code** | Third-party apps | Google/Facebook login |
| **Password** | Own application | Backend + Frontend |
| **Refresh Token** | Token renewal | Long-lived sessions |

### Evolution of OAuth Standards

- **OAuth 1.0**: Original standard (complex, rarely used)
- **OAuth 2.0**: Modern standard (flexible, widely adopted)
- **OpenID Connect**: Extends OAuth2 with identity verification

### HTTPS Requirement

⚠️ **Important**: OAuth2 doesn't specify encryption. Always use HTTPS in production.

---

## First Steps

### Installation

Ensure FastAPI is installed with security dependencies:

```bash
pip install "fastapi[standard]"
pip install python-multipart
```

### Basic OAuth2 Setup

Create a simple OAuth2 password bearer scheme:

```python
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

# Creates a bearer token scheme
# tokenUrl is the relative path where clients get tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    The token is automatically extracted from the Authorization header.
    Header format: "Authorization: Bearer <token>"
    Returns 401 if missing or invalid.
    """
    return {"token": token}
```

### How It Works

1. **Client Request**: Browser sends `Authorization: Bearer <token>`
2. **FastAPI Extraction**: OAuth2PasswordBearer extracts the token
3. **Validation**: Your function receives the token as a string
4. **Auto-docs**: Interactive documentation shows "Authorize" button

### Interactive Documentation

Run your app and visit `/docs`:
- See an "Authorize" button
- Lock icon on protected endpoints
- Test authentication directly in the UI

---

## Getting Current User

### Architecture

Instead of just getting a token, extract user information:

```
Request → Extract Token → Decode Token → Get User → Return User
```

### Step 1: Create User Model

```python
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
```

### Step 2: Create Utility Functions

```python
def fake_decode_token(token: str):
    """
    Decode token and return user.
    In production: verify JWT signature, check expiration, etc.
    """
    return User(
        username=token + "fakedecoded",
        email="john@example.com",
        full_name="John Doe"
    )
```

### Step 3: Create Dependency Chain

```python
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    """
    Dependency that:
    1. Gets token from oauth2_scheme
    2. Decodes the token
    3. Returns User object
    """
    user = fake_decode_token(token)
    return user
```

### Step 4: Use in Endpoints

```python
@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """Returns the authenticated user's data."""
    return current_user
```

### Dependency Injection Benefits

- **Reusability**: Use `get_current_user` in any endpoint
- **Composability**: Chain dependencies together
- **Testability**: Easy to mock in tests
- **DRY**: Write security logic once

---

## Password Flow with Bearer Tokens

### Complete Flow Diagram

```
1. User enters username/password in UI
   ↓
2. Frontend sends to /token endpoint
   ↓
3. Backend validates credentials
   ↓
4. Returns {"access_token": "...", "token_type": "bearer"}
   ↓
5. Frontend stores token temporarily
   ↓
6. For subsequent requests, sends: Authorization: Bearer <token>
   ↓
7. Backend validates token, processes request
   ↓
8. Token expires after set time, user must re-login
```

### Implementation

#### Step 1: Set Up Form Input

```python
from fastapi.security import OAuth2PasswordRequestForm

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    OAuth2PasswordRequestForm provides:
    - username: str
    - password: str
    - scope: str (optional, space-separated)
    - grant_type: str (optional)
    - client_id: str (optional)
    - client_secret: str (optional)
    """
    pass
```

#### Step 2: Create Database Models

```python
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

# Fake database (use real DB in production)
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}
```

#### Step 3: Implement Login Logic

```python
def fake_hash_password(password: str) -> str:
    """Hash password (use bcrypt/argon2 in production)."""
    return "fakehashed" + password

def get_user(db: dict, username: str):
    """Retrieve user from database."""
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None

def authenticate_user(db: dict, username: str, password: str):
    """Validate username and password."""
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def verify_password(plain: str, hashed: str) -> bool:
    """Verify password against hash."""
    return fake_hash_password(plain) == hashed
```

#### Step 4: Create Token Endpoint

```python
from typing import Annotated
from fastapi import HTTPException, status

@app.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    Endpoint where clients POST username/password to get token.
    Called when user clicks "Authorize" in docs.
    """
    user_dict = fake_users_db.get(form_data.username)
    
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    
    if hashed_password != user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # In production, return JWT token instead of username
    return {"access_token": user.username, "token_type": "bearer"}
```

#### Step 5: Add User Status Check

```python
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """Check if user is active (not disabled)."""
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    """Retrieve authenticated user's profile."""
    return current_user
```

### Testing the Flow

**In interactive docs (/docs):**

1. Click "Authorize" button
2. Enter username: `johndoe`, password: `secret`
3. Try GET `/users/me` to see your profile
4. Try with disabled user `alice` to see error handling

---

## JWT Tokens with Password Hashing

### What is JWT?

JWT (JSON Web Tokens) is a standard for encoding data securely.

**Format**: `header.payload.signature`

**Example**:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U
```

**Key Properties**:
- ✓ Verifiable (signed, can't be tampered with)
- ✓ Expirable (includes expiration time)
- ✗ Not encrypted (anyone can read contents)

### Installation

```bash
pip install pyjwt
pip install "pwdlib[argon2]"  # Secure password hashing
```

### Complete Implementation

#### Configuration

```python
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel

# Generate with: openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize password hasher
password_hash = PasswordHash.recommended()  # Uses Argon2
```

#### Password Hashing Functions

```python
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plaintext password against hash."""
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate secure hash of password."""
    return password_hash.hash(password)

# Example:
# hashed = get_password_hash("mypassword")
# verify_password("mypassword", hashed)  # True
```

#### Token Creation

```python
def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:
    """
    Create JWT token with optional expiration.
    
    Args:
        data: Claims to encode (e.g., {"sub": "username"})
        expires_delta: Token lifetime (default: 15 minutes)
    
    Returns:
        Signed JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
    return encoded_jwt
```

#### Token Validation

```python
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    """
    Validate JWT token and return user.
    
    Raises:
        HTTPException: If token invalid, expired, or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode and verify signature
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        
        # Extract username from "sub" claim
        username: str | None = payload.get("sub")
        
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username)
        
    except InvalidTokenError:
        raise credentials_exception
    
    # Get user from database
    user = get_user(fake_users_db, username=token_data.username)
    
    if user is None:
        raise credentials_exception
    
    return user
```

#### Login Endpoint with JWT

```python
@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    Create access token for user.
    
    Called by frontend to exchange username/password for JWT.
    """
    user = authenticate_user(
        fake_users_db,
        form_data.username,
        form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Set token expiration
    access_token_expires = timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    # Create JWT
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer"
    )
```

#### Models

```python
class Token(BaseModel):
    """Token response model."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Decoded token claims."""
    username: str | None = None

class User(BaseModel):
    """User data model."""
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    """User with password hash (internal only)."""
    hashed_password: str
```

### Why Hash Passwords?

| Scenario | Unhashed | Hashed |
|----------|----------|--------|
| Database stolen | Passwords exposed | Hashes revealed (cannot reverse) |
| User reuses password | Account compromised everywhere | Single account compromised |
| Compliance | Violates GDPR, PCI-DSS | Meets security standards |

### JWT Subject Claim ("sub")

The JWT spec defines `sub` for the token subject (typically the user ID):

```python
# Standard approach
{"sub": "johndoe"}

# To avoid collisions with other entities:
{"sub": "user:johndoe"}  # Prefix with entity type
```

---

## Advanced Topics

### OAuth2 with Scopes

Scopes define granular permissions:

```python
@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """User can only see their own items."""
    return [{"item_id": "Foo", "owner": current_user.username}]
```

**Common Scopes**:
- `read:users` - Read user data
- `write:users` - Modify user data
- `read:items` - List items
- `admin:all` - Full admin access

### Refresh Tokens

For long-lived sessions without constant re-authentication:

```python
@app.post("/token/refresh")
async def refresh_token(
    refresh_token: str
) -> Token:
    """Exchange refresh token for new access token."""
    # Validate refresh token
    # Issue new short-lived access token
    pass
```

### Third-Party Authentication

Integrate with external providers:

```python
# Example: Google OAuth2
GOOGLE_CLIENT_ID = "..."
GOOGLE_CLIENT_SECRET = "..."

async def get_current_user_google(token: str):
    """Validate token from Google."""
    # Call Google API to verify token
    # Get user info
    pass
```

### Role-Based Access Control (RBAC)

```python
class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    VIEWER = "viewer"

class User(BaseModel):
    username: str
    role: UserRole

async def get_admin_user(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    """Ensure user is admin."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

@app.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    admin: Annotated[User, Depends(get_admin_user)]
):
    """Only admins can delete users."""
    # Delete user
    pass
```

---

## Best Practices

### 1. **Never Log Passwords**

```python
# ✗ Bad
logger.info(f"User login: {username}:{password}")

# ✓ Good
logger.info(f"User login attempt: {username}")
```

### 2. **Use HTTPS in Production**

```python
# Development
uvicorn main:app --reload

# Production
uvicorn main:app --ssl-keyfile=key.pem --ssl-certfile=cert.pem
```

### 3. **Rotate Secrets Regularly**

```python
# Store in environment variables, not code
import os
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
```

### 4. **Implement Rate Limiting**

```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.post("/token")
@limiter.limit("5/minute")
async def login(request: Request, ...):
    """Prevent brute force attacks."""
    pass
```

### 5. **Add CORS Configuration**

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 6. **Use Strong Hashing Algorithms**

| Algorithm | Status | Note |
|-----------|--------|------|
| MD5 | ✗ Broken | Never use |
| SHA-1 | ✗ Broken | Never use |
| bcrypt | ✓ Good | Legacy support |
| Argon2 | ✓ Best | Modern standard |
| scrypt | ✓ Good | Alternative |

### 7. **Token Expiration Strategy**

```python
# Short-lived access tokens (security)
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# Long-lived refresh tokens (convenience)
REFRESH_TOKEN_EXPIRE_DAYS = 7
```

### 8. **Timing Attack Prevention**

```python
from pwdlib import PasswordHash

# Always verify against dummy hash if user not found
DUMMY_HASH = password_hash.hash("dummypassword")

def authenticate_user(db, username, password):
    user = get_user(db, username)
    if not user:
        # Still verify to take same time
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
```

### 9. **Validate Token Claims**

```python
async def get_current_user(token: str):
    """
    Validate:
    - Signature (not tampered)
    - Expiration (not expired)
    - Issuer (trusted source)
    - User exists (not deleted)
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(detail="Invalid token")
```

### 10. **Audit Logging**

```python
import logging

logger = logging.getLogger(__name__)

@app.post("/token")
async def login(form_data):
    """Log authentication attempts."""
    try:
        user = authenticate_user(db, form_data.username, form_data.password)
        logger.info(f"Successful login: {form_data.username}")
        return token
    except Exception as e:
        logger.warning(f"Failed login: {form_data.username}")
        raise
```

---

## Complete Example

### Full Application Code

```python
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel

# Configuration
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize
password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

# Database
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": password_hash.hash("secret"),
        "disabled": False,
    }
}

# Utilities
def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)

def get_user(db: dict, username: str):
    if username in db:
        return UserInDB(**db[username])

def authenticate_user(db: dict, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Dependencies
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise exception
    except InvalidTokenError:
        raise exception
    
    user = get_user(fake_users_db, username)
    if user is None:
        raise exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Routes
@app.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
        )
    token = create_access_token(
        {"sub": user.username},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

@app.get("/users/me/items/")
async def read_own_items(current_user: Annotated[User, Depends(get_current_active_user)]):
    return [{"item_id": "Foo", "owner": current_user.username}]
```

---

## Troubleshooting

### Common Issues

**Q: "Could not validate credentials"**
- Token expired? Check expiration time
- Wrong secret key? Use same key for encode/decode
- Token tampered? Invalid signature detected

**Q: User can access without authentication**
- Dependency not used? Check `Depends(oauth2_scheme)`
- Missing `async`? Use `async` for dependencies

**Q: Password verification always fails**
- Hash algorithm mismatch? Use consistent algorithm
- Plaintext password stored? Always hash before comparing

---

## Resources

- [FastAPI Security Docs](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT.io](https://jwt.io) - JWT debugger and information
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OAuth2 Specification](https://tools.ietf.org/html/rfc6749)

---

**Document Version**: 1.0  
**Last Updated**: May 2026  
**Status**: Ready for contribution