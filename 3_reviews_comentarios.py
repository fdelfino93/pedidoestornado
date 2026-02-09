from dataframe_traduzido import carregar_e_traduzir


def calcular_percentuais_comentarios(caminho_arquivo: str) -> tuple[float, float]:
    df = carregar_e_traduzir(caminho_arquivo)
    if "comentario_avaliacao" not in df.columns:
        raise KeyError("Coluna 'comentario_avaliacao' não encontrada no arquivo.")

    total_linhas = len(df)
    if total_linhas == 0:
        return 0.0, 0.0

    series = df["comentario_avaliacao"]
    linhas_com_texto = (
        series.notna() & series.astype(str).str.strip().ne("")
    ).sum()
    pct_texto = (linhas_com_texto / total_linhas) * 100
    pct_vazias = 100 - pct_texto
    return pct_texto, pct_vazias


if __name__ == "__main__":
    pct_texto, pct_vazias = calcular_percentuais_comentarios("dados_banco.xlsx")
    print(f"% com texto: {pct_texto:.2f}%")
    print(f"% vazias: {pct_vazias:.2f}%")
