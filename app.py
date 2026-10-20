"""Interface web dos agentes, feita com Streamlit.

Rode localmente com:
    streamlit run app.py
"""

import hmac
import io
import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
# No Streamlit Community Cloud as chaves ficam em "Secrets"; copia para o
# ambiente, que é de onde o CrewAI lê o modelo e as chaves de API.
try:
    for chave, valor in st.secrets.items():
        if isinstance(valor, str):
            os.environ.setdefault(chave, valor)
except FileNotFoundError:
    pass

from agentes import DEPARTAMENTOS, anexar_dados, executar  # noqa: E402

st.set_page_config(page_title="AI Agents Hub", page_icon="🤖")


def senha_correta() -> bool:
    """Exige APP_PASSWORD, quando configurada, antes de liberar o app."""
    senha = os.getenv("APP_PASSWORD")
    if not senha or st.session_state.get("autenticado"):
        return True
    digitada = st.text_input("Senha", type="password")
    if digitada and hmac.compare_digest(digitada, senha):
        st.session_state["autenticado"] = True
        st.rerun()
    elif digitada:
        st.error("Senha incorreta.")
    return False


def ler_arquivo(arquivo) -> str:
    """Converte o arquivo enviado em texto (planilhas viram CSV)."""
    if arquivo.name.lower().endswith((".xlsx", ".xls")):
        planilhas = pd.read_excel(arquivo, sheet_name=None)
        return "\n\n".join(
            f"Aba {nome}:\n{tabela.to_csv(index=False)}" for nome, tabela in planilhas.items()
        )
    dados = arquivo.getvalue()
    try:
        return dados.decode("utf-8")
    except UnicodeDecodeError:
        # CSV exportado pelo Excel em português costuma vir em Windows-1252.
        return dados.decode("cp1252")


st.title("🤖 AI Agents Hub")

if not senha_correta():
    st.stop()

with st.form("solicitacao"):
    departamento = st.selectbox(
        "Departamento", sorted(DEPARTAMENTOS), format_func=str.capitalize
    )
    solicitacao = st.text_area(
        "Solicitação",
        placeholder="Ex.: Projete o caixa dos próximos 3 meses e aponte riscos de liquidez.",
        height=150,
    )
    arquivo = st.file_uploader(
        "Arquivo de dados (opcional)", type=["csv", "txt", "xlsx", "xls"]
    )
    enviado = st.form_submit_button("Executar", type="primary")

if enviado:
    if not solicitacao.strip():
        st.warning("Descreva sua solicitação antes de executar.")
        st.stop()
    texto = solicitacao
    if arquivo:
        texto = anexar_dados(texto, arquivo.name, ler_arquivo(arquivo))
    with st.spinner("Os agentes estão trabalhando, isso pode levar alguns minutos..."):
        try:
            resposta = executar(departamento, texto)
        except Exception as erro:
            st.error(f"Erro ao executar o agente: {erro}")
            st.stop()
    st.markdown(resposta)
    st.download_button(
        "Baixar relatório", io.BytesIO(resposta.encode("utf-8")),
        file_name=f"relatorio_{departamento}.md", mime="text/markdown",
    )
