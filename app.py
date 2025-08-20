from fastapi import FastAPI, Response
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import base64

app = FastAPI(title="Basic Token API", version="1.0.0")

TOKEN_B64 = os.getenv(
    "TOKEN_B64",
    "NzA5MzE2NDcyMTpoMzY2OTdDcGg0cnpVVmJVbGliNDRPQldOa2dsbXRwWA=="
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

def try_decode(b64str: str) -> str | None:
    try:
        return base64.b64decode(b64str).decode("utf-8", errors="strict")
    except Exception:
        return None

@app.get("/", response_class=JSONResponse)
def root():
    decoded = try_decode(TOKEN_B64)
    return {
        "ok": True,
        "token_base64": TOKEN_B64,
        "decoded": decoded  # ممكن تكون None لو مش Base64 صحيح
    }

@app.get("/token", response_class=PlainTextResponse)
def token_plain():
    return TOKEN_B64

@app.get("/auth-header", response_class=JSONResponse)
def auth_header():
    # بيرجع الهيدر كـ JSON + بيحطه فعلاً في الاستجابة
    hdr_val = f"Basic {TOKEN_B64}"
    resp = JSONResponse({"Authorization": hdr_val})
    resp.headers["Authorization"] = hdr_val
    return resp

@app.get("/healthz", response_class=JSONResponse)
def health():
    return {"status": "ok"}
