from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from chatbot import get_models, upload_pdf, ask_ollama
from database import login
from config import UPLOAD_FOLDER
import os, shutil

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="odf_ai_chatbot_secret_key_2026")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    if request.session.get("logged_in"):
        return RedirectResponse("/home", status_code=303)
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


@app.post("/login")
async def login_user(request: Request, username: str = Form(...), password: str = Form(...)):
    if login(username, password):
        request.session["logged_in"] = True
        return RedirectResponse("/home", status_code=303)
    return RedirectResponse("/", status_code=303)


@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    if not request.session.get("logged_in"):
        return RedirectResponse("/", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "models": get_models()
        }
    )


@app.post("/upload")
async def upload(request: Request, files: list[UploadFile] = File(...)):
    if not request.session.get("logged_in"):
        return JSONResponse({"message": ["Please login first."]}, status_code=401)

    messages = []

    for file in files:
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        messages.append(upload_pdf(path))

    return JSONResponse({"message": messages})


@app.post("/ask")
async def ask(request: Request, question: str = Form(...), model: str = Form(...)):
    if not request.session.get("logged_in"):
        return JSONResponse({"answer": "Please login first."}, status_code=401)

    answer, source = ask_ollama(question, model)

    return JSONResponse({
        "answer": answer,
        "source": source
    })


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)
