from acesso import obter_conexao

def analisar_avaliacoes():
    print("Analisando distribuição de avaliações (review_score)...")
    conexao = obter_conexao()

    if conexao and conexao.is_connected():
        try:
            cursor = conexao.cursor()
            
            # Agrupa por nota e conta a quantidade de ocorrências
            sql = """
                SELECT review_score, COUNT(*) as quantidade
                FROM olist_order_reviews_dataset
                GROUP BY review_score
                ORDER BY review_score DESC
            """
            
            cursor.execute(sql)
            resultados = cursor.fetchall()
            
            # Exibe quais valores crus foram encontrados no banco para depuração
            valores_encontrados = [str(r[0]) for r in resultados]
            print(f"Valores distintos encontrados na coluna: {valores_encontrados}")

            # Dicionário para armazenar contagens (garante que todas as notas apareçam mesmo se zeradas)
            contagem = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
            vazios = 0
            
            for nota, quantidade in resultados:
                eh_valido = False
                if nota is not None:
                    try:
                        # Converte para string, remove espaços e tenta converter para float depois int
                        # Isso resolve casos como "5.0", " 5 ", ou 5 (inteiro)
                        nota_str = str(nota).strip()
                        if nota_str:
                            nota_int = int(float(nota_str))
                            if nota_int in contagem:
                                contagem[nota_int] += quantidade
                                eh_valido = True
                    except ValueError:
                        pass # Se der erro na conversão, considera inválido/vazio
                
                if not eh_valido:
                    vazios += quantidade
            
            print("\n--- Quantidade de Avaliações por Nota ---")
            for i in range(5, 0, -1):
                print(f"Nota {i}: {contagem[i]} avaliações")
                
            print(f"Sem nota (Vazios/Nulos): {vazios} linhas")

            cursor.close()
            conexao.close()
        except Exception as e:
            print(f"Erro na análise: {e}")
    else:
        print("Não foi possível conectar ao banco.")

if __name__ == "__main__":
    analisar_avaliacoes()