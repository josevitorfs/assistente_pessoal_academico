# Assistente Pessoal Acadêmico (JARVIS Acadêmico)

Projeto desenvolvido para a disciplina de Inteligência Artificial, com o objetivo de construir um assistente acadêmico inteligente utilizando técnicas modernas de IA generativa, RAG (Retrieval-Augmented Generation), Tool Calling e integração com Large Language Models (LLMs).

O sistema foi desenvolvido com foco em auxiliar estudantes na organização acadêmica, consulta de materiais de estudo e gerenciamento de tarefas, utilizando a LLM Gemma 12B disponibilizada pela disciplina.

---

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/koddart/assistente_pessoal_academico.git
```

### 2. Acessar a pasta

```bash
cd assistente_pessoal_academico
```

### 3. Criar ambiente virtual

#### Windows

```bash
python -m venv venv
```

### 4. Ativar ambiente virtual

#### PowerShell

```bash
venv\Scripts\Activate.ps1
```

#### CMD

```bash
venv\Scripts\activate.bat
```

### 5. Instalar dependências

```bash
pip install -r requirements.txt
```

## Configuração da API

Criar um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY="sua_chave"
OPENAI_BASE_URL="sua_base_url"
MODEL_NAME=seu_modelo
```


## Execução

Executar o sistema:

```bash
python -m app.main
```


## Testes

O projeto utiliza `pytest` para validar os principais módulos da aplicação. Os testes cobrem a leitura de documentos, chunking, persistência vetorial, recuperação semântica, agenda, tarefas e a camada de integração com a LLM.

Para executar a suíte completa:

```bash
python -m pytest
```
`test_llm.py`

Valida a comunicação com a LLM Gemma 12B, verificando envio de prompts e recebimento de respostas.

`test_ingest.py`

Testa a leitura e carregamento dos documentos acadêmicos utilizados no RAG.
`test_chunking.py`

Verifica o funcionamento da divisão dos documentos em chunks de texto.

`test_embeddings.py`

Valida a geração de embeddings semânticos a partir dos chunks textuais.


`test_vectordb.py`

Testa o armazenamento local dos embeddings na base vetorial.


 `test_retrieval.py`

Verifica a recuperação semântica de chunks relevantes para perguntas do usuário.


 `test_agenda.py`

Valida o funcionamento das consultas relacionadas à agenda acadêmica.


`test_tarefas.py`

Testa as funcionalidades de gerenciamento e listagem de tarefas.


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

## 2. Agenda Acadêmica

O sistema permite consultar agenda, sendo que nessa estão compromissos acadêmicos armazenados localmente em JSON, com perguntas do tipo "O que tenho hoje?", "Tenho prova amanhã?", "Quais são minhas aulas esta semana?".

Atualmente, os eventos da agenda são previamente definidos no arquivo JSON utilizado pelo sistema, não havendo ainda funcionalidades completas de edição dinâmica (CRUD).

## 3. Lista de Tarefas

O sistema permite:

* adicionar tarefas;
* listar tarefas;
* concluir tarefas.

Para essa funcionalidade, o sistema apresenta melhores resultados quando as instruções seguem uma estrutura mais objetiva. Ainda existe necessidade de melhorar a capacidade de generalização das interpretações feitas pela LLM para comandos menos explícitos ou mais ambíguos.

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


## Estratégia de Chunking

Os documentos são divididos em pequenos blocos de texto para melhorar a precisão da recuperação, relevância contextual e qualidade das respostas da LLM. A estratégia utilizada consiste em divisão textual com tamanho fixo e sobreposição parcial entre chunks. Essa abordagem reduz perda de contexto e melhora a recuperação semântica.


## Embeddings

Os embeddings são gerados utilizando o modelo:

```text
sentence-transformers/all-MiniLM-L6-v2
```

E os vetores representam semanticamente os chunks de texto.


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

# Limitações do Sistema

Atualmente, o sistema apresenta algumas limitações relacionadas à escalabilidade, usabilidade e recuperação de informações.

A implementação utiliza um armazenamento vetorial local e simplificado, adequado para pequenos conjuntos de documentos, mas limitado para cenários maiores. Além disso, o sistema ainda não possui interface gráfica, tornando a interação mais técnica.

Outro ponto importante é a limitação da janela de contexto da LLM, o que faz com que apenas parte dos trechos recuperados possa ser utilizada na geração das respostas. O desempenho também depende diretamente da qualidade dos documentos utilizados no dataset.

Por fim, a recuperação de informações é baseada principalmente em similaridade semântica, sem técnicas mais avançadas de reranking ou refinamento contextual.

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
