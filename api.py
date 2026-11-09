"""API FastAPI para executar os agentes.

Inicie com:
    uvicorn api:app --reload

Toda chamada exige o cabeçalho "Authorization: Bearer <API_TOKEN>".
"""

import hmac
import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel

from agentes import DEPARTAMENTOS, executar

load_dotenv()



def exigir_token(authorization: str = Header(default="")) -> None:
    """Libera a chamada só com o token de API_TOKEN; sem ele configurado, recusa tudo."""
    token = os.getenv("API_TOKEN")
    if not token:
        raise HTTPException(status_code=503, detail="API_TOKEN não configurado no servidor.")
    if not hmac.compare_digest(authorization.encode(), f"Bearer {token}".encode()):
        raise HTTPException(status_code=401, detail="Token inválido ou ausente.")


app = FastAPI(title="AI Agents Hub", dependencies=[Depends(exigir_token)])


class Solicitacao(BaseModel):
    solicitacao: str


class Resposta(BaseModel):
    departamento: str
    resposta: str


@app.get("/agentes")
def listar_agentes() -> list[str]:
    return sorted(DEPARTAMENTOS)


@app.post("/agentes/{departamento}", response_model=Resposta)
async def executar_agente(departamento: str, corpo: Solicitacao) -> Resposta:
    if departamento not in DEPARTAMENTOS:
        raise HTTPException(status_code=404, detail=f"Departamento '{departamento}' não encontrado.")
    # A execução da Crew é síncrona e demorada; roda fora do event loop.
    resposta = await run_in_threadpool(executar, departamento, corpo.solicitacao)
    return Resposta(departamento=departamento, resposta=resposta)
