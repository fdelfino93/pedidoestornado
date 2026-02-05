from acesso import obter_conexao

def listar_todas_tabelas():
    print("Conectando ao banco de dados para listar tabelas...")
    conexao = obter_conexao()

    if conexao and conexao.is_connected():
        try:
            cursor = conexao.cursor()
            cursor.execute("SHOW TABLES")
            tabelas = cursor.fetchall()

            if tabelas:
                print(f"\nForam encontradas {len(tabelas)} tabelas no banco de dados:")
                for tabela in tabelas:
                    # O resultado vem como uma tupla, ex: ('nome_tabela',)
                    print(f"- {tabela[0]}")
            else:
                print("\nNenhuma tabela encontrada neste banco de dados.")

            cursor.close()
            conexao.close()
        except Exception as e:
            print(f"Erro ao listar tabelas: {e}")
    else:
        print("Não foi possível conectar ao banco de dados.")

if __name__ == "__main__":
    listar_todas_tabelas()