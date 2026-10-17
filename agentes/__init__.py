"""Registro dos agentes de IA disponíveis por departamento."""

from collections.abc import Callable

from agentes import financeiro, marketing

# Cada departamento expõe uma função que recebe a solicitação do usuário
# e devolve a resposta final dos agentes em texto.
DEPARTAMENTOS: dict[str, Callable[[str], str]] = {
    "financeiro": financeiro.executar,
    "marketing": marketing.executar,
}


def executar(departamento: str, solicitacao: str) -> str:
    """Executa o agente do departamento informado."""
    try:
        executar_departamento = DEPARTAMENTOS[departamento]
    except KeyError:
        disponiveis = ", ".join(sorted(DEPARTAMENTOS))
        raise ValueError(
            f"Departamento '{departamento}' não encontrado. Disponíveis: {disponiveis}"
        ) from None
    return executar_departamento(solicitacao)


def anexar_dados(solicitacao: str, nome_arquivo: str, conteudo: str) -> str:
    """Acrescenta o conteúdo de um arquivo de dados à solicitação."""
    return f"{solicitacao}\n\nDados do arquivo {nome_arquivo}:\n{conteudo}"
