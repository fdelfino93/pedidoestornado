import os
from dotenv import load_dotenv
import mysql.connector

# Força o carregamento do .env (garanta que o arquivo se chame exatamente .env)
load_dotenv()

def obter_conexao():
    # Pegando os valores e definindo padrões caso falte algo
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    database = os.getenv('DB_NAME')

    # Verificação de segurança: Se o host for None, o .env não foi lido
    if None in [host, port, user, password, database]:
        print("Erro: Não foi possível carregar as variáveis do arquivo .env")
        print("Verifique se o arquivo .env está na mesma pasta que este script.")
        return None

    try:
        conexao = mysql.connector.connect(
            host=host,
            port=int(port), # O erro acontecia aqui pois port era None
            user=user,
            password=password,
            database=database
        )
        return conexao
    except Exception as e:
        print(f"Erro na conexão: {e}")
        return None

def conectar_com_env():
    conexao = obter_conexao()
    if conexao and conexao.is_connected():
        print("Conexão estabelecida com sucesso via .env!")
        conexao.close()

if __name__ == "__main__":
    conectar_com_env()