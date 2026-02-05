from acesso import obter_conexao

def inspecionar_linha_321():
    print("Inspecionando a linha 321 da tabela olist_order_reviews_dataset...")
    conexao = obter_conexao()
    
    if conexao and conexao.is_connected():
        try:
            cursor = conexao.cursor()
            # LIMIT 1 OFFSET 320 pega a 321ª linha (baseado em índice 0)
            # Nota: A ordem exata depende de como o banco armazena, pois não usamos ORDER BY
            sql = "SELECT * FROM olist_order_reviews_dataset LIMIT 1 OFFSET 320"
            cursor.execute(sql)
            colunas = [desc[0] for desc in cursor.description]
            linha = cursor.fetchone()
            
            if linha:
                print("\nDados da linha 321:")
                for col, val in zip(colunas, linha):
                    print(f"{col}: {val}")
            else:
                print("Linha 321 não encontrada.")
                
            cursor.close()
            conexao.close()
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    inspecionar_linha_321()