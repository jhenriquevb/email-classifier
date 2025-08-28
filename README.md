# Email Classifier

Uma aplicação web para classificação inteligente de emails utilizando processamento de linguagem natural e inteligência artificial.

## Sobre o Projeto

O Email Classifier é uma ferramenta que automatiza a análise e classificação de emails, categorizando-os como "Produtivo" ou "Improdutivo" e sugerindo respostas apropriadas. A aplicação utiliza modelos de IA da OpenAI para fornecer análises precisas e sugestões contextuais.

### Funcionalidades Principais

- **Classificação Automática**: Categoriza emails como Produtivo (requer ação) ou Improdutivo (informativo)
- **Sugestão de Respostas**: Gera respostas profissionais adequadas ao contexto
- **Processamento de Arquivos**: Suporte para upload de arquivos PDF e TXT
- **Interface Intuitiva**: Interface web responsiva com drag-and-drop
- **Processamento de Linguagem Natural**: Pré-processamento avançado de texto
- **Análise de Tópicos**: Identificação automática dos principais assuntos do email

## Tecnologias Utilizadas

- **Backend**: FastAPI
- **IA**: OpenAI
- **NLP**: spaCy (modelo pt_core_news_sm)
- **Processamento de PDF**: PyPDF2
- **Gerenciamento de Dependências**: UV

## Pré-requisitos

- Python >= 3.10
- Chave de API da OpenAI
- Modelo spaCy em português: `pt_core_news_sm`

## Instalação

1. **Instale o UV** (se ainda não tiver)
   
   Siga as instruções em: https://docs.astral.sh/uv/getting-started/installation/

2. **Clone o repositório**
   ```bash
   git clone https://github.com/jhenriquevb/email-classifier.git
   cd email-classifier
   ```

3. **Instale as dependências**
   ```bash
   uv sync
   ```

4. **Instale o modelo spaCy**
   ```bash
   python -m spacy download pt_core_news_sm
   ```

4. **Configure as variáveis de ambiente**
   
   Crie um arquivo `.env` na raiz do projeto:
   ```env
   OPENAI_API_KEY=sua_chave_openai_aqui
   OPENAI_MODEL=gpt-4o-mini
   ```

## Como Executar

1. **Inicie o servidor**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Acesse a aplicação**
   
   Abra seu navegador e acesse: `http://localhost:8000`

## Como Usar

1. Acesse a aplicação no navegador
2. **Opção 1**: Cole o texto do email diretamente na área de texto
3. **Opção 2**: Faça upload de um arquivo PDF ou TXT
4. Clique em "Processar e Classificar"
5. Visualize os resultados:
   - Categoria (Produtivo/Improdutivo)
   - Justificativa da classificação
   - Tópicos identificados
   - Resposta sugerida

## Arquitetura do Projeto

```
email-classifier/
├── app/
│   ├── core/
│   │   └── config.py          # Configurações da aplicação
│   ├── services/
│   │   ├── nlp.py            # Processamento de linguagem natural
│   │   └── openai_client.py  # Cliente OpenAI
│   ├── static/
│   │   ├── css/              # Estilos CSS
│   │   └── js/               # Scripts JavaScript
│   ├── templates/
│   │   ├── index.html        # Página principal
│   │   └── result.html       # Página de resultados
│   ├── utils/
│   │   └── pdf.py            # Utilitários para PDF
│   └── main.py               # Aplicação FastAPI
├── pyproject.toml            # Configuração do projeto
└── uv.lock                   # Lock file das dependências
```

## Configuração

### Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|---------|
| `OPENAI_API_KEY` | Chave da API OpenAI | Obrigatório |
| `OPENAI_MODEL` | Modelo GPT a utilizar | `gpt-4.1-mini` |

### Modelos de IA Suportados

- `gpt-4.1-mini` (recomendado)
- Outros modelos compatíveis com Chat Completions

## Critérios de Classificação

### Produtivo
- Emails que requerem ação específica
- Suporte técnico
- Dúvidas que precisam de resposta
- Atualizações de casos/tickets
- Solicitações de informações

### Improdutivo  
- Mensagens informativas
- Agradecimentos simples
- Felicitações
- Comunicados gerais sem necessidade de resposta

## Processamento de Texto

A aplicação realiza pré-processamento avançado incluindo:

- **Limpeza**: Normalização de espaços e quebras de linha
- **Anonimização**: Substituição de emails, URLs, datas, horários e números por tokens
- **Lematização**: Redução de palavras à forma canônica
- **Remoção de Stopwords**: Eliminação de palavras funcionais
- **Filtragem POS**: Manutenção apenas de substantivos, verbos, adjetivos, advérbios e nomes próprios