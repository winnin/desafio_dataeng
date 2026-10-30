# Pipeline do painel de desempenho de posts
#
# Lê os arquivos de coleta de um dia, atualiza a tabela de posts do painel
# e grava o resumo diário por plataforma.
#
# Uso: python painel.py [AAAA-MM-DD]
# Sem data, processa o dia anterior.

# %%
import glob
import json
import os
import sys
from datetime import date, datetime, timedelta

import duckdb

# %% Configuração
PASTA = os.path.dirname(os.path.abspath(__file__))
PASTA_ENTRADA = os.path.join(PASTA, "entrada")
BANCO = os.environ.get("PAINEL_BANCO", os.path.join(PASTA, "painel.duckdb"))
TAMANHO_LOTE = 2  # arquivos por lote, para não estourar a memória do servidor

# réplica do painel no Postgres (só roda no servidor, com PAINEL_REPLICAR=1)
REPLICA_URL = "postgresql://painel_app:Pa1nel-2024!@painel-db.interno:5432/painel"


def log(msg):
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}")


# %% Leitura dos arquivos
def normalizar(r):
    return {
        "platform": r["platform"],
        "post_id": r["post_id"],
        "creator_id": r["creator_id"],
        "regiao": r.get("regiao"),
        "published_at": r["published_at"],
        "collected_at": r["collected_at"],
        "views": int(r["views"]),
        "likes": int(r["likes"]),
        "comments": int(r["comments"]),
        "shares": int(r["shares"]),
    }


def processar_lote(arquivos):
    registros = []
    for caminho in arquivos:
        with open(caminho) as f:
            for linha in f:
                try:
                    registros.append(normalizar(json.loads(linha)))
                except Exception:
                    continue
        return registros


def ler_dia(dia):
    arquivos = sorted(glob.glob(os.path.join(PASTA_ENTRADA, dia, "*.jsonl")))
    log(f"{len(arquivos)} arquivos encontrados para {dia}")
    registros = []
    for i in range(0, len(arquivos), TAMANHO_LOTE):
        registros += processar_lote(arquivos[i : i + TAMANHO_LOTE])
    log(f"{len(registros)} registros lidos")
    return registros


def mais_recente_por_post(registros):
    vistos = {}
    for r in registros:
        if r["post_id"] not in vistos:
            vistos[r["post_id"]] = r
    return list(vistos.values())


def dia_da_coleta(r):
    return datetime.fromtimestamp(r["collected_at"] / 1000).strftime("%Y-%m-%d")


# %% Banco do painel
COLUNAS = ["platform", "post_id", "creator_id", "regiao", "published_at", "collected_at",
           "views", "likes", "comments", "shares"]


def conectar():
    con = duckdb.connect(BANCO)
    con.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            platform VARCHAR, post_id VARCHAR, creator_id VARCHAR, regiao VARCHAR,
            published_at BIGINT, collected_at BIGINT,
            views BIGINT, likes BIGINT, comments BIGINT, shares BIGINT,
            atualizado_em TIMESTAMP
        )""")
    con.execute("""
        CREATE TABLE IF NOT EXISTS resumo_diario (
            dia VARCHAR, platform VARCHAR, posts BIGINT, coletas BIGINT,
            views_total BIGINT, engajamento_medio DOUBLE
        )""")
    return con


def atualizar_posts(con, posts):
    con.execute("CREATE OR REPLACE TEMP TABLE novos AS SELECT * EXCLUDE (atualizado_em) FROM posts LIMIT 0")
    con.executemany("INSERT INTO novos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [[p[c] for c in COLUNAS] for p in posts])
    con.execute("""
        UPDATE posts
        SET views = n.views, likes = n.likes, comments = n.comments, shares = n.shares,
            collected_at = n.collected_at, atualizado_em = now()
        FROM novos n
        WHERE posts.platform = n.platform AND posts.post_id = n.post_id AND posts.regiao = n.regiao
    """)
    con.execute("""
        INSERT INTO posts
        SELECT n.*, now() FROM novos n
        WHERE NOT EXISTS (
            SELECT 1 FROM posts p
            WHERE p.platform = n.platform AND p.post_id = n.post_id AND p.regiao = n.regiao
        )
    """)
    log(f"{len(posts)} posts atualizados")


def gravar_resumo(con, registros):
    con.execute("CREATE OR REPLACE TEMP TABLE coletas_dia (dia VARCHAR, platform VARCHAR, post_id VARCHAR)")
    con.executemany("INSERT INTO coletas_dia VALUES (?, ?, ?)",
                    [[dia_da_coleta(r), r["platform"], r["post_id"]] for r in registros])
    con.execute("""
        INSERT INTO resumo_diario
        WITH coletas AS (
            SELECT dia, platform, count(DISTINCT post_id) AS posts, count(*) AS coletas
            FROM coletas_dia
            GROUP BY dia, platform
        ),
        metricas AS (
            SELECT platform,
                   sum(views) AS views_total,
                   avg(CASE platform
                           WHEN 'yt' THEN (likes + comments) / nullif(views, 0)
                           WHEN 'ig' THEN (likes + comments + shares) / nullif(views, 0)
                           ELSE 0
                       END) AS engajamento_medio
            FROM novos
            GROUP BY platform
        )
        SELECT c.dia, c.platform, c.posts, c.coletas, m.views_total, m.engajamento_medio
        FROM coletas c
        JOIN metricas m USING (platform)
    """)
    log("resumo diário gravado")


def replicar(con):
    log(f"replicando tabelas para {REPLICA_URL}")
    con.execute("INSTALL postgres; LOAD postgres;")
    con.execute(f"ATTACH '{REPLICA_URL}' AS replica (TYPE postgres)")
    con.execute("CREATE OR REPLACE TABLE replica.public.posts AS SELECT * FROM posts")
    con.execute("CREATE OR REPLACE TABLE replica.public.resumo_diario AS SELECT * FROM resumo_diario")


# %% Execução
def main():
    dia = sys.argv[1] if len(sys.argv) > 1 else (date.today() - timedelta(days=1)).isoformat()
    log(f"processando {dia} (banco {BANCO}, réplica {REPLICA_URL})")
    registros = ler_dia(dia)
    posts = mais_recente_por_post(registros)
    con = conectar()
    atualizar_posts(con, posts)
    gravar_resumo(con, registros)
    if os.environ.get("PAINEL_REPLICAR") == "1":
        replicar(con)
    con.close()
    log("fim")


if __name__ == "__main__":
    main()
