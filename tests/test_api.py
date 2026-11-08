import sys
from types import SimpleNamespace

from fastapi.testclient import TestClient

# Executor simulado: o teste não chama a IA nem precisa do CrewAI instalado.
sys.modules["agentes"] = SimpleNamespace(
    DEPARTAMENTOS={"marketing": None},
    executar=lambda departamento, solicitacao: f"ok {departamento}",
)

import api  # noqa: E402

cliente = TestClient(api.app)
CORPO = {"solicitacao": "teste"}


def test_sem_api_token_configurado_recusa_tudo(monkeypatch):
    monkeypatch.delenv("API_TOKEN", raising=False)
    assert cliente.get("/agentes", headers={"Authorization": "Bearer x"}).status_code == 503


def test_token_errado_ou_ausente_recebe_401(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "segredo")
    assert cliente.post("/agentes/marketing", json=CORPO).status_code == 401
    errado = cliente.post("/agentes/marketing", json=CORPO, headers={"Authorization": "Bearer outro"})
    assert errado.status_code == 401


def test_token_certo_executa_o_agente(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "segredo")
    r = cliente.post("/agentes/marketing", json=CORPO, headers={"Authorization": "Bearer segredo"})
    assert r.status_code == 200 and r.json() == {"departamento": "marketing", "resposta": "ok marketing"}
