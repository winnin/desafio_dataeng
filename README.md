# Desafio Data Engineer Winnin

## Instruções
Usar o Databricks Community para realizar a tarefa. Caso não tenha cadastro fazer o  cadastro em https://www.databricks.com/try-databricks#account e na tela de escolher o plano escolha "Get started with Community Edition"

Ao fazer Login crie um cluster no menu "Compute"

Para carregar os arquivos e poder gerar as tabelas a partir deles use o menu "Catalog"->Create Table->Drop Files To Upload, or click to browse. Depois do upload ele mostra o path do arquivo

Temos 2 arquivos para serem carregados:

- 1-wiki_pages.json.gz com nomes de criadores de conteúdo(wiki_page) para buscar na API da wikipedia o user_id do respectivo criador no youtube.
- 2-posts_creator_json.json.gz com dados de posts de criadores de conteúdo (creator_id,views,likes,title,published_at,tags,yt_user)


## Exercícios

1. Criar o notebook "1 - create_table_creators_scrape_wiki" que le o arquivo 1-wiki_pages.json.gz e cria a tabela delta default.creators_scrape_wiki

2. Criar o notebook "2 - create_table_posts_creator" que le o arquivo 2-posts_creator_json.json.gz e cria a tabela delta default.posts_creator

3. Criar o notebook "3 - create_table_user_yt_from_wikipedia_api" para gerar a tabela delta default.users_yt
    * Usar a tabela default.creators_scrape_wiki para buscar na api da wikipedia o user_id do youtube de cada wiki_name
    * Campos da tabela default.users_yt:  user_id(extraido da wikipedia) e o wiki_page(da tabela default.creators_scrape_wiki)
    * Exemplo de 1 registro da tabela {'user_id': 'felipeneto', 'wiki_page': 'Felipe_Neto'}    

4. Criar o notebook "4 - analyze_creators"
    * Usar o join da default.users_yt com a default.posts_creator para gerar analises desses creators
        - Mostrar o top 3 posts ordenado por likes de cada creator nos últimos 6 meses (user_id, title, likes, rank)
        - Mostrar o top 3 posts ordenado por views de cada creator nos últimos 6 meses (user_id, title, views, rank)
        - Mostrar os yt_user que estão na tabela default.post_creator mas não estão na tabela default.users_yt
        - Mostrar a quantidade de publicações por mês de cada creator.
            - Exercício Extra 1: mostrar 0 nos meses que não tem video
            - Exercício Extra 2: transformar a tabela no formato que a primeira coluna é o user_id e temos uma coluna para cada mês. 
                - ex: 
                    - user_id, 2024/01, 2024/02, 2024/03
                    - felipeneto, 10, 20, 30
                    - lucasneto, 5, 10, 15
            - Exercício Extra 3: Mostrar as 3 tags mais utilizadas por criador de conteúdo

## Envio
Exportar todo seu workspace e nos enviar como um projeto github.
 
Para exportar va no menu workspace->users->seu usuário->clicar na setinha pra baixo->export->source file
