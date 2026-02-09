from acesso import obter_conexao
import statistics
from datetime import datetime

def calcular_metricas_entrega():
    print("Calculando métricas de entrega (Aprovação -> Entrega)...")
    conexao = obter_conexao()
    
    if conexao and conexao.is_connected():
        try:
            cursor = conexao.cursor()
            # Seleciona as datas, garantindo que não sejam nulas
            # Usamos o nome correto da tabela: olist_orders_dataset
            sql = """
                SELECT order_approved_at, order_delivered_customer_date, order_estimated_delivery_date
                FROM olist_orders_dataset
                WHERE order_approved_at IS NOT NULL 
                AND order_status = 'delivered'
            """
            cursor.execute(sql)
            dados = cursor.fetchall()
            
            tempos_entrega = []
            
            for aprovacao, entrega, estimativa in dados:
                # Converte strings para datetime caso o banco retorne texto
                if isinstance(aprovacao, str):
                    aprovacao = datetime.strptime(aprovacao, '%Y-%m-%d %H:%M:%S')
                if isinstance(entrega, str):
                    entrega = datetime.strptime(entrega, '%Y-%m-%d %H:%M:%S')
                if isinstance(estimativa, str):
                    estimativa = datetime.strptime(estimativa, '%Y-%m-%d %H:%M:%S')

                # Se a data de entrega for vazia, usa a estimativa
                if entrega is None:
                    entrega = estimativa

                # O conector MySQL retorna objetos datetime. Calculamos a diferença.
                # Verificamos se a entrega ocorreu após a aprovação para evitar dados inconsistentes
                if entrega and aprovacao and entrega >= aprovacao:
                    diferenca = entrega - aprovacao
                    # Converte a diferença para dias (inteiros)
                    dias = int(diferenca.total_seconds() / (24 * 3600))
                    tempos_entrega.append(dias)
            
            qtd = len(tempos_entrega)
            if qtd > 0:
                media = statistics.mean(tempos_entrega)
                mediana = statistics.median(tempos_entrega)
                
                print(f"\n--- Resultados ({qtd} pedidos analisados) ---")
                print(f"Tempo Médio de Entrega:   {int(media)} dias")
                print(f"Tempo Mediano de Entrega: {int(mediana)} dias")
            else:
                print("Não há dados válidos suficientes para o cálculo.")
                
            cursor.close()
            conexao.close()
            
        except Exception as e:
            print(f"Erro ao executar a consulta: {e}")
    else:
        print("Falha na conexão com o banco de dados.")

if __name__ == "__main__":
    calcular_metricas_entrega()