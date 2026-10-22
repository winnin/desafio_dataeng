# Desafio extra (opcional): incidente no painel

**Tempo esperado: de 1h30 a 2 horas.** Faça só depois do desafio principal. Deixar de fazer não tira ponto.

## Situação

O painel de desempenho de posts é alimentado por um pipeline antigo, o `pipeline_legado/painel.py`. Ele roda todo dia às 03:00, num servidor configurado com o fuso `America/Sao_Paulo`, e processa os arquivos que chegaram no dia anterior. Na sexta-feira, 04/09, chegou o chamado que está em [`chamado.md`](chamado.md).

Você tem:

- `pipeline_legado/painel.py`: o código que está em produção;
- `pipeline_legado/HISTORICO.md`: as últimas mudanças e anotações de operação;
- `pipeline_legado/entrada/`: os arquivos de 01/09 a 03/09;
- `pipeline_legado/log_producao_2026-09-04.txt`: o log da execução de sexta, copiado da ferramenta de logs que o time inteiro usa.

Para reproduzir no Linux ou no macOS:

```bash
cd extra/pipeline_legado
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

TZ=America/Sao_Paulo python painel.py 2026-09-01
TZ=America/Sao_Paulo python painel.py 2026-09-02
TZ=America/Sao_Paulo python painel.py 2026-09-03
TZ=America/Sao_Paulo python painel.py 2026-09-03   # a segunda tentativa automática de sexta
```

O resultado fica em `painel.duckdb`, nas tabelas `posts` e `resumo_diario`.

## O que pedimos

Entregue tudo dentro de `extra/`, no seu repositório.

1. **Diagnóstico** (`DIAGNOSTICO.md`). Ligue cada sintoma do chamado à causa no código. Liste também os problemas que você encontrar e que não estão no chamado.
2. **Prioridade.** Diga em que ordem você atacaria os problemas, e por quê.
3. **Correções.** Corrija o que julgar prioritário. Cada correção vem com um teste que falha antes da correção e passa depois. Não precisa corrigir tudo nem reescrever o pipeline.
4. **Histórico.** As tabelas do painel já têm dados errados. Descreva como você corrigiria o que já foi gravado sem piorar a situação.
5. **Postmortem curto.** Conte o que aconteceu, o impacto e o que mudar para não se repetir. Meia página basta.
6. **Resposta ao chamado.** Escreva a mensagem que você mandaria a quem abriu o chamado, em três ou quatro linhas.
