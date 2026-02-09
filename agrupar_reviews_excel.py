import pandas as pd
import os

def agrupar_reviews_excel():
    # O arquivo com prefixo ~$ é temporário. Lemos o arquivo original dados_banco.xlsx
    caminho_arquivo = r"c:\Users\Leonardo\Documents\Harve - Análise de Dados\Projeto Final\dados_banco.xlsx"
    
    print(f"Lendo arquivo para agrupamento: {caminho_arquivo}...")
    
    if os.path.exists(caminho_arquivo):
        try:
            df = pd.read_excel(caminho_arquivo)
            
            if 'review_score' in df.columns:
                print("\n--- Contagem de valores em 'review_score' ---")
                # dropna=False garante que valores nulos (NaN) também sejam contados
                agrupamento = df['review_score'].value_counts(dropna=False)
                print(agrupamento)
            else:
                print("Coluna 'review_score' não encontrada no arquivo.")
                
        except Exception as e:
            print(f"Erro ao processar arquivo: {e}")
    else:
        print("Arquivo não encontrado.")

if __name__ == "__main__":
    agrupar_reviews_excel()