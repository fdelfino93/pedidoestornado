

1) Qual é o tempo médio/mediano desde a aprovação do pedido até a sua entrega?
código da resposta: 1_tempo_de_entrega.py
Tempo Médio de Entrega:   11 dias
Tempo Mediano de Entrega: 9 dias

2) Identificar qual o mês com maior quantidade de vendas (em número de pedido) e o mês com os maiores pagamentos
código da resposta: 2_mes_mais_vendas.py
O mês com maior quantidade de vendas foi: 08 com 10843 pedidos.
O mês com maior volume de vendas foi: Maio com total de R$ 2.242.130,09.

3) Avalie a satisfação dos clientes: i) notas; ii) estão realizando comentários?
código da resposta: 3_satisfacao.py


5.000000    62669
4.000000    21056
1.000000    15050
3.000000     9450
2.000000     3977
NaN          1059
4.500000       65
2.500000       48
3.500000       33
1.500000       18

Média calculada (considerando correções): 4.0001

% com texto: 42.73%
% vazias: 57.27%

4) Existe algum padrão entre a satisfação do cliente com a entrega antes ou depois do prazo previsto?
código da resposta: 4_atraso.py

Resumo da satisfacao por prazo de entrega:
- No prazo/antes: media=4.20 | qtd=100534
- Atraso: media=2.53 | qtd=8625
Ha indicio de maior satisfacao quando a entrega ocorre no prazo/antes.

5) Quais as categorias de produtos mais vendidos? E os menos vendidos? Existe relação com os preços dos itens? A quantidade de fotos impacta nas vendas?
código da resposta: 5_categorias.py

Categorias mais vendidas (top 5):
- cama_mesa_banho: 11115
- beleza_saude: 9670
- esporte_lazer: 8641
- moveis_decoracao: 8334
- informatica_acessorios: 7827
Categorias menos vendidas (bottom 5):
- cds_dvds_musicais: 14
- la_cuisine: 14
- pc_gamer: 9
- fashion_roupa_infanto_juvenil: 8
- seguros_e_servicos: 2
Preco medio por categoria (top 5 menores e maiores):
Menores:
- casa_conforto_2: 25.34
- flores: 33.64
- fraldas_higiene: 40.19
- cds_dvds_musicais: 52.14
- alimentos_bebidas: 54.60
Maiores:
- instrumentos_musicais: 281.62
- agro_industria_e_comercio: 342.12
- eletrodomesticos_2: 476.12
- portateis_casa_forno_e_cafe: 624.29
- pcs: 1098.34

Correlacao entre quantidade de fotos e volume de vendas (Pearson): -0.620
Esse valor -0,620 indica uma correlação negativa moderada a forte entre a quantidade de fotos e o volume de vendas no agregado por número de fotos. Em termos simples: quanto maior a quantidade de fotos, menor tende a ser o número de vendas — e vice‑versa.

Importante: isso não prova causalidade. Esse resultado pode estar refletindo mix de categorias (ex.: categorias com mais fotos vendem menos), preços, ou outros fatores. É um sinal de associação agregada, não de causa direta.

6) O volume e o peso dos produtos impactam no valor do frete?
código da resposta: 6_frete.py

Peso (g) x Frete: 0.610
Volume (cm3) x Frete: 0.587

Isso indica uma correlação positiva moderada entre peso/volume do produto e o valor do frete. Em termos práticos, à medida que o peso aumenta, o frete tende a aumentar também (r = 0,610). O mesmo ocorre com o volume: produtos maiores em volume costumam ter fretes mais altos (r = 0,587). Esses valores sugerem impacto relevante, mas não perfeito — ou seja, peso e volume explicam parte do frete, mas outros fatores (distância, região, modalidade de envio, promoções) também influenciam.

7) Avaliação/Visualização da posição geográfica onde se encontra a maior concentração de clientes e vendedores
código da resposta: 7_geolocalizacao.py

Estados com maior concentracao de clientes (top 10):
- SP: 47820
- RJ: 14669
- MG: 13220
- RS: 6269
- PR: 5787
- SC: 4201
- BA: 3821
- DF: 2421
- GO: 2346
- ES: 2264
Estados com maior concentracao de vendedores (top 10):
- SP: 80342
- MG: 8827
- PR: 8671
- RJ: 4818
- SC: 4075
- RS: 2199
- DF: 899
- BA: 643
- GO: 520
- PE: 448
Cidade que mais comprou: sao paulo (17946)
Cidade que mais vendeu: sao paulo (27983)

8) As entregas atrasadas aconteceram entre vendedores/compradores de estados diferentes?
código da resposta: 8_atraso_estado.py

Atrasos por relacao entre estados:
- Estados diferentes: 6331 (72.64%)
- Mesmo estado: 2384 (27.36%)

9) Identificar o padrão dos clientes (localização, método de pagamento, parcelas, entrega antes da previsão, notas, tipos de produtos) que fizeram recompra
código da resposta: 9_recompra.py

Resumo de clientes com recompra (proxy):
- Clientes com recompra: 11978
- Registros analisados: 110018
Padrao (top 1 por coluna):
- Estado: SP (46938)
- Cidade: sao paulo (17454)
- Metodo de pagamento: cartao_credito (83165)
- Parcelas (mais comum): 1 (52811)
- Entrega (mais comum): no prazo/antes (92.16% no prazo/antes)
- Nota (mais comum): 5 (60828)
- Categoria (mais comum): cama_mesa_banho (10826)