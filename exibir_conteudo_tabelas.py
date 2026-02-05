from acesso import obter_conexao

def exibir_conteudo_tabelas():
    tabelas = [
        "olist_customers_dataset",
        "olist_geolocation_dataset",
        "olist_order_items_dataset",
        "olist_order_payments_dataset",
        "olist_order_reviews_dataset",
        "olist_orders_dataset",
        "olist_products_dataset",
        "olist_sellers_dataset"
    ]

    print("Conectando ao banco de dados...")
    conexao = obter_conexao()

    if conexao and conexao.is_connected():
        cursor = conexao.cursor()
        
        for tabela in tabelas:
            print(f"\n{'='*40}")
            print(f"Conteúdo da tabela: {tabela}")
            print(f"{'='*40}")
            try:
                # Limitando a 5 registros para evitar travar o terminal com muitos dados
                cursor.execute(f"SELECT * FROM {tabela} LIMIT 5")
                colunas = [desc[0] for desc in cursor.description]
                linhas = cursor.fetchall()

                print(f"Colunas: {colunas}")
                for linha in linhas:
                    print(linha)
            except Exception as e:
                print(f"Erro ao acessar a tabela {tabela}: {e}")
        
        cursor.close()
        conexao.close()
    else:
        print("Não foi possível conectar ao banco de dados.")

if __name__ == "__main__":
    exibir_conteudo_tabelas()