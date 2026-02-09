import pandas as pd
from acesso import obter_conexao
from dataframe_traduzido import carregar_e_traduzir

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

    print("Analisando mês com maior volume de vendas (valor total)...")
    try:
        df = carregar_e_traduzir("dados_banco.xlsx")
        df["data_compra"] = pd.to_datetime(df["data_compra"], errors="coerce")

        df_validos = df.dropna(subset=["data_compra", "pagamento_total"])
        if df_validos.empty:
            print("Não foram encontrados dados de vendas no DataFrame.")
            return

        nomes_meses = [
            "janeiro",
            "fevereiro",
            "marco",
            "abril",
            "maio",
            "junho",
            "julho",
            "agosto",
            "setembro",
            "outubro",
            "novembro",
            "dezembro",
        ]

        def formatar_brl(valor: float) -> str:
            return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        df_validos["mes"] = df_validos["data_compra"].dt.month
        total_por_mes = df_validos.groupby("mes")["pagamento_total"].sum()
        mes_max = int(total_por_mes.idxmax())
        total_max = float(total_por_mes.loc[mes_max])
        nome_mes = nomes_meses[mes_max - 1] if 1 <= mes_max <= 12 else str(mes_max)
        print(
            f"O mês com maior volume de vendas foi: {nome_mes} "
            f"com total de {formatar_brl(total_max)}."
        )
    except Exception as e:
        print(f"Erro na análise do volume de vendas: {e}")

if __name__ == "__main__":
    analisar_mes_maior_vendas()
