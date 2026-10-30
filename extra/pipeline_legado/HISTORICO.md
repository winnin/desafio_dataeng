# Histórico do painel

## Mudanças

| data | mudança |
|---|---|
| 31/08/2026 (seg) | A leitura dos arquivos passa a ser feita em lotes de 2, para reduzir o uso de memória no servidor. |
| 31/08/2026 (seg) | O engajamento passa a ter uma fórmula por plataforma, a pedido do produto: o YouTube conta likes e comentários; o Instagram e o TikTok contam likes, comentários e compartilhamentos. |
| 20/08/2026 | A coluna `regiao` entra na chave da tabela `posts`, para o filtro por região do painel. |
| 03/08/2026 | Réplica das tabelas do painel num Postgres usado pelo produto. |
| 15/07/2026 | Primeira versão. |

## Anotações de operação

- **28/08/2026.** O time de coleta avisou que, a partir de 01/09, criadores sem região definida passam a vir com `regiao` nula. Antes vinham com `"desconhecida"`.
- **04/09/2026.** A execução das 03:00, que processa o dia 03/09, caiu por tempo esgotado na réplica. O agendador tentou de novo automaticamente às 03:41 e a segunda tentativa terminou bem. O log está em `log_producao_2026-09-04.txt`.
