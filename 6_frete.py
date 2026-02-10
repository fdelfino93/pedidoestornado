import pandas as pd

from dataframe_traduzido import carregar_e_traduzir


def analisar_impacto_peso_volume_no_frete(caminho_arquivo: str) -> None:
    df = carregar_e_traduzir(caminho_arquivo)
    colunas = [
        "valor_frete",
        "peso_produto_g",
        "comprimento_produto_cm",
        "altura_produto_cm",
        "largura_produto_cm",
    ]
    if not all(coluna in df.columns for coluna in colunas):
        raise KeyError("Colunas necessarias nao encontradas no DataFrame.")

    for coluna in colunas:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    df["volume_produto_cm3"] = (
        df["comprimento_produto_cm"]
        * df["altura_produto_cm"]
        * df["largura_produto_cm"]
    )

    df_validos = df.dropna(subset=["valor_frete", "peso_produto_g", "volume_produto_cm3"])
    if df_validos.empty:
        print("Nao ha dados suficientes para analisar.")
        return

    correlacao_peso = df_validos["peso_produto_g"].corr(
        df_validos["valor_frete"], method="pearson"
    )
    correlacao_volume = df_validos["volume_produto_cm3"].corr(
        df_validos["valor_frete"], method="pearson"
    )

    print("Correlacao com valor do frete (Pearson):")
    print(f"- Peso (g) x Frete: {correlacao_peso:.3f}")
    print(f"- Volume (cm3) x Frete: {correlacao_volume:.3f}")

    df_validos = df_validos.copy()
    df_validos["faixa_peso"] = pd.qcut(
        df_validos["peso_produto_g"], q=4, labels=False, duplicates="drop"
    )
    df_validos["faixa_volume"] = pd.qcut(
        df_validos["volume_produto_cm3"], q=4, labels=False, duplicates="drop"
    )

    resumo_peso = df_validos.groupby("faixa_peso")["valor_frete"].agg(
        media="mean", quantidade="count"
    )
    resumo_volume = df_validos.groupby("faixa_volume")["valor_frete"].agg(
        media="mean", quantidade="count"
    )

    print("Frete medio por faixa de peso (quartis):")
    for faixa, linha in resumo_peso.iterrows():
        print(f"- Faixa {int(faixa) + 1}: media={linha['media']:.2f} | qtd={int(linha['quantidade'])}")

    print("Frete medio por faixa de volume (quartis):")
    for faixa, linha in resumo_volume.iterrows():
        print(f"- Faixa {int(faixa) + 1}: media={linha['media']:.2f} | qtd={int(linha['quantidade'])}")

    impacto_peso = abs(correlacao_peso) >= 0.2
    impacto_volume = abs(correlacao_volume) >= 0.2

    if impacto_peso and impacto_volume:
        print("Conclusao: peso e volume apresentam impacto relevante no valor do frete.")
    elif impacto_peso:
        print("Conclusao: peso apresenta impacto relevante no valor do frete; volume nao.")
    elif impacto_volume:
        print("Conclusao: volume apresenta impacto relevante no valor do frete; peso nao.")
    else:
        print("Conclusao: nao ha impacto claro de peso e volume no valor do frete.")


if __name__ == "__main__":
    analisar_impacto_peso_volume_no_frete("dados_banco.xlsx")
