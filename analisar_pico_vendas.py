from acesso import obter_conexao

def analisar_mes_maior_vendas():
    print("Analisando mês com maior quantidade de vendas...")
    conexao = obter_conexao()
    
    if conexao and conexao.is_connected():
        try:
            cursor = conexao.cursor()
            
            # Agrupa por Ano-Mês usando a data de compra e conta os pedidos
            sql = """
                SELECT DATE_FORMAT(order_purchase_timestamp, '%m') as mes, 
                       COUNT(*) as total_pedidos
                FROM olist_orders_dataset
                GROUP BY mes
                ORDER BY total_pedidos DESC
                LIMIT 1
            """
            
            cursor.execute(sql)
            resultado = cursor.fetchone()
            
            if resultado:
                mes, total = resultado
                print(f"O mês com maior quantidade de vendas foi: {mes} com {total} pedidos.")
            else:
                print("Não foram encontrados dados de vendas.")
                
            cursor.close()
            conexao.close()
        except Exception as e:
            print(f"Erro na análise: {e}")
    else:
        print("Não foi possível conectar ao banco.")

if __name__ == "__main__":
    analisar_mes_maior_vendas()