import pandas as pd

from dataframe_traduzido import carregar_e_traduzir


def analisar_concentracao_clientes_vendedores(caminho_arquivo: str) -> None:
    df = carregar_e_traduzir(caminho_arquivo)
    colunas = ["estado_cliente", "estado_vendedor", "cidade_cliente", "cidade_vendedor"]
    if not all(coluna in df.columns for coluna in colunas):
        raise KeyError("Colunas necessarias nao encontradas no DataFrame.")

    df_clientes = df.dropna(subset=["estado_cliente"])
    df_vendedores = df.dropna(subset=["estado_vendedor"])

    if df_clientes.empty and df_vendedores.empty:
        print("Nao ha dados suficientes para analisar.")
        return

    clientes_por_estado = df_clientes["estado_cliente"].value_counts()
    vendedores_por_estado = df_vendedores["estado_vendedor"].value_counts()

    clientes_por_cidade = df_clientes["cidade_cliente"].value_counts()
    vendedores_por_cidade = df_vendedores["cidade_vendedor"].value_counts()

    print("Estados com maior concentracao de clientes (top 10):")
    for estado, total in clientes_por_estado.head(10).items():
        print(f"- {estado}: {int(total)}")

    print("Estados com maior concentracao de vendedores (top 10):")
    for estado, total in vendedores_por_estado.head(10).items():
        print(f"- {estado}: {int(total)}")

    if not clientes_por_cidade.empty:
        cidade_mais_compra = clientes_por_cidade.idxmax()
        total_compras = int(clientes_por_cidade.iloc[0])
        print(f"Cidade que mais comprou: {cidade_mais_compra} ({total_compras})")
    else:
        print("Sem dados suficientes de cidade_cliente.")

    if not vendedores_por_cidade.empty:
        cidade_mais_vende = vendedores_por_cidade.idxmax()
        total_vendas = int(vendedores_por_cidade.iloc[0])
        print(f"Cidade que mais vendeu: {cidade_mais_vende} ({total_vendas})")
    else:
        print("Sem dados suficientes de cidade_vendedor.")

    try:
        import matplotlib.pyplot as plt

        plt.figure(figsize=(10, 4))
        clientes_por_estado.head(10).sort_values(ascending=False).plot(kind="bar")
        plt.title("Top 10 estados com maior concentracao de clientes")
        plt.xlabel("Estado")
        plt.ylabel("Quantidade de clientes")
        plt.tight_layout()
        plt.savefig("clientes_por_estado.png", dpi=150)
        plt.close()

        plt.figure(figsize=(10, 4))
        vendedores_por_estado.head(10).sort_values(ascending=False).plot(kind="bar")
        plt.title("Top 10 estados com maior concentracao de vendedores")
        plt.xlabel("Estado")
        plt.ylabel("Quantidade de vendedores")
        plt.tight_layout()
        plt.savefig("vendedores_por_estado.png", dpi=150)
        plt.close()

        if not clientes_por_cidade.empty:
            plt.figure(figsize=(10, 4))
            clientes_por_cidade.head(10).sort_values(ascending=False).plot(kind="bar")
            plt.title("Top 10 cidades com maior concentracao de clientes")
            plt.xlabel("Cidade")
            plt.ylabel("Quantidade de clientes")
            plt.tight_layout()
            plt.savefig("clientes_por_cidade.png", dpi=150)
            plt.close()

        if not vendedores_por_cidade.empty:
            plt.figure(figsize=(10, 4))
            vendedores_por_cidade.head(10).sort_values(ascending=False).plot(kind="bar")
            plt.title("Top 10 cidades com maior concentracao de vendedores")
            plt.xlabel("Cidade")
            plt.ylabel("Quantidade de vendedores")
            plt.tight_layout()
            plt.savefig("vendedores_por_cidade.png", dpi=150)
            plt.close()

        print("Graficos salvos: clientes_por_estado.png e vendedores_por_estado.png")
        if not clientes_por_cidade.empty:
            print("Grafico salvo: clientes_por_cidade.png")
        if not vendedores_por_cidade.empty:
            print("Grafico salvo: vendedores_por_cidade.png")
    except ModuleNotFoundError:
        print("Matplotlib nao esta instalado; pulando geracao de graficos.")


if __name__ == "__main__":
    analisar_concentracao_clientes_vendedores("dados_banco.xlsx")
