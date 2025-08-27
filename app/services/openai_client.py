import json
import time
from typing import Any, Dict

from openai import OpenAI, APIConnectionError, RateLimitError, BadRequestError, APIStatusError
from app.core.config import settings

_client = OpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT = """Você é um assistente que classifica emails como Produtivo ou Improdutivo e sugere uma resposta.
Definições:
- Produtivo: requer ação/resposta específica (suporte, dúvida técnica, atualização de caso).
- Improdutivo: não requer ação imediata (felicitações, agradecimentos simples).

Instruções:
- Seja objetivo.
- Não invente informações.
- Se houver múltiplos assuntos, aplique a categoria mais exigente em termos de ação (priorize Produtivo).
- O campo resposta_sugerida deve ser redigido no mesmo idioma do email original, a menos que o email esteja em português; nesse caso, responda em português.
- Responda **apenas** com JSON válido no formato exigido.
"""

FEW_SHOTS = [
    {
        "role": "user",
        "content": "Olá, poderiam verificar o status do ticket #1234? O sistema ainda cai quando tento exportar relatórios."
    },
    {
        "role": "assistant",
        "content": json.dumps({
            "categoria": "Produtivo",
            "justificativa": "Solicitação de verificação de ticket com problema técnico.",
            "topicos": ["status do ticket", "erro ao exportar"],
            "resposta_sugerida": "Olá! Obrigado pelo retorno. Verificaremos o status do ticket #1234 e retornaremos com uma atualização. Se possível, envie horário aproximado do último erro e o navegador utilizado."
        }, ensure_ascii=False)
    },
    {
        "role": "user",
        "content": "Bom dia, parabéns à equipe pelo novo portal, ficou excelente!"
    },
    {
        "role": "assistant",
        "content": json.dumps({
            "categoria": "Improdutivo",
            "justificativa": "Mensagem de congratulações, sem ação solicitada.",
            "topicos": ["felicitações", "elogio"],
            "resposta_sugerida": "Muito obrigado pela mensagem! Ficamos felizes com o feedback. Permanecemos à disposição."
        }, ensure_ascii=False)
    },
]

JSON_INSTRUCTIONS = (
    "Formato JSON obrigatório:\n"
    '{"categoria":"Produtivo|Improdutivo","justificativa":"...","topicos":["..."],"resposta_sugerida":"..."}'
)

def _build_user_prompt(email_text: str) -> str:
    return (
        f"Texto do email a analisar:\n---\n{email_text}\n---\n"
        "Na resposta_sugerida, use tom formal, claro e profissional. "
        f"{JSON_INSTRUCTIONS}"
    )

def _call_chat_json_mode(messages: list[dict[str, Any]], model: str) -> str:
    backoff = 1.0
    last_err: Exception | None = None
    for _ in range(4):
        try:
            resp = _client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.2,
                response_format={"type": "json_object"},
            )
            return resp.choices[0].message.content or "{}"
        except (RateLimitError, APIConnectionError) as e:
            last_err = e
            time.sleep(backoff)
            backoff *= 2
        except (BadRequestError, APIStatusError) as e:
            raise e
    if last_err:
        raise last_err
    raise RuntimeError("Falha desconhecida ao chamar a API.")

def classify_and_suggest(email_text: str) -> Dict[str, Any]:
    """
    Usa Chat Completions em JSON Mode com validação.
    Tenta primeiro o modelo do .env; se der erro de modelo, tenta 'gpt-4o-mini'.
    """
    base_messages = [{"role": "system", "content": SYSTEM_PROMPT}, *FEW_SHOTS,
                     {"role": "user", "content": _build_user_prompt(email_text)}]

    model_to_try = [settings.OPENAI_MODEL, "gpt-4o-mini"]
    last_raw = "{}"

    for mdl in model_to_try:
        if not mdl:
            continue
        try:
            last_raw = _call_chat_json_mode(base_messages, mdl)
            break
        except (BadRequestError, APIStatusError):
            continue

    try:
        parsed = json.loads(last_raw)
        if parsed.get("categoria") not in ("Produtivo", "Improdutivo"):
            parsed["categoria"] = "Produtivo"
        parsed.setdefault("resposta_sugerida", "")
        parsed.setdefault("justificativa", "")
        parsed.setdefault("topicos", [])
        return parsed
    except Exception:
        return {
            "categoria": "Produtivo",
            "justificativa": "Fallback aplicado (não foi possível interpretar o JSON).",
            "topicos": [],
            "resposta_sugerida": (
                "Olá! Recebemos sua mensagem e vamos analisá-la. "
                "Se possível, compartilhe detalhes adicionais para agilizar o atendimento."
            )
        }
