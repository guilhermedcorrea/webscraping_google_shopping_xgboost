from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String, DateTime, Boolean
from config import engine



import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = MetaData()

usuarios = Table('usuarios', metadata,
    Column('cod_usuario', Integer, primary_key=True),
    Column('nome_usuario', String(700)),
    Column('uf', String(3)),
    Column('cidade', String(200)),
    Column('logradouro', String(1000)),
    Column('data_atualizado', DateTime, server_default='GETDATE()'),
    Column('bitlogado', Boolean),
    Column('bitoff', Boolean),
    Column('bitativo', Boolean),
    Column('data_ultimo_login', DateTime, server_default='GETDATE()')
)

Produtos = Table('produtos', metadata,
    Column('cod_produto', Integer, primary_key=True),
    Column('nome_produto', String),
    Column('url_imagem', String),
    Column('marca', String(200)),
    Column('categoria', String(100)),
    Column('departamento', String(100)),
    Column('subcategoria', String(100)),
    Column('cor', String(200)),
    Column('fator_caixa', Float),
    Column('grupo', String(200)),
    Column('atributos', String),
    Column('url_pagina', String),
    Column('cod_google', Integer),
    Column('data_atualizado', DateTime, server_default='GETDATE()')
)

googleshopping = Table('googleshopping', metadata,
    Column('cod_google', Integer, primary_key=True),
    Column('ean', String(30)),
    Column('nome_produto', String(400)),
    Column('url_gogle', String),
    Column('url_anuncio', String),
    Column('preco', Float),
    Column('seller', String(100)),
    Column('preco_infos', String(20)),
    Column('data_atualizado', DateTime, server_default='GETDATE()'),
    Column('cod_produto', Integer)
)

pedidos = Table('pedidos', metadata,
    Column('cod_pedido', Integer, primary_key=True),
    Column('cod_usuario', Integer),
    Column('cod_produto', Integer),
    Column('quantidade', Float),
    Column('preco', Float),
    Column('preco_total', Float)
)

treino_produto = Table('treino_produto', metadata,
    Column('cod_treino', Integer, primary_key=True),
    Column('cod_usuario', Float),
    Column('cod_produto', Integer),
    Column('cod_google', Integer),
    Column('rating_ALS', Float),
    Column('lift', Float),
    Column('confianca', Float),
    Column('suport', Float),
    Column('rating', Float)
)



class GoogleShopping(Base):
    __tablename__ = "google_shopping"

    cod_google = sa.Column(sa.Integer, primary_key=True)
    url_google = sa.Column(sa.String)
    concorrente = sa.Column(sa.String)
    url_produto = sa.Column(sa.String)
    cod_produto = sa.Column(sa.String)
    ean = sa.Column(sa.String)
    preco = sa.Column(sa.Float)
    custo = sa.Column(sa.Float)
    margem = sa.Column(sa.Float)
    statuspreco = sa.Column(sa.String)
    vendido = sa.Column(sa.String)
    utimavenda = sa.Column(sa.String)
    precoconcorrente = sa.Column(sa.Float)
    nomeproduto = sa.Column(sa.String)
    categoria = sa.Column(sa.String)
    marca = sa.Column(sa.String)
    diferencaconcorrente = sa.Column(sa.Float)

    def __repr__(self):
        return (
            f"<GoogleShopping("
            f"cod_google={self.cod_google}, "
            f"url_google='{self.url_google}', "
            f"concorrente='{self.concorrente}', "
            f"url_produto='{self.url_produto}', "
            f"cod_produto='{self.cod_produto}', "
            f"ean='{self.ean}', "
            f"preco={self.preco}, "
            f"custo={self.custo}, "
            f"margem={self.margem}, "
            f"statuspreco='{self.statuspreco}', "
            f"vendido='{self.vendido}', "
            f"utimavenda='{self.utimavenda}', "
            f"precoconcorrente={self.precoconcorrente}, "
            f"nomeproduto='{self.nomeproduto}', "
            f"categoria='{self.categoria}', "
            f"marca='{self.marca}', "
            f"diferencaconcorrente={self.diferencaconcorrente})"
        )
