import os
import json
import sqlite3
import pandas as pd
import argparse

"""
Módulo para gerenciamento do banco de dados SQLite.

Funções principais:
- Criar tabelas para armazenar dados.
- Inserir e consultar registros.
- Conectar e fechar o banco de dados.
- Importar dados JSON e exibi-los formatados.
"""


def conectar_banco(banco_dados):
    """
    Conecta ao banco de dados SQLite especificado.

    Parâmetros:
    banco_dados (str): Caminho para o arquivo do banco de dados.

    Retorna:
    conn: Objeto de conexão com o banco de dados.
    """
    try:
        conn = sqlite3.connect(banco_dados)
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        exit(1)


def criar_tabela(conn):
    """
    Cria a tabela 'dados' no banco de dados, caso não exista.

    Parâmetros:
    conn: Objeto de conexão com o banco de dados.
    """
    try:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS dados (
            Tipo TEXT,
            CNPJ TEXT,
            MOFG TEXT,
            Situacao TEXT,
            Data_do_Evento TEXT,
            Grupo_de_Tributo TEXT,
            Codigo_da_Receita TEXT,
            Periodicidade TEXT,
            Ano TEXT,
            Mes TEXT,
            Dia TEXT,
            Ordem_do_Estabelecimento TEXT,
            CNPJ_CEI TEXT,
            Reservado_1 TEXT,
            Valor_do_Debito TEXT,
            Balanco_de_Reducao TEXT,
            Debito_dividido_em_quotas TEXT,
            Reservado_2 TEXT,
            Debito_de_SCP_INC TEXT,
            Reservado_3 TEXT,
            Delimitador_de_Registro TEXT
        )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao criar tabela: {e}")


def importar_dados_json_para_db(diretorio, conn):
    """
    Importa os dados de arquivos JSON encontrados no diretório especificado
    e os insere no banco de dados.

    Parâmetros:
    diretorio (str): Caminho para o diretório contendo os arquivos JSON.
    conn: Objeto de conexão com o banco de dados.
    """
    cursor = conn.cursor()

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".json"):
            caminho_arquivo = os.path.join(diretorio, arquivo)
            try:
                with open(caminho_arquivo, 'r', encoding='utf-8') as json_file:
                    dados = json.load(json_file)
                    for registro in dados:
                        cursor.execute('''
                        INSERT INTO dados (
                            Tipo, CNPJ, MOFG, Situacao, Data_do_Evento, Grupo_de_Tributo, Codigo_da_Receita,
                            Periodicidade, Ano, Mes, Dia, Ordem_do_Estabelecimento, CNPJ_CEI,
                            Reservado_1, Valor_do_Debito, Balanco_de_Reducao, Debito_dividido_em_quotas, Reservado_2,
                            Debito_de_SCP_INC, Reservado_3, Delimitador_de_Registro
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            registro.get('Tipo'), registro.get('CNPJ'), registro.get('MOFG'), registro.get('Situacao'),
                            registro.get('Data_do_Evento'), registro.get('Grupo_de_Tributo'),
                            registro.get('Codigo_da_Receita'),
                            registro.get('Periodicidade'), registro.get('Ano'), registro.get('Mes'), registro.get('Dia'),
                            registro.get('Ordem_do_Estabelecimento'), registro.get('CNPJ_CEI'),
                            registro.get('Reservado_1'), registro.get('Valor_do_Debito'),
                            registro.get('Balanco_de_Reducao'),
                            registro.get('Debito_dividido_em_quotas'), registro.get('Reservado_2'),
                            registro.get('Debito_de_SCP_INC'),
                            registro.get('Reservado_3'), registro.get('Delimitador_de_Registro')
                        ))
                print(f"Arquivo {arquivo} importado com sucesso!")
            except Exception as e:
                print(f"Erro ao processar {arquivo}: {e}")
    conn.commit()


def exibir_dados(conn):
    """
    Exibe os dados armazenados no banco de dados em formato tabular.

    Parâmetros:
    conn: Objeto de conexão com o banco de dados.
    """
    try:
        df = pd.read_sql_query("SELECT * FROM dados", conn)
        print(df.to_string(index=False))
    except Exception as e:
        print(f"Erro ao exibir dados: {e}")


def main():
    """
    Função principal que executa o fluxo do programa:
    - Recebe o diretório como argumento.
    - Cria e conecta ao banco de dados.
    - Cria a tabela e importa os dados JSON.
    - Exibe os dados importados.
    """
    parser = argparse.ArgumentParser(description="Importar dados JSON para SQLite")
    parser.add_argument('diretorio', type=str, help="Caminho do diretório contendo os arquivos JSON")
    args = parser.parse_args()

    banco_dados = 'dados.sqlite3'

    # Conectar ao banco e executar operações
    with conectar_banco(banco_dados) as conn:
        criar_tabela(conn)
        importar_dados_json_para_db(args.diretorio, conn)
        exibir_dados(conn)


if __name__ == "__main__":
    main()
