"""Executa um agente pela linha de comando.

Exemplo:
    python run_agent.py --department marketing --input "Lançamento de um app de finanças pessoais"
    python run_agent.py --department financeiro --input "Analise o caixa do trimestre" --file extrato.csv
"""

import argparse
from pathlib import Path

from dotenv import load_dotenv

from agentes import DEPARTAMENTOS, anexar_dados, executar


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa um agente de IA por departamento.")
    parser.add_argument("--department", required=True, choices=sorted(DEPARTAMENTOS))
    parser.add_argument("--input", help="Solicitação para o agente (pergunta interativamente se omitida).")
    parser.add_argument("--file", type=Path, help="Arquivo de dados (CSV, TXT) anexado à solicitação.")
    args = parser.parse_args()

    load_dotenv()
    solicitacao = args.input or input("Descreva sua solicitação: ")
    if args.file:
        dados = args.file.read_text(encoding="utf-8")
        solicitacao = anexar_dados(solicitacao, args.file.name, dados)
    print(executar(args.department, solicitacao))


if __name__ == "__main__":
    main()
