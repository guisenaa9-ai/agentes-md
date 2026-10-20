"""API FastAPI para executar os agentes.

Inicie com:
    uvicorn api:app --reload
"""

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel

from agentes import DEPARTAMENTOS, executar

load_dotenv()

app = FastAPI(title="AI Agents Hub")


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
