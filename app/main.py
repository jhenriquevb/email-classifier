from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.services.openai_client import classify_and_suggest
from app.utils.pdf import extract_text_from_pdf_bytes
from app.services import nlp

app = FastAPI(
    title="Email Classifier",
    version="1.0.0",
    description="A web application to classify emails.",
)

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/process", response_class=HTMLResponse)
async def process(
    request: Request,
    email_text: str = Form(None),
    file: UploadFile | None = File(None),
):
    text = (email_text or "").strip()
    if file and not text:
        content = await file.read()
        if file.filename.lower().endswith(".txt"):
            text = content.decode("utf-8", errors="ignore")
        elif file.filename.lower().endswith(".pdf"):
            text = extract_text_from_pdf_bytes(content)
        else:
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "error": "Tipo de arquivo não suportado. Por favor, envie um arquivo .txt ou .pdf.",
                },
            )

    if not text:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": "Por favor, cole o texto do e-mail ou envie um arquivo .txt/.pdf.",
            },
        )

    cleaned = nlp.clean_text(text)

    ai_result = classify_and_suggest(cleaned)

    result = {
        "categoria": ai_result.get("categoria", "Produtivo"),
        "justificativa": ai_result.get("justificativa", ""),
        "resposta_sugerida": ai_result.get("resposta_sugerida", ""),
        "topicos": ai_result.get("topicos", []),
    }

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "raw_text": text,
            "cleaned": cleaned,
            "result": result,
        },
    )


@app.get("/health")
def health_check():
    return {"status": "ok", "env": settings.ENV}
