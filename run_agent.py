"""Executa um agente pela linha de comando.

Exemplo:
    python run_agent.py --department marketing --input "Lançamento de um app de finanças pessoais"
"""

import argparse

from dotenv import load_dotenv

from agentes import DEPARTAMENTOS, executar


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa um agente de IA por departamento.")
    parser.add_argument("--department", required=True, choices=sorted(DEPARTAMENTOS))
    parser.add_argument("--input", help="Solicitação para o agente (pergunta interativamente se omitida).")
    args = parser.parse_args()

    load_dotenv()
    solicitacao = args.input or input("Descreva sua solicitação: ")
    print(executar(args.department, solicitacao))


if __name__ == "__main__":
    main()
