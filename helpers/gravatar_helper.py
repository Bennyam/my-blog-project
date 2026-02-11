import hashlib

def gravatar_url(email, size=100, default="identicon"):
    email = email.strip().lower()
    hash = hashlib.md5(email.encode("utf-8")).hexdigest()
    return f"https://www.gravatar.com/avatar/{hash}?s={size}&d={default}"