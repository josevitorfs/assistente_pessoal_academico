# Assistente Pessoal Acadêmico (JARVIS Acadêmico)

Projeto desenvolvido para a disciplina de Inteligência Artificial, com o objetivo de construir um assistente acadêmico inteligente utilizando técnicas modernas de IA generativa, RAG (Retrieval-Augmented Generation), Tool Calling e integração com Large Language Models (LLMs).

O sistema foi desenvolvido com foco em auxiliar estudantes na organização acadêmica, consulta de materiais de estudo e gerenciamento de tarefas, utilizando a LLM Gemma 12B disponibilizada pela disciplina.

---

# Instalação

## 1. Clonar o repositório

```bash
git clone https://github.com/koddart/assistente_pessoal_academico.git
```

---

## 2. Acessar a pasta

```bash
cd assistente_pessoal_academico
```

---

## 3. Criar ambiente virtual

### Windows

```bash
python -m venv venv
```

---

## 4. Ativar ambiente virtual

### PowerShell

```bash
venv\Scripts\Activate.ps1
```

### CMD

```bash
venv\Scripts\activate.bat
```

---

## 5. Instalar dependências

```bash
pip install -r requirements.txt
```

---

# Configuração da API

Criar um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY="sua_chave"
OPENAI_BASE_URL="sua_base_url"
MODEL_NAME=seu_modelo
```

---

# Execução

Executar o sistema:

```bash
python -m app.main
```

---

# Testes

Executar os testes:

```bash
pytest
```

---

# Objetivo do Projeto

O projeto busca desenvolver um sistema capaz de responder perguntas sobre materiais acadêmicos, consultar compromissos acadêmicos, gerenciar tarefas, integrar recuperação semântica com geração de respostas e utilizar múltiplas ferramentas controladas pela LLM.

Além da implementação funcional, o projeto também busca aplicar conceitos de engenharia de software, modularização e separação de responsabilidades.

---

# Tecnologias Utilizadas

## Linguagem

* Python 3.11

## LLM

* Google Gemma 3 12B IT
* API disponibilizada pela disciplina

## Bibliotecas Principais

* openai
* sentence-transformers
* scikit-learn
* PyMuPDF
* pytest
* python-dotenv

---

# Estrutura do Projeto

```text
assistente_pessoal_academico/
│
├── app/
│   ├── main.py
│   │
│   ├── llm/
│   │   └── client.py
│   │
│   ├── rag/
│   │   ├── ingest.py
│   │   ├── chunking.py
│   │   ├── embeddings.py
│   │   ├── vectordb.py
│   │   └── retrieval.py
│   │
│   ├── tools/
│   │   ├── agenda.py
│   │   ├── tarefas.py
│   │   ├── rag_tool.py
│   │   └── orquestrador.py
│   │
│   ├── memory/
│   │   ├── agenda.json
│   │   ├── tarefas.json
│   │   └── vector_store.pkl
│   │
│   └── logs/
│       └── tool_logs.json
│
├── data/
│   └── pdfs/
│
├── tests/
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

# Funcionalidades Implementadas

## 1. Consulta a Materiais Acadêmicos (RAG)

O sistema permite realizar perguntas sobre documentos acadêmicos armazenados localmente como por exemplo "Explique regressão logística", "O que são embeddings?", "Resuma o conteúdo sobre transformers".

Fluxo implementado:

1. Leitura de PDFs;
2. Extração de texto;
3. Chunking dos documentos;
4. Geração de embeddings;
5. Recuperação semântica;
6. Geração da resposta utilizando a Gemma 12B.

---

## 2. Agenda Acadêmica

O sistema permite consultar agenda, sendo que nessa estão compromissos acadêmicos armazenados localmente em JSON, com perguntas do tipo "O que tenho hoje?", "Tenho prova amanhã?", "Quais são minhas aulas esta semana?".

Porém, essa agenda foi implementada sem a capacidade de alteração de eventos (CRUD), sendo harcoded esses eventos.

---

## 3. Lista de Tarefas

O sistema permite:

* adicionar tarefas;
* listar tarefas;
* concluir tarefas.

Para essa parte, o sistema entrega melhores respostas quando segue um estrutura correta, sendo necessário trabalhar melhor a generalização do

* "Adicionar tarefa estudar embeddings"
* "Listar tarefas"
* "Concluir tarefa 2"

---

# Implementação do RAG

## Ingestão de Documentos

Os documentos são carregados automaticamente da pasta:

```text
data/pdfs/
```

A leitura é realizada utilizando a biblioteca PyMuPDF.

---

## Estratégia de Chunking

Os documentos são divididos em pequenos blocos de texto para melhorar a precisão da recuperação, relevância contextual e qualidade das respostas da LLM. A estratégia utilizada consiste em divisão textual com tamanho fixo e sobreposição parcial entre chunks. Essa abordagem reduz perda de contexto e melhora a recuperação semântica.

---

## Embeddings

Os embeddings são gerados utilizando o modelo:

```text
sentence-transformers/all-MiniLM-L6-v2
```

E os vetores representam semanticamente os chunks de texto.

---

## Recuperação Semântica

A busca é realizada por similaridade de cosseno utilizando os embeddings armazenados localmente. Os chunks mais relevantes são enviados como contexto para a LLM.

---

# Tool Calling

O sistema implementa tool calling utilizando roteamento por LLM. A Gemma recebe a pergunta do usuário e decide qual ferramenta deve ser executada.

Ferramentas implementadas foram:

* consultar_agenda
* listar_tarefas
* adicionar_tarefa
* concluir_tarefa
* buscar_material_rag

---

# Logs

O sistema registra automaticamente quais foram as ferramentas utilizadas, as entradas recebidas, as saídas geradas e o timestamp da execução.

Os logs são armazenados em:

```text
app/logs/tool_logs.json
```

---

# Dataset

O dataset do projeto é composto por documentos acadêmicos focados em inteligência artificial, abrangendo tópicos como machine learning, deep learning, NLP, transformers e embeddings. Vale ressaltar que todo o material foi utilizado exclusivamente para fins acadêmicos e experimentais.

---

## Limitações do Sistema

Atualmente, o sistema apresenta algumas limitações técnicas e funcionais que são importantes de serem destacadas para uma avaliação correta do projeto.

### Armazenamento vetorial simplificado

A implementação do mecanismo de recuperação utiliza uma solução vetorial local e relativamente simples, adequada para a proposta do trabalho, mas ainda distante de uma estrutura mais robusta de produção. Isso significa que o sistema funciona bem para um conjunto reduzido de documentos, porém pode apresentar limitações de escalabilidade quando o volume de materiais cresce. Em cenários mais amplos, seria recomendável utilizar uma solução mais sofisticada de persistência e indexação vetorial.

### Ausência de interface gráfica

Neste momento, o sistema foi construído com foco na lógica central da aplicação, na integração com a LLM e na implementação das ferramentas exigidas pelo trabalho. Por esse motivo, ainda não há uma interface gráfica completa para o usuário final. A interação ocorre de forma mais técnica, o que é suficiente para validação funcional, mas reduz a experiência de uso. Uma interface visual tornaria a navegação mais intuitiva e facilitaria a demonstração do sistema.

### Limitação pela janela de contexto da LLM

A qualidade das respostas geradas depende diretamente da quantidade de contexto que pode ser enviada para a LLM. Como a janela de contexto do modelo é limitada, apenas os trechos mais relevantes recuperados pelo RAG são incluídos na resposta. Isso pode fazer com que informações importantes, mas menos relevantes na etapa de busca, sejam descartadas. Em documentos longos, esse fator pode comprometer parcialmente a cobertura da resposta.

### Dependência da qualidade dos documentos

O desempenho do sistema também depende fortemente da qualidade dos materiais inseridos no dataset. Documentos com textos mal formatados, conteúdo muito fragmentado, baixa clareza ou pouca organização tendem a prejudicar a extração, o chunking e a recuperação semântica. Dessa forma, quanto melhor for a estrutura dos documentos utilizados, maior tende a ser a precisão das respostas geradas.

### Recuperação baseada apenas em similaridade semântica

A etapa de busca recupera trechos com base principalmente na proximidade semântica entre a pergunta do usuário e os chunks armazenados. Embora essa abordagem seja eficiente e adequada para o escopo do projeto, ela ainda não considera mecanismos mais avançados, como reranking, ponderação por relevância estrutural ou análise de intenção mais refinada. Isso pode fazer com que, em algumas consultas ambíguas, o sistema recupere trechos semanticamente parecidos, mas não necessariamente os mais adequados para a resposta final.

---

# Ferramentas de IA Utilizadas no Desenvolvimento

Durante o desenvolvimento foram utilizadas ferramentas de apoio baseadas em IA para revisão e correção de código, identificação de bugs, auxílio arquitetural na fase inicial do projeto como organização do pipeline RAG e tambem na melhoria da modularização. Durante a fase inicial, o desenvolvimento foi realizado majoritariamente de forma manual, com apoio de pesquisas e consultas técnicas. A etapa de integração com a LLM apresentou maior dificuldade devido à quantidade de conceitos e ferramentas novas envolvidas no processo.

Ferramentas utilizadas:

* ChatGPT
* GitHub Copilot
* Gemini

---

# Considerações Finais

O projeto permitiu explorar conceitos modernos de Inteligência Artificial aplicada, especialmente técnicas de RAG, recuperação semântica, embeddings e integração de LLMs em aplicações reais.

Além da implementação funcional, o projeto buscou aplicar princípios de engenharia de software, modularização e separação de responsabilidades para garantir maior organização e extensibilidade do sistema.
