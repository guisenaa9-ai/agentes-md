<h1 align="center">AI Agents Hub - Agentes de IA para Cada Departamento da Empresa</h1>  

> Este repositório reúne uma coleção de agentes de inteligência artificial especializados para apoiar as operações de diferentes setores de uma empresa, incluindo Marketing, Recursos Humanos, Financeiro, Logística, Comercial, e muito mais.

---

🎯 **Objetivo:**  
O principal objetivo deste repositório é fornecer agentes de IA prontos para uso, desenvolvidos para otimizar e automatizar processos em diversas áreas funcionais. Cada agente foi projetado para lidar com desafios específicos de um departamento, reduzindo trabalho manual e aumentando a eficiência operacional.  

💡 **Benefícios:**  
- **Automação Inteligente:** Os agentes ajudam a reduzir tarefas repetitivas e melhorar a tomada de decisões baseada em dados.  
- **Precisão e Eficiência:** Modelos de IA especializados para cada área garantem respostas rápidas e contextualizadas.  
- **Integração e Escalabilidade:** Os agentes podem ser integrados a sistemas internos e escalados conforme a necessidade do negócio.  
- **Aprendizado Contínuo:** Melhorias constantes nos modelos garantem respostas cada vez mais precisas.  

📂 **Departamentos Atendidos:**  
Este repositório contém agentes de IA para os seguintes setores:  
1. **Marketing** - Análises de tendências, segmentação de público, automação de campanhas.  
2. **Recursos Humanos (RH)** - Triagem de currículos, suporte a colaboradores, análise de clima organizacional.  
3. **Financeiro** - Previsão de fluxo de caixa, detecção de anomalias, automação de relatórios.  
4. **Logística** - Otimização de rotas, rastreamento de pedidos, previsão de demanda.  
5. **Operação** - Monitoramento de processos, detecção de falhas, otimização de eficiência.  
6. **Comercial** - Assistência na gestão de vendas, análise de concorrência, recomendação de produtos.  
7. **Data Insights** - Análise avançada de dados, construção de dashboards, insights preditivos.  
8. **Jurídico** - Análise de contratos, revisão de documentos, compliance automatizado.  
9. **Suporte** - Chatbots para atendimento, análise de feedbacks, priorização de chamados.  
10. **Pricing** - Modelagem de preços dinâmicos, análise de elasticidade de preço.  
11. **Fraud Prevention** - Detecção de fraudes, monitoramento de transações suspeitas.  
12. **ESG (Environmental, Social, and Governance)** - Análise de impacto ambiental, relatórios de sustentabilidade.  

## Stack Tecnológica  
- **CrewAI** - Framework de orquestração de agentes de IA que permite criar, coordenar e gerenciar equipes de agentes autônomos.  
- **FastAPI** - Framework web Python moderno, rápido e assíncrono para construção de APIs com validação automática, documentação interativa e excelente performance, permitindo a integração eficiente entre agentes de IA e sistemas externos.  
- **LLMs** - Google Gemini (gratuito), Ollama (local) ou OpenAI GPT, configuráveis pelo `.env`.  

## Como Usar  
1. Clone este repositório:  
   ```bash
   git clone https://github.com/guisenaa9-ai/agentes-md.git
   cd agentes-md
   ```
2. Instale as dependências:  
   ```bash
   pip install -r requirements.txt
   ```
3. Configure o modelo e a chave de API:  
   ```bash
   cp .env_example .env
   ```
   Escolha o modelo na variável `MODEL` do `.env` e preencha a chave correspondente:
   - **Gemini (gratuito):** `MODEL=gemini/gemini-2.5-flash` + `GEMINI_API_KEY`, gerada sem cartão em https://aistudio.google.com/apikey. O plano gratuito tem limite de requisições por minuto e por dia, e o Google pode usar os dados enviados para melhorar os modelos. Evite dados sensíveis.
   - **Ollama (gratuito, local):** instale em https://ollama.com, rode `ollama pull llama3.1` e use `MODEL=ollama/llama3.1`. Os dados não saem do seu computador, mas exige uma máquina com boa memória.
   - **OpenAI (pago):** `MODEL=gpt-4.1-mini` + `OPENAI_API_KEY`, gerada em https://platform.openai.com/api-keys.

   A `SERPER_API_KEY` é opcional e habilita busca na web no agente de Marketing.
4. Execute o agente desejado:  
   ```bash
   python run_agent.py --department marketing --input "Lançamento de um app de finanças pessoais"
   ```
5. Ou suba a API e chame os agentes via HTTP:  
   ```bash
   uvicorn api:app --reload
   curl -X POST http://localhost:8000/agentes/marketing \
        -H "Content-Type: application/json" \
        -d '{"solicitacao": "Lançamento de um app de finanças pessoais"}'
   ```
   A documentação interativa fica em `http://localhost:8000/docs`.

   Para o agente Financeiro, é possível anexar um arquivo de dados (CSV ou TXT) à solicitação:  
   ```bash
   python run_agent.py --department financeiro --input "Projete o caixa dos próximos 3 meses" --file extrato.csv
   ```

Agentes disponíveis no momento:
- **Financeiro** (`financeiro`) - análise e projeção de fluxo de caixa, detecção de anomalias e relatório executivo. Os agentes usam apenas os dados enviados e declaram as premissas quando falta informação.
- **Marketing** (`marketing`) - tendências de mercado, público-alvo e plano de campanha.

Para adicionar um departamento, crie um módulo em `agentes/` com uma função `executar(solicitacao: str) -> str` e registre-o em `agentes/__init__.py`.

## Usar pelo navegador (sem instalar nada)

O arquivo `app.py` é uma interface web em Streamlit: escolha o departamento, escreva a solicitação e, se quiser, envie um CSV ou uma planilha Excel. O relatório aparece na tela e pode ser baixado.

Para publicar gratuitamente no **Streamlit Community Cloud**:
1. Acesse https://share.streamlit.io e entre com a conta do GitHub.
2. Clique em **Create app** → **Deploy a public app from GitHub**.
3. Preencha: repositório `guisenaa9-ai/agentes-md`, branch `main`, arquivo `app.py`.
4. Em **Advanced settings**, escolha Python **3.12** e cole em **Secrets**:
   ```toml
   MODEL = "gemini/gemini-2.5-flash"
   GEMINI_API_KEY = "sua-chave-aqui"
   APP_PASSWORD = "uma-senha-forte"
   ```
5. Clique em **Deploy**. Em alguns minutos o app fica disponível em um link `https://....streamlit.app`.

A `APP_PASSWORD` é recomendada: sem ela, qualquer pessoa com o link consegue usar o app e consumir a cota da sua chave.

Para rodar a interface localmente: `streamlit run app.py`.

## 🤝 Contribuições  
Contribuições são bem-vindas! Se você tem ideias para novos agentes ou melhorias, siga os passos abaixo:  

1. **Faça um fork** deste repositório.  
2. **Crie uma nova branch** para sua funcionalidade:  
   ```bash
   git checkout -b feature/novo-agente
   ```
3. **Adicione ou melhore agentes de IA em qualquer departamento** e faça o commit:  
   ```bash
   git commit -m "Adiciona novo agente de IA para [departamento]"
   ```
4. **Faça o push para seu repositório remoto:**  
   ```bash
   git push origin feature/novo-agente
   ```
5. **Abra um Pull Request** e envie sua contribuição!  


## Contribuições Específicas que Buscamos  
- **Novos agentes de IA especializados para setores empresariais.**  
- **Templates de Prompt Engineering para otimização dos agentes.**  
- **Casos de uso e aplicações reais para cada departamento.**  

---

## Entre em Contato  
Se você tiver dúvidas ou sugestões, entre em contato ou abra uma issue no repositório.  

🔗 **Criado por:** [Thiago Silva](https://www.linkedin.com/in/thiagosilvafarias/)  
