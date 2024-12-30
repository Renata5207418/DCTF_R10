# 📄 Processador de Arquivos RFB

## 📌 Descrição
Este projeto é uma ferramenta automatizada para **processar arquivos .rfb**, extrair informações estruturadas e convertê-las para **formato JSON**. Foi desenvolvido para facilitar a manipulação e análise de dados fiscais em conformidade com a legislação brasileira.

---

## 🚀 Funcionalidades
- 🔍 **Leitura e Análise** de arquivos **.rfb**.
- 📑 Busca por registros com código específico (padrão: **R10**).
- 📊 **Extração de Dados** estruturados como **CNPJ**, valores monetários e datas.
- 🔄 **Exportação** dos dados para **JSON** e **SQLite**.
- 📂 Suporte a múltiplos arquivos no mesmo diretório.
- 🗂️ Armazenamento estruturado em banco de dados SQLite.
- 📋 Exibição de dados formatados com **Pandas**.

---

## 🛠️ Tecnologias Utilizadas
- **Python 3.12** – Linguagem principal.
- **JSON** – Exportação e manipulação dos dados.
- **Regex (re)** – Validação e extração de padrões de texto.
- **argparse** – Argumentos via terminal.
- **SQLite** – Armazenamento estruturado dos dados.
- **Pandas** – Visualização e manipulação tabular dos dados.
- **dotenv** – Gerenciamento de variáveis de ambiente.

---

## 📥 Instalação e Configuração

### 1. Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/processador-rfb.git
cd processador-rfb
```

### 2. Configurar o Ambiente

Crie um arquivo `.env` baseado no modelo fornecido em `.env.example`:
```env
# Exemplo de variáveis de ambiente
DATABASE_PATH=dados.sqlite3
```

Instale as dependências do projeto:
```bash
pip install -r requirements.txt
```

---

## 🧑‍💻 Como Usar

### 1. Processar Arquivos `.rfb`
Execute o script `extract_r10.py` para processar os arquivos `.rfb` em um diretório e exportar os dados para JSON:
```bash
python scripts/extract_r10.py <diretorio-dos-arquivos> --codigo R10
```

### 2. Importar Dados JSON para o Banco de Dados
Use o script `banco_dados_r10.py` para importar os dados JSON para o SQLite:
```bash
python scripts/banco_dados_r10.py <diretorio-dos-arquivos>
```

### 3. Exibir Dados no Banco de Dados
O script `banco_dados_r10.py` também permite visualizar os dados importados:
```bash
python scripts/banco_dados_r10.py <diretorio-dos-arquivos>
```
---

## ⚠️ Observações
- Certifique-se de que os arquivos `.rfb` estão no formato correto.
- O código padrão para extração é `R10`, mas pode ser ajustado com o parâmetro `--codigo`.
- Não esqueça de configurar as variáveis de ambiente antes de executar os scripts.

---

