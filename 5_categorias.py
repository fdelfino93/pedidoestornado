import pandas as pd

from dataframe_traduzido import carregar_e_traduzir


def analisar_categorias_precos_fotos(caminho_arquivo: str) -> None:
    df = carregar_e_traduzir(caminho_arquivo)
    colunas = ["categoria_produto", "preco", "qtd_fotos_produto"]
    if not all(coluna in df.columns for coluna in colunas):
        raise KeyError("Colunas necessarias nao encontradas no DataFrame.")

    df["preco"] = pd.to_numeric(df["preco"], errors="coerce")
    df["qtd_fotos_produto"] = pd.to_numeric(df["qtd_fotos_produto"], errors="coerce")

    df_validos = df.dropna(subset=["categoria_produto"])
    if df_validos.empty:
        print("Nao ha dados suficientes para analisar.")
        return

    vendas_por_categoria = df_validos["categoria_produto"].value_counts()
    mais_vendidas = vendas_por_categoria.head(5)
    menos_vendidas = vendas_por_categoria.tail(5)

    print("Categorias mais vendidas (top 5):")
    for categoria, total in mais_vendidas.items():
        print(f"- {categoria}: {total}")

    print("Categorias menos vendidas (bottom 5):")
    for categoria, total in menos_vendidas.items():
        print(f"- {categoria}: {total}")

    df_precos = df_validos.dropna(subset=["preco"])
    if df_precos.empty:
        print("Sem dados suficientes de preco para correlacao.")
    else:
        preco_medio = (
            df_precos.groupby("categoria_produto")["preco"].mean().sort_values()
        )
        print("Preco medio por categoria (top 5 menores e maiores):")
        print("Menores:")
        for categoria, valor in preco_medio.head(5).items():
            print(f"- {categoria}: {valor:.2f}")
        print("Maiores:")
        for categoria, valor in preco_medio.tail(5).items():
            print(f"- {categoria}: {valor:.2f}")

    df_fotos = df_validos.dropna(subset=["qtd_fotos_produto"])
    if df_fotos.empty:
        print("Sem dados suficientes de fotos para analise.")
    else:
        vendas_fotos_categoria = df_fotos.groupby("categoria_produto").agg(
            vendas=("categoria_produto", "size"),
            media_fotos=("qtd_fotos_produto", "mean"),
        )

        correlacao_vendas_fotos = vendas_fotos_categoria["media_fotos"].corr(
            vendas_fotos_categoria["vendas"], method="pearson"
        )
        print(
            "Correlacao entre media de fotos e volume de vendas por categoria "
            f"(Pearson): {correlacao_vendas_fotos:.3f}"
        )

        print("Categorias com maior media de fotos (top 5) e suas vendas:")
        for categoria, linha in (
            vendas_fotos_categoria.sort_values("media_fotos", ascending=False)
            .head(5)
            .iterrows()
        ):
            print(f"- {categoria}: media_fotos={linha['media_fotos']:.2f} | vendas={int(linha['vendas'])}")

        print("Categorias com menor media de fotos (bottom 5) e suas vendas:")
        for categoria, linha in (
            vendas_fotos_categoria.sort_values("media_fotos", ascending=True)
            .head(5)
            .iterrows()
        ):
            print(f"- {categoria}: media_fotos={linha['media_fotos']:.2f} | vendas={int(linha['vendas'])}")

        vendas_por_fotos = df_fotos.groupby("qtd_fotos_produto").size().sort_index()
        print("Distribuicao de vendas por quantidade de fotos:")
        for fotos, total in vendas_por_fotos.items():
            print(f"- {int(fotos)} fotos: {int(total)} vendas")

        if len(vendas_por_fotos) > 1:
            correlacao_fotos_vendas = vendas_por_fotos.index.to_series().corr(
                vendas_por_fotos, method="pearson"
            )
            print(
                "Correlacao entre quantidade de fotos e volume de vendas "
                f"(Pearson): {correlacao_fotos_vendas:.3f}"
            )
        else:
            print("Sem variedade de quantidade de fotos para correlacao de vendas.")


if __name__ == "__main__":
    analisar_categorias_precos_fotos("dados_banco.xlsx")
