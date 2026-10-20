"""Agente de Marketing: análise de tendências, público-alvo e campanhas."""

import os

from crewai import Agent, Crew, Process, Task


def _ferramentas() -> list:
    # A busca na web só é habilitada quando há chave do Serper configurada.
    if not os.getenv("SERPER_API_KEY"):
        return []
    from crewai_tools import SerperDevTool

    return [SerperDevTool()]


def criar_crew() -> Crew:
    analista = Agent(
        role="Analista de Marketing",
        goal="Identificar tendências e oportunidades de mercado relevantes para a solicitação",
        backstory=(
            "Especialista em pesquisa de mercado e comportamento do consumidor, "
            "com experiência em transformar dados em recomendações práticas."
        ),
        tools=_ferramentas(),
        verbose=False,
    )
    estrategista = Agent(
        role="Estrategista de Campanhas",
        goal="Transformar a análise de mercado em um plano de campanha acionável",
        backstory=(
            "Profissional de marketing digital que planeja campanhas multicanal "
            "com foco em segmentação de público e resultados mensuráveis."
        ),
        verbose=False,
    )

    analise = Task(
        description=(
            "Analise a seguinte solicitação de marketing: {solicitacao}\n"
            "Levante tendências do mercado, perfil do público-alvo e principais concorrentes."
        ),
        expected_output="Relatório com tendências, público-alvo e concorrentes, em tópicos.",
        agent=analista,
    )
    plano = Task(
        description=(
            "Com base na análise, proponha um plano de campanha para: {solicitacao}"
        ),
        expected_output=(
            "Plano de campanha em português com objetivo, público, canais, "
            "mensagens-chave e métricas de sucesso."
        ),
        agent=estrategista,
        context=[analise],
    )

    return Crew(
        agents=[analista, estrategista],
        tasks=[analise, plano],
        process=Process.sequential,
    )


def executar(solicitacao: str) -> str:
    resultado = criar_crew().kickoff(inputs={"solicitacao": solicitacao})
    return str(resultado)
