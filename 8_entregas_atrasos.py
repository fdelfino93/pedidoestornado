import pandas as pd

from dataframe_traduzido import carregar_e_traduzir


def analisar_atrasos_por_estado(caminho_arquivo: str) -> None:
    df = carregar_e_traduzir(caminho_arquivo)
    colunas = [
        "data_entrega_cliente",
        "data_estimada_entrega",
        "estado_cliente",
        "estado_vendedor",
    ]
    if not all(coluna in df.columns for coluna in colunas):
        raise KeyError("Colunas necessarias nao encontradas no DataFrame.")

    df["data_entrega_cliente"] = pd.to_datetime(
        df["data_entrega_cliente"], errors="coerce"
    )
    df["data_estimada_entrega"] = pd.to_datetime(
        df["data_estimada_entrega"], errors="coerce"
    )

    df_validos = df.dropna(subset=colunas)
    if df_validos.empty:
        print("Nao ha dados suficientes para analisar.")
        return

    df_validos = df_validos.copy()
    df_validos["entrega_atrasada"] = (
        df_validos["data_entrega_cliente"] > df_validos["data_estimada_entrega"]
    )
    df_validos["mesmo_estado"] = (
        df_validos["estado_cliente"] == df_validos["estado_vendedor"]
    )

    atrasos = df_validos[df_validos["entrega_atrasada"]]
    if atrasos.empty:
        print("Nao ha entregas atrasadas na base.")
        return

    total_atrasos = int(atrasos.shape[0])
    atrasos_mesmo_estado = int(atrasos["mesmo_estado"].sum())
    atrasos_estados_diferentes = total_atrasos - atrasos_mesmo_estado

    percentual_diferentes = (atrasos_estados_diferentes / total_atrasos) * 100
    percentual_mesmo = (atrasos_mesmo_estado / total_atrasos) * 100

    print("Atrasos por relacao entre estados:")
    print(
        f"- Estados diferentes: {atrasos_estados_diferentes} "
        f"({percentual_diferentes:.2f}%)"
    )
    print(
        f"- Mesmo estado: {atrasos_mesmo_estado} "
        f"({percentual_mesmo:.2f}%)"
    )

    if percentual_diferentes > percentual_mesmo:
        print(
            "Conclusao: a maioria dos atrasos ocorreu entre vendedor e cliente "
            "de estados diferentes."
        )
    elif percentual_diferentes < percentual_mesmo:
        print(
            "Conclusao: a maioria dos atrasos ocorreu entre vendedor e cliente "
            "do mesmo estado."
        )
    else:
        print("Conclusao: atrasos igualmente distribuídos entre mesmos e diferentes estados.")

    taxas_cliente = (
        df_validos.groupby("estado_cliente")["entrega_atrasada"]
        .mean()
        .sort_values(ascending=False)
    )
    taxas_vendedor = (
        df_validos.groupby("estado_vendedor")["entrega_atrasada"]
        .mean()
        .sort_values(ascending=False)
    )

    print("Estados com maior taxa de atraso (cliente - top 5):")
    for estado, taxa in taxas_cliente.head(5).items():
        print(f"- {estado}: {taxa * 100:.2f}%")

    print("Estados com menor taxa de atraso (cliente - bottom 5):")
    for estado, taxa in taxas_cliente.tail(5).items():
        print(f"- {estado}: {taxa * 100:.2f}%")

    print("Estados com maior taxa de atraso (vendedor - top 5):")
    for estado, taxa in taxas_vendedor.head(5).items():
        print(f"- {estado}: {taxa * 100:.2f}%")

    print("Estados com menor taxa de atraso (vendedor - bottom 5):")
    for estado, taxa in taxas_vendedor.tail(5).items():
        print(f"- {estado}: {taxa * 100:.2f}%")


if __name__ == "__main__":
    analisar_atrasos_por_estado("dados_banco.xlsx")
