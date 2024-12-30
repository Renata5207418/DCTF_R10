import os
import re
import json
import argparse

"""
Módulo para extração e conversão de arquivos .rfb para JSON.

Funções principais:
- Encontrar linhas com código específico.
- Extrair dados formatados com base em um mapeamento.
- Exportar os dados em formato JSON.
- Lidar com múltiplos arquivos em um diretório.
"""


def encontrar_codigos(linhas, codigo):
    """
    Encontra índices das linhas que contêm um código específico.

    Parâmetros:
    linhas (list): Lista com as linhas do arquivo.
    codigo (str): Código a ser buscado nas primeiras 3 posições.

    Retorna:
    list: Índices das linhas que contêm o código especificado.
    """
    indices = []
    for idx, linha in enumerate(linhas):
        if linha[:3] == codigo:
            indices.append(idx)
    return indices


def extrair_dados(linhas, linha_codigo_idx):
    """
    Extrai dados formatados com base em um mapeamento predefinido.

    Parâmetros:
    linhas (list): Lista com as linhas do arquivo.
    linha_codigo_idx (list): Índices das linhas identificadas com o código.

    Retorna:
    list: Lista de dicionários contendo os dados extraídos.
    """
    dados_extraidos = []

    # Mapeamento das posições dos dados (linha, início, tamanho, tipo)
    mapeamento = {
        'Tipo': (0, 0, 3, 'X'),
        'CNPJ': (0, 3, 14, 'CNPJ'),
        'MOFG': (0, 17, 6, 'N'),
        'Situação': (0, 23, 1, 'N'),
        'Data do Evento': (0, 24, 8, 'DATA2'),
        'Valor do Débito': (0, 70, 14, 'R+')
    }

    # Regex para CNPJ
    padrao_cnpj = r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}"

    for idx in linha_codigo_idx:
        dados = {}
        for campo, (linha_offset, inicio, tamanho, tipo) in mapeamento.items():
            linha_idx = idx + linha_offset
            if linha_idx < len(linhas):
                fim = inicio + tamanho
                trecho = linhas[linha_idx][inicio:fim].strip()

                # Tratamento específico para campos
                if campo == 'Dia' and set(trecho) == {'0'}:
                    dados[campo] = ""
                elif tipo == 'CNPJ':
                    resultado = re.search(padrao_cnpj, trecho)
                    dados[campo] = resultado.group() if resultado else trecho
                else:
                    dados[campo] = trecho
        dados_extraidos.append(dados)

    return dados_extraidos


def ler_arquivos_txt(diretorio, codigo):
    """
    Processa arquivos no formato .rfb e exporta os dados para JSON.

    Parâmetros:
    diretorio (str): Caminho do diretório contendo os arquivos.
    codigo (str): Código a ser buscado nos arquivos.

    Retorna:
    None
    """
    arquivos_processados = 0

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".rfb"):
            caminho_arquivo = os.path.join(diretorio, arquivo)
            try:
                with open(caminho_arquivo, 'r', encoding='latin-1') as file:
                    linhas = file.readlines()
                    linha_codigo_indices = encontrar_codigos(linhas, codigo)
                    if linha_codigo_indices:
                        dados = extrair_dados(linhas, linha_codigo_indices)
                        if dados:
                            nome_arquivo_json = os.path.splitext(arquivo)[0] + '.json'
                            caminho_arquivo_json = os.path.join(diretorio, nome_arquivo_json)
                            with open(caminho_arquivo_json, 'w', encoding='utf-8') as json_file:
                                json.dump(dados, json_file, ensure_ascii=False, indent=4)
                            print(f"Dados exportados para {caminho_arquivo_json}")
                            arquivos_processados += 1
            except Exception as e:
                print(f"Erro ao processar {arquivo}: {e}")

    print(f"Processamento concluído! {arquivos_processados} arquivos convertidos.")


def main():
    """
    Função principal que configura argumentos e executa o processamento.
    """
    # Parser para entrada de argumentos
    parser = argparse.ArgumentParser(description="Processar arquivos .rfb e converter para JSON.")
    parser.add_argument('diretorio', type=str, help="Diretório contendo os arquivos .rfb")
    parser.add_argument('--codigo', type=str, default='R10', help="Código a ser buscado nos arquivos (padrão: R10)")

    args = parser.parse_args()

    # Executar processamento
    ler_arquivos_txt(args.diretorio, args.codigo)


if __name__ == "__main__":
    main()
