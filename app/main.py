from fastapi import FastAPI, Header, Response, Request, Cookie
from fastapi.responses import JSONResponse

app = FastAPI(title="QA CTF: Block 1 - HTTP & Architecture")

# --- Middleware для Лабы №4 (Response Headers) ---
@app.middleware("http")
async def add_debug_header(request: Request, call_next):
    response = await call_next(request)
    # Имитируем забытый дебаг-хедер
    response.headers["X-Debug-Token"] = "FLAG{VERBOSE_HEADERS_LEAK}"
    return response

# --- Лаба №1: HTTP Methods ---
@app.api_route("/api/v1/user/me", methods=["GET", "DELETE"])
async def user_profile(request: Request):
    if request.method == "DELETE":
        return JSONResponse(
            status_code=403,
            content={"error": "Access Denied", "hint": "FLAG{METHOD_NOT_RESTRICTED}"}
        )
    return {"user": "student_qa", "role": "guest", "status": "active"}

# --- Лаба №2: User-Agent Spoofing ---
@app.get("/api/v1/news")
async def secure_news(user_agent: str = Header(None)):
    if user_agent == "QuestOS/1.0":
        return {
            "news": "Secret company news: we are moving to Mars!",
            "flag": "FLAG{USER_AGENT_SPOOFING}"
        }
    return {"message": "Access restricted. Only for QuestOS users."}

# --- Лаба №3: Cookie Manipulation ---
@app.post("/api/v1/login")
async def login(response: Response):
    # Устанавливаем обычную куку при логине
    response.set_cookie(key="role", value="user")
    return {"message": "Logged in successfully"}

@app.get("/api/v1/admin")
async def admin_panel(role: str = Cookie(None)):
    if role == "admin":
        return {"welcome": "Admin Console", "flag": "FLAG{COOKIE_MANIPULATION_MASTER}"}
    return JSONResponse(status_code=403, content={"error": "You are not an admin!"})