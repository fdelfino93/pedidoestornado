from acesso import obter_conexao

def analisar_mes_maiores_pagamentos():
    print("Analisando mês com maior valor total de pagamentos...")
    conexao = obter_conexao()
    
    if conexao and conexao.is_connected():
        try:
            cursor = conexao.cursor()
            
            # Realiza o JOIN entre pedidos e pagamentos para somar o valor por mês
            # Agrupa apenas pelo mês (01 a 12), somando todos os anos
            sql = """
                SELECT DATE_FORMAT(o.order_purchase_timestamp, '%m') as mes, 
                       SUM(p.payment_value) as total_payment
                FROM olist_orders_dataset o
                JOIN olist_order_payments_dataset p ON o.order_id = p.order_id
                GROUP BY mes
                ORDER BY total_payment DESC
                LIMIT 1
            """
            
            cursor.execute(sql)
            resultado = cursor.fetchone()
            
            if resultado:
                mes, total = resultado
                print(f"O mês com maiores pagamentos foi: {mes} com R$ {total:,.2f}")
            else:
                print("Não foram encontrados dados de pagamentos.")
                
            cursor.close()
            conexao.close()
        except Exception as e:
            print(f"Erro na análise: {e}")
    else:
        print("Não foi possível conectar ao banco.")

if __name__ == "__main__":
    analisar_mes_maiores_pagamentos()