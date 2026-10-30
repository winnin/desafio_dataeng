# Desafio técnico: Engenharia de Dados

Obrigado por participar do processo. Este desafio se parece com o trabalho do dia a dia. Os dados chegam de mais de uma fonte, do jeito que chegam, e precisam virar tabelas confiáveis para outros times usarem.

**Tempo esperado: de 4 a 6 horas.** Você tem 7 dias corridos para entregar. Não esperamos perfeição. Preferimos menos coisa, bem feita e bem explicada, a tudo pela metade.

## Contexto

Acompanhamos o desempenho de posts públicos de criadores de conteúdo no YouTube, no Instagram e no TikTok. Dois coletores observam cada post várias vezes por dia e entregam o que viram em arquivos:

- **api**: lê a API oficial das plataformas;
- **pagina**: lê a página pública do post.

Cada observação é uma foto das métricas de um post naquele momento. Ao longo dos dias, o mesmo post aparece dezenas de vezes.

Dois times usam esses dados:

- o **produto** mostra aos clientes o estado atual de cada post;
- a **ciência de dados** estuda como os posts crescem nos primeiros 30 dias depois de publicados.

## Os dados

A pasta `dados/` tem 10 dias de arquivos, organizados pela **data em que o arquivo chegou** (em UTC):

```
dados/
├── 2026-09-01/
│   ├── api_20260901T062214_3fa2c1.jsonl.gz
│   ├── pagina_20260901T124501_9b07e3.jsonl.gz
│   └── ...
├── ...
└── 2026-09-10/
```

Cada arquivo é compactado com gzip e traz uma observação JSON por linha. Por exemplo, uma linha da fonte api (formatada para leitura):

```json
{
  "source": "api",
  "platform": "tt",
  "post_id": "7400000000000000001",
  "creator_id": "6800000000000000001",
  "published_at": "2026-09-02T14:03:11Z",
  "collected_at": "2026-09-03T08:12:45Z",
  "status": "active",
  "metrics": {"views": 15234, "likes": 812, "comments": 40}
}
```

O que sabemos das fontes (a documentação está incompleta, como costuma estar):

- `status` vale `active` ou `removed`, e `removed` quer dizer que o post foi removido ou ficou privado;
- as métricas possíveis são `views`, `likes`, `comments` e `shares`, e cada fonte traz só algumas delas;
- a fonte pagina escreve algumas coisas de um jeito diferente da api.

Os arquivos estão como chegaram, sem limpeza nem correção. Descobrir o que há neles faz parte do desafio.

## O que construir

1. **Um pipeline que processa um dia de chegada por vez.** Crie um comando para processar um dia e outro (ou o mesmo) para processar um intervalo de dias. Reprocessar um dia ou um intervalo, quantas vezes for preciso, não pode duplicar nem perder dados. Lembre que arquivos podem chegar atrasados.
2. **A tabela `posts_estado_atual`.** Uma linha por post, com o estado mais recente que conhecemos dele.
3. **A tabela `posts_curva_diaria`.** Uma linha por post e por dia desde a publicação (do dia 0 ao dia 30), com as métricas do post ao final daquele dia. Você decide o que "dia N" significa e o que fazer em dias sem coleta. Registre essa decisão.
4. **Checagens de qualidade.** Elas rodam a cada execução e deixam um resultado que outra pessoa consegue ler. Nenhum registro pode ser descartado em silêncio: o que for rejeitado fica guardado, com o motivo.
5. **Testes automatizados.** Cubra o que você considera mais arriscado no seu pipeline.

### Contrato de saída

Depois de processar os 10 dias, exporte as duas tabelas para a pasta `saida/`, em CSV ou Parquet, com os nomes `posts_estado_atual` e `posts_curva_diaria`. Elas devem ter pelo menos as colunas abaixo, e podem ter outras.

**posts_estado_atual**

| coluna | tipo | observação |
|---|---|---|
| `platform` | texto | `yt`, `ig` ou `tt` |
| `post_id` | texto | |
| `creator_id` | texto | |
| `published_at` | data e hora | em UTC, no formato ISO 8601 |
| `status` | texto | `active` ou `removed` |
| `views`, `likes`, `comments`, `shares` | inteiro | vazio quando não se sabe |

**posts_curva_diaria**

| coluna | tipo | observação |
|---|---|---|
| `platform` | texto | `yt`, `ig` ou `tt` |
| `post_id` | texto | |
| `dia` | inteiro | de 0 a 30 |
| `views`, `likes`, `comments`, `shares` | inteiro | valor ao final do dia; vazio quando não se sabe |

## Ferramentas

- Use Python (3.10 ou mais novo) e SQL. Para processar, escolha o que preferir: DuckDB, Polars, pandas, PySpark local ou outra ferramenta.
- Tudo precisa rodar no seu computador, sem conta em nuvem. Docker é opcional.
- Instalar e rodar tem que ser simples: dois ou três comandos no seu README.

## Uso de IA

Pode usar IA à vontade (Claude, Copilot, ChatGPT ou outra). Nós usamos no dia a dia. Pedimos só duas coisas:

- conte como usou, em `USO_DE_IA.md`: onde ajudou e o que você corrigiu ou rejeitou;
- entenda tudo o que entregar, porque na conversa técnica você vai explicar o código e mudar uma parte dele ao vivo.

Usar IA não tira ponto. Entregar código que você não sabe explicar tira.

## O que entregar

Um repositório git, que pode ser um link do GitHub ou do GitLab, ou um `.zip` com a pasta `.git`. Você pode trabalhar direto numa cópia deste repositório. Ele deve conter:

- o código e os testes;
- um `README.md` explicando como instalar, rodar o pipeline e rodar os testes;
- o `DECISOES.md`, com as decisões que você tomou e por quê (há um modelo nesta pasta);
- o `USO_DE_IA.md` (também há um modelo nesta pasta);
- a pasta `saida/` gerada pela sua última execução.

## Como avaliamos

- **Modelagem:** a granularidade de cada tabela e a regra de cada campo.
- **Reprocessamento:** o que acontece quando um dia roda de novo, quando um arquivo chega atrasado e quando algo falha no meio.
- **Qualidade e testes:** o que você checa, o que você testa e por quê.
- **Operação:** como isso rodaria todo dia em produção, e o que mudaria com mil vezes mais dados.
- **Comunicação:** a clareza do README, do `DECISOES.md` e da conversa.

Depois da entrega, marcamos uma conversa de cerca de 60 minutos. Você apresenta a solução, responde perguntas sobre o código e faz uma pequena mudança nele com a tela compartilhada. Pode usar IA nessa hora também.

## Se algo parecer ambíguo

Algumas coisas são ambíguas de propósito, e não existe uma única resposta certa. Decida, registre em `DECISOES.md` e siga em frente: isso também é avaliado. Se algo impedir você de continuar, responda à mensagem de quem enviou o desafio.

## Desafio extra (opcional)

A pasta [`extra/`](extra/README.md) tem um segundo desafio, menor: um incidente num pipeline antigo. Ele é **opcional** e conta como diferencial; deixar de fazer não tira ponto. Faça só se sobrar tempo depois do principal.
