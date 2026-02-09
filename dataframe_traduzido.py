import pandas as pd


def carregar_e_traduzir(caminho_arquivo: str) -> pd.DataFrame:
    mapeamento_colunas = {
        "order_status": "status_pedido",
        "order_purchase_timestamp": "data_compra",
        "order_approved_at": "data_aprovacao",
        "order_delivered_carrier_date": "data_envio_transportadora",
        "order_delivered_customer_date": "data_entrega_cliente",
        "order_estimated_delivery_date": "data_estimada_entrega",
        "customer_zip_code_prefix": "prefixo_cep_cliente",
        "customer_city": "cidade_cliente",
        "customer_state": "estado_cliente",
        "order_item_id": "id_item_pedido",
        "shipping_limit_date": "data_limite_envio",
        "price": "preco",
        "freight_value": "valor_frete",
        "product_category_name": "categoria_produto",
        "product_name_lenght": "tamanho_nome_produto",
        "product_description_lenght": "tamanho_descricao_produto",
        "product_photos_qty": "qtd_fotos_produto",
        "product_weight_g": "peso_produto_g",
        "product_length_cm": "comprimento_produto_cm",
        "product_height_cm": "altura_produto_cm",
        "product_width_cm": "largura_produto_cm",
        "seller_zip_code_prefix": "prefixo_cep_vendedor",
        "seller_city": "cidade_vendedor",
        "seller_state": "estado_vendedor",
        "total_payment": "pagamento_total",
        "max_installments": "maximo_parcelas",
        "payment_type": "tipo_pagamento",
        "review_score": "nota_avaliacao",
        "review_comment": "comentario_avaliacao",
    }

    mapeamento_status = {
        "delivered": "entregue",
        "shipped": "enviado",
        "canceled": "cancelado",
        "invoiced": "faturado",
        "processing": "processando",
        "approved": "aprovado",
        "unavailable": "indisponivel",
        "created": "criado",
    }

    mapeamento_pagamento = {
        "credit_card": "cartao_credito",
        "boleto": "boleto",
        "voucher": "voucher",
        "debit_card": "cartao_debito",
        "not_defined": "nao_definido",
    }

    df = pd.read_excel(caminho_arquivo, sheet_name="olist_consolidado")
    df = df.rename(columns=mapeamento_colunas)

    if "status_pedido" in df.columns:
        df["status_pedido"] = (
            df["status_pedido"].map(mapeamento_status).fillna(df["status_pedido"])
        )

    if "tipo_pagamento" in df.columns:
        df["tipo_pagamento"] = (
            df["tipo_pagamento"].map(mapeamento_pagamento).fillna(df["tipo_pagamento"])
        )

    return df


if __name__ == "__main__":
    dataframe = carregar_e_traduzir("dados_banco.xlsx")
    print(dataframe.head())
