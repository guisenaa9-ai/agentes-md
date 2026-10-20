"""Agente Financeiro: fluxo de caixa, detecção de anomalias e relatórios."""

from crewai import Agent, Crew, Process, Task

# Os agentes trabalham apenas com os dados fornecidos na solicitação;
# esta regra evita que inventem valores ausentes.
REGRA_DADOS = (
    "Use somente os números fornecidos na solicitação. Quando faltar informação, "
    "declare a premissa adotada ou indique o dado necessário, sem inventar valores."
)


def criar_crew() -> Crew:
    analista_caixa = Agent(
        role="Analista de Fluxo de Caixa",
        goal="Analisar entradas e saídas e projetar o fluxo de caixa dos próximos períodos",
        backstory=(
            "Analista de tesouraria com experiência em projeções de caixa, "
            "capital de giro e sazonalidade de receitas e despesas."
        ),
        verbose=False,
    )
    auditor = Agent(
        role="Analista de Riscos e Anomalias",
        goal="Identificar lançamentos atípicos, inconsistências e riscos financeiros",
        backstory=(
            "Auditor com experiência em controles internos, conciliação "
            "e detecção de desvios em dados financeiros."
        ),
        verbose=False,
    )
    controller = Agent(
        role="Controller",
        goal="Consolidar as análises em um relatório executivo claro e acionável",
        backstory=(
            "Controller responsável por reportar a saúde financeira da empresa "
            "à diretoria, com foco em indicadores e recomendações objetivas."
        ),
        verbose=False,
    )

    fluxo = Task(
        description=(
            "Analise a seguinte solicitação financeira: {solicitacao}\n"
            "Avalie entradas, saídas, saldo e tendências, e projete o fluxo de caixa "
            "para os próximos períodos quando houver dados suficientes.\n" + REGRA_DADOS
        ),
        expected_output=(
            "Análise do fluxo de caixa com saldo, principais variações, "
            "projeção e premissas utilizadas."
        ),
        agent=analista_caixa,
    )
    anomalias = Task(
        description=(
            "Com base nos dados de: {solicitacao}\n"
            "Aponte lançamentos atípicos, variações fora do padrão, possíveis "
            "duplicidades e riscos de liquidez.\n" + REGRA_DADOS
        ),
        expected_output="Lista de anomalias e riscos, cada um com evidência e grau de severidade.",
        agent=auditor,
        context=[fluxo],
    )
    relatorio = Task(
        description=(
            "Consolide as análises de fluxo de caixa e de riscos em um relatório "
            "executivo para a solicitação: {solicitacao}"
        ),
        expected_output=(
            "Relatório executivo em português com resumo, indicadores-chave, "
            "riscos, recomendações e próximos passos."
        ),
        agent=controller,
        context=[fluxo, anomalias],
    )

    return Crew(
        agents=[analista_caixa, auditor, controller],
        tasks=[fluxo, anomalias, relatorio],
        process=Process.sequential,
    )


def executar(solicitacao: str) -> str:
    resultado = criar_crew().kickoff(inputs={"solicitacao": solicitacao})
    return str(resultado)
