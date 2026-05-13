from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pyotp
import time

app = FastAPI()

# Generate a single static secret for the lifetime of this server run
SECRET = pyotp.random_base32()
totp = pyotp.TOTP(SECRET)

@app.get("/", response_class=HTMLResponse)
def get_index():
    with open("index.html", "r") as f:
        return f.read()

@app.get("/code")
def get_code():
    return {"code": totp.now()}

@app.get("/verify/{code}")
def verify_code(code: str):
    valid = totp.verify(code)
    return {"valid": valid}
