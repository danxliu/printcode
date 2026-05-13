from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pyotp
import time

app = FastAPI()

# Generate a single static secret for the lifetime of this server run
SECRET = pyotp.random_base32()
totp = pyotp.TOTP(SECRET)

HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <title>TOTP Generator</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            font-family: sans-serif;
            background-color: #f0f0f0;
        }
        #code {
            font-size: 8rem;
            font-weight: bold;
            margin-bottom: 2rem;
            color: #333;
            letter-spacing: 0.2rem;
        }
        progress {
            width: 80%;
            max-width: 600px;
            height: 2rem;
        }
    </style>
</head>
<body>
    <div id="code">------</div>
    <progress id="pb" value="30" max="30"></progress>
    
    <script>
        const codeDiv = document.getElementById('code');
        const pb = document.getElementById('pb');
        
        async function fetchCode() {
            try {
                const res = await fetch('/code');
                const data = await res.json();
                codeDiv.textContent = data.code;
            } catch (e) {
                console.error('Failed to fetch code');
            }
        }
        
        let currentInterval = -1;
        
        function tick() {
            const now = Date.now() / 1000;
            const interval = Math.floor(now / 30);
            
            if (interval !== currentInterval) {
                currentInterval = interval;
                fetchCode();
            }
            
            const remaining = 30 - (now % 30);
            pb.value = remaining;
            
            requestAnimationFrame(tick);
        }
        
        // Start loop
        requestAnimationFrame(tick);
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def get_index():
    return HTML_CONTENT

@app.get("/code")
def get_code():
    return {"code": totp.now()}

@app.get("/verify/{code}")
def verify_code(code: str):
    valid = totp.verify(code)
    return {"valid": valid}
