import pandas as pd
import os

def analisar_review_excel():
    # Define o caminho do arquivo (assumindo a mesma pasta do projeto)
    # O arquivo ~$dados_banco.xlsx é temporário, usamos o arquivo real dados_banco.xlsx
    caminho_arquivo = r"c:\Users\Leonardo\Documents\Harve - Análise de Dados\Projeto Final\dados_banco.xlsx"
    
    print(f"Lendo arquivo Excel: {caminho_arquivo}...")
    
    if os.path.exists(caminho_arquivo):
        try:
            # Lê o arquivo Excel (requer bibliotecas: pip install pandas openpyxl)
            df = pd.read_excel(caminho_arquivo)
            
            if 'review_score' in df.columns:
                # Converte a coluna para numérico, transformando erros (texto, vazios, espaços) em NaN
                scores_validos = pd.to_numeric(df['review_score'], errors='coerce')
                
                # Verifica quais valores NÃO estão na lista de válidos [1, 2, 3, 4, 5]
                # O operador ~ inverte a seleção, contando NaNs, zeros, e outros números fora do intervalo
                qtd_diferentes = (~scores_validos.isin([1, 2, 3, 4, 5])).sum()
                
                print(f"Total de linhas com 'review_score' diferente de 1, 2, 3, 4, 5: {qtd_diferentes}")
            else:
                print("A coluna 'review_score' não foi encontrada na planilha.")
                
        except Exception as e:
            print(f"Erro ao processar o arquivo Excel: {e}")
    else:
        print("Arquivo não encontrado. Verifique se o nome está correto e se o arquivo existe na pasta.")

if __name__ == "__main__":
    analisar_review_excel()