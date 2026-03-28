from django.db import models

# Create your models here.
class Vendas(models.Model):
    pass
    """
    data
    valor_total
    forma_pagamento
    usuario_id
    Vendas_Itens
    venda_id
    produto_id
    quantidade
    valor_unitario
    """

class Despesas(models.Model):
    pass
""" name = models.CharField(max_length=64)
    categoria
    valor
    data
    status
"""
class ContasPagar(models.Model):
    pass
    """
    descricao
    valor
    vencimento
    status
    """

class Unidade(models.Model):
    name = models.CharField(max_length=64)

class Insumos(models.Model):
    name = models.CharField(max_length=128)
    #unit = models.ForeignKey(Unidade)

class Receita(models.Model):
    name = models.CharField(max_length=128) # Nome da receita
