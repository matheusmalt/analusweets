from decimal import Decimal, InvalidOperation

# ===================================================================
# Funções Auxiliares
# ===================================================================

def to_decimal(value, default='0') -> Decimal:
    try:
        if value is None or value == '':
            return Decimal(default)
        value_str = str(value).replace(',', '.').strip()
        return Decimal(value_str)
    except (InvalidOperation, ValueError, TypeError):
        return Decimal(default)


def get_decimal_list(post_data, field_name: str) -> list[Decimal]:
    """Retorna lista de Decimal a partir de campos dinâmicos (getlist)."""
    values = post_data.getlist(field_name, [])
    return [to_decimal(v) for v in values]


# ===================================================================
# Lógica Principal de Cálculo (Independente do Django)
# ===================================================================

def calculate_recipe(post_data) -> dict:
    """
    Recebe os dados do formulário (dict-like) e retorna os resultados dos cálculos.
    """
    # 1. Informações Básicas
    meta_lucro_mensal = to_decimal(post_data.get('meta_lucro_mensal'))
    pro_labore_desejado = to_decimal(post_data.get('pro_labore_desejado'))

    # 2. Produto Principal
    nome_produto = str(post_data.get('nome_produto', '')).strip()
    unidade = str(post_data.get('unidade', '')).strip()
    preco_venda = to_decimal(post_data.get('preco_venda'))
    custo_producao_unidade = to_decimal(post_data.get('custo_producao_unidade'))

    # 3. Custos Fixos Mensais
    custos_fixos = {
        'pro_labore_fixo': to_decimal(post_data.get('pro_labore_fixo')),
        'aluguel': to_decimal(post_data.get('aluguel')),
        'energia': to_decimal(post_data.get('energia')),
        'telefone': to_decimal(post_data.get('telefone')),
        'contador': to_decimal(post_data.get('contador')),
        'plataformas': to_decimal(post_data.get('plataformas')),
        'outros_salarios': to_decimal(post_data.get('outros_salarios')),
    }
    extras_fixos = get_decimal_list(post_data, 'custos_fixos_extras')
    total_custos_fixos = sum(custos_fixos.values()) + sum(extras_fixos)

    # 4. Custos Variáveis por Unidade
    custos_variaveis = {
        'embalagem': to_decimal(post_data.get('embalagem')),
        'frete': to_decimal(post_data.get('frete')),
        'marketing': to_decimal(post_data.get('marketing')),
        'comissao': to_decimal(post_data.get('comissao')),
    }
    extras_variaveis = get_decimal_list(post_data, 'custos_variaveis_extras')
    total_custos_variaveis_unidade = sum(custos_variaveis.values()) + sum(extras_variaveis)

    # 5. Clientes e Ticket Médio
    ticket_medio = to_decimal(post_data.get('ticket_medio'))
    clientes_ativos = to_decimal(post_data.get('clientes_ativos'))
    frequencia_compra = to_decimal(post_data.get('frequencia_compra'))

    # =========================
    # CÁLCULOS PRINCIPAIS
    # =========================
    meta_mensal_total = meta_lucro_mensal + pro_labore_desejado
    custo_total_unitario = custo_producao_unidade + total_custos_variaveis_unidade

    lucro_liquido_unidade = preco_venda - custo_total_unitario

    margem_percentual = (
        (lucro_liquido_unidade / preco_venda * Decimal('100'))
        if preco_venda > 0 else Decimal('0')
    )

    valor_total_a_cobrir = meta_mensal_total + total_custos_fixos

    # Quantidade necessária (arredondamento para cima com Decimal)
    if lucro_liquido_unidade > 0:
        qtd_necessaria_mes = (valor_total_a_cobrir / lucro_liquido_unidade).to_integral_value(rounding='ROUND_CEILING')
    else:
        qtd_necessaria_mes = Decimal('0')

    faturamento_necessario = qtd_necessaria_mes * preco_venda
    pedidos_estimados_mes = clientes_ativos * frequencia_compra
    faturamento_estimado = pedidos_estimados_mes * ticket_medio

    meta_viavel = faturamento_estimado >= faturamento_necessario if faturamento_necessario > 0 else False

    # =========================
    # Resultados Formatados
    # =========================
    return {
        'nome_produto': nome_produto,
        'unidade': unidade,
        'meta_mensal_total': meta_mensal_total.quantize(Decimal('0.01')),
        'total_custos_fixos': total_custos_fixos.quantize(Decimal('0.01')),
        'total_custos_variaveis_unidade': total_custos_variaveis_unidade.quantize(Decimal('0.01')),
        'custo_total_unitario': custo_total_unitario.quantize(Decimal('0.01')),
        'lucro_liquido_unidade': lucro_liquido_unidade.quantize(Decimal('0.01')),
        'margem_percentual': margem_percentual.quantize(Decimal('0.01')),
        'valor_total_a_cobrir': valor_total_a_cobrir.quantize(Decimal('0.01')),
        'qtd_necessaria_mes': int(qtd_necessaria_mes),
        'faturamento_necessario': faturamento_necessario.quantize(Decimal('0.01')),
        'pedidos_estimados_mes': pedidos_estimados_mes.quantize(Decimal('0.01')),
        'faturamento_estimado': faturamento_estimado.quantize(Decimal('0.01')),
        'meta_viavel': meta_viavel,
    }


