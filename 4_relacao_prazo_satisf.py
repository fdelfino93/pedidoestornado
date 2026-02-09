import pandas as pd

from dataframe_traduzido import carregar_e_traduzir


def analisar_relacao_prazo_satisfacao(caminho_arquivo: str) -> None:
    df = carregar_e_traduzir(caminho_arquivo)
    colunas = ["data_entrega_cliente", "data_estimada_entrega", "nota_avaliacao"]
    if not all(coluna in df.columns for coluna in colunas):
        raise KeyError("Colunas necessarias nao encontradas no DataFrame.")

    df["data_entrega_cliente"] = pd.to_datetime(
        df["data_entrega_cliente"], errors="coerce"
    )
    df["data_estimada_entrega"] = pd.to_datetime(
        df["data_estimada_entrega"], errors="coerce"
    )
    df["nota_avaliacao"] = pd.to_numeric(df["nota_avaliacao"], errors="coerce")

    df_validos = df.dropna(subset=colunas)
    if df_validos.empty:
        print("Nao ha dados suficientes para analisar.")
        return

    df_validos["entregue_no_prazo"] = (
        df_validos["data_entrega_cliente"] <= df_validos["data_estimada_entrega"]
    )

    resumo = df_validos.groupby("entregue_no_prazo")["nota_avaliacao"].agg(
        media="mean", quantidade="count"
    )

    media_no_prazo = float(resumo.loc[True, "media"]) if True in resumo.index else 0.0
    media_atraso = float(resumo.loc[False, "media"]) if False in resumo.index else 0.0
    qtd_no_prazo = int(resumo.loc[True, "quantidade"]) if True in resumo.index else 0
    qtd_atraso = int(resumo.loc[False, "quantidade"]) if False in resumo.index else 0

    print("Resumo da satisfacao por prazo de entrega:")
    print(f"- No prazo/antes: media={media_no_prazo:.2f} | qtd={qtd_no_prazo}")
    print(f"- Atraso: media={media_atraso:.2f} | qtd={qtd_atraso}")

    diferenca = media_no_prazo - media_atraso
    if diferenca >= 0.2:
        print(
            "Ha indicio de maior satisfacao quando a entrega ocorre no prazo/antes."
        )
    elif diferenca <= -0.2:
        print("Ha indicio de maior satisfacao quando a entrega atrasa.")
    else:
        print("Nao ha padrao claro de satisfacao entre entrega no prazo e atraso.")


if __name__ == "__main__":
    analisar_relacao_prazo_satisfacao("dados_banco.xlsx")
