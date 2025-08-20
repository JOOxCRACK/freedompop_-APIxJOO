from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(title="Token+Telegram API", version="1.0.0")

# === ثوابتك ===
TOKEN_B64    = "NzA5MzE2NDcyMTpoMzY2OTdDcGg0cnpVVmJVbGliNDRPQldOa2dsbXRwWA=="
TG_BOT_TOKEN = "8496267640:AAH-dyEX0h3qKFroSijTCvBPULsqU_lZDdE"
TG_CHAT_ID   = "5169610078"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

async def notify(text: str):
    try:
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
        async with httpx.AsyncClient(timeout=5) as client:
            await client.post(url, json={"chat_id": TG_CHAT_ID, "text": text})
    except Exception:
        pass

@app.get("/", response_class=JSONResponse)
def root():
    return {"ok": True, "token": TOKEN_B64}

@app.get("/token", response_class=PlainTextResponse)
async def token_plain():
    return TOKEN_B64

@app.get("/token/{payload:path}", response_class=PlainTextResponse)
async def token_with_payload(payload: str, request: Request):
    ip = request.headers.get("x-forwarded-for", request.client.host)
    ua = request.headers.get("user-agent", "")
    await notify(f"payload: {payload}\nip: {ip}\nua: {ua}")
    return TOKEN_B64

@app.middleware("http")
async def token_suffix_capture(request: Request, call_next):
    path = request.url.path
    if path.startswith("/token") and path != "/token" and not path.startswith("/token/"):
        payload = path[len("/token"):]
        ip = request.headers.get("x-forwarded-for", request.client.host)
        ua = request.headers.get("user-agent", "")
        await notify(f"payload: {payload}\nip: {ip}\nua: {ua}")
        return PlainTextResponse(TOKEN_B64)
    return await call_next(request)

@app.get("/healthz")
def health():
    return {"status": "ok"}
