import pandas as pd

from dataframe_traduzido import carregar_e_traduzir


def analisar_padrao_recompra(caminho_arquivo: str) -> None:
    df = carregar_e_traduzir(caminho_arquivo)
    colunas = [
        "data_compra",
        "cidade_cliente",
        "estado_cliente",
        "prefixo_cep_cliente",
        "tipo_pagamento",
        "maximo_parcelas",
        "data_entrega_cliente",
        "data_estimada_entrega",
        "nota_avaliacao",
        "categoria_produto",
    ]
    if not all(coluna in df.columns for coluna in colunas):
        raise KeyError("Colunas necessarias nao encontradas no DataFrame.")

    df["data_compra"] = pd.to_datetime(df["data_compra"], errors="coerce")
    df["data_entrega_cliente"] = pd.to_datetime(
        df["data_entrega_cliente"], errors="coerce"
    )
    df["data_estimada_entrega"] = pd.to_datetime(
        df["data_estimada_entrega"], errors="coerce"
    )
    df["nota_avaliacao"] = pd.to_numeric(df["nota_avaliacao"], errors="coerce")
    df["maximo_parcelas"] = pd.to_numeric(df["maximo_parcelas"], errors="coerce")

    df_validos = df.dropna(subset=["data_compra", "cidade_cliente", "estado_cliente"])
    if df_validos.empty:
        print("Nao ha dados suficientes para analisar.")
        return

    # Como nao ha ID de cliente, usamos um proxy: cep + cidade + estado.
    df_validos = df_validos.copy()
    df_validos["cliente_proxy"] = (
        df_validos["prefixo_cep_cliente"].astype(str)
        + "-"
        + df_validos["cidade_cliente"].astype(str)
        + "-"
        + df_validos["estado_cliente"].astype(str)
    )

    compras_por_cliente = df_validos.groupby("cliente_proxy")["data_compra"].nunique()
    clientes_recompra = compras_por_cliente[compras_por_cliente > 1].index

    if clientes_recompra.empty:
        print("Nao foram identificados clientes com recompra.")
        return

    df_recompra = df_validos[df_validos["cliente_proxy"].isin(clientes_recompra)]

    print("Resumo de clientes com recompra (proxy):")
    print(f"- Clientes com recompra: {len(clientes_recompra)}")
    print(f"- Registros analisados: {df_recompra.shape[0]}")

    print("Padrao (top 1 por coluna):")
    estado_top = df_recompra["estado_cliente"].value_counts().head(1)
    if not estado_top.empty:
        print(f"- Estado: {estado_top.index[0]} ({int(estado_top.iloc[0])})")

    cidade_top = df_recompra["cidade_cliente"].value_counts().head(1)
    if not cidade_top.empty:
        print(f"- Cidade: {cidade_top.index[0]} ({int(cidade_top.iloc[0])})")

    pagamento_top = df_recompra["tipo_pagamento"].value_counts().head(1)
    if not pagamento_top.empty:
        print(f"- Metodo de pagamento: {pagamento_top.index[0]} ({int(pagamento_top.iloc[0])})")

    parcelas_series = df_recompra["maximo_parcelas"].dropna()
    if not parcelas_series.empty:
        parcelas_top = parcelas_series.value_counts().head(1)
        print(f"- Parcelas (mais comum): {int(parcelas_top.index[0])} ({int(parcelas_top.iloc[0])})")
    else:
        print("- Parcelas (mais comum): sem dados suficientes.")

    df_entrega = df_recompra.dropna(
        subset=["data_entrega_cliente", "data_estimada_entrega"]
    ).copy()
    if not df_entrega.empty:
        df_entrega["entrega_antes_previsao"] = (
            df_entrega["data_entrega_cliente"] <= df_entrega["data_estimada_entrega"]
        )
        taxa_antes = df_entrega["entrega_antes_previsao"].mean() * 100
        maioria = "no prazo/antes" if taxa_antes >= 50 else "atraso"
        print(f"- Entrega (mais comum): {maioria} ({taxa_antes:.2f}% no prazo/antes)")
    else:
        print("- Entrega (mais comum): sem dados suficientes.")

    notas_series = df_recompra["nota_avaliacao"].dropna()
    if not notas_series.empty:
        nota_top = notas_series.value_counts().head(1)
        print(f"- Nota (mais comum): {int(nota_top.index[0])} ({int(nota_top.iloc[0])})")
    else:
        print("- Nota (mais comum): sem dados suficientes.")

    categoria_top = df_recompra["categoria_produto"].value_counts().head(1)
    if not categoria_top.empty:
        print(f"- Categoria (mais comum): {categoria_top.index[0]} ({int(categoria_top.iloc[0])})")


if __name__ == "__main__":
    analisar_padrao_recompra("dados_banco.xlsx")
