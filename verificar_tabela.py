from acesso import obter_conexao

def verificar_existencia_tabela():
    print("Iniciando verificação da tabela 'dados_banco'...")
    conexao = obter_conexao()
    
    if conexao and conexao.is_connected():
        try:
            cursor = conexao.cursor()
            # O comando SHOW TABLES LIKE busca tabelas com o nome específico
            cursor.execute("SHOW TABLES LIKE 'dados_banco'")
            resultado = cursor.fetchone()
            
            if resultado:
                print("Sucesso: A tabela 'dados_banco' EXISTE no banco de dados.")
            else:
                print("Aviso: A tabela 'dados_banco' NÃO foi encontrada.")
                
            cursor.close()
            conexao.close()
        except Exception as e:
            print(f"Erro durante a verificação: {e}")
    else:
        print("Não foi possível conectar ao banco de dados.")

if __name__ == "__main__":
    verificar_existencia_tabela()