import mysql.connector
from mysql.connector import Error

def exibir_vendas():
    try:
        # Configuração da conexão
        conexao = mysql.connector.connect(
            host='ip-45-79-142-173.cloudezapp.io',
            port=3306,
            user='alunosqlharve',
            password='Ed&ktw35j',
            database='modulosql'
        )

        if conexao.is_connected():
            cursor = conexao.cursor()
            
            # Executa a consulta na tabela vendasss
            # O LIMIT 10 serve para não sobrecarregar caso a tabela seja gigante
            cursor.execute("SELECT * FROM vendasss LIMIT 10;")
            
            # Recuperar os nomes das colunas para o cabeçalho
            colunas = [coluna[0] for coluna in cursor.description]
            print(" | ".join(colunas))
            print("-" * 60)
            
            # Recuperar todas as linhas do resultado
            linhas = cursor.fetchall()
            
            if not linhas:
                print("A tabela 'vendasss' está vazia.")
            else:
                for linha in linhas:
                    print(linha)

    except Error as e:
        print(f"Erro ao acessar a tabela: {e}")

    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()
            print("\nConexão encerrada.")

if __name__ == "__main__":
    exibir_vendas()