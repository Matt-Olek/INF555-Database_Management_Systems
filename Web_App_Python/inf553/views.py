from django.template import loader
from django.shortcuts import render
import psycopg2
import dotenv
import os

dotenv.load_dotenv()

def connect_to_postgres():
    '''Connect to the postgres database and return the connection object'''
    host = "localhost"
    database="pubmed"
    user="postgres"
    password=os.getenv("POSTGRES_PASSWORD")
    port=5432
    con = psycopg2.connect(host=host,database=database,  user=user, password=password, port=port)
    return con

def index(request):
    # ---------------------------------- Connect to Postgres ---------------------------------- #

    con = connect_to_postgres()
    
    # ----------------------------------------- Query 1 ----------------------------------------- #

    query = """SELECT tablename
    FROM pg_catalog.pg_tables
    WHERE schemaname != 'pg_catalog' AND
    schemaname != 'information_schema'; """
    cur = con.cursor()
    cur.execute(query)
    tables = cur.fetchall()
    # ----------------------------------------- Query 2 ----------------------------------------- #

    query = """SELECT * FROM pubmed_article;"""
    cur.execute(query)
    articles = cur.fetchall()

    # ----------------------------------------- Query 3 ----------------------------------------- #

    query = """SELECT 
                DISTINCT journal_title, COUNT(*) AS num_articles 
            FROM 
                pubmed_article 
            GROUP BY 
                journal_title 
            ORDER BY 
                num_articles DESC;"""
    cur.execute(query)
    journals = cur.fetchall()

    cur.close()
    con.close()

    template = loader.get_template('inf553/index.html')
    context = {
        'tables': tables,
        'articles': articles,
        'journals': journals,
    }
    return render(request, 'inf553/index.html', context)

def pubmed_journal(request, journal_title):

    # ---------------------------------- Connect to Postgres ---------------------------------- #

    con = connect_to_postgres()
    

    # ----------------------------------------- Query ------------------------------------------ #

    cur = con.cursor()
    query = """ SELECT
                    DISTINCT pa.author_name
                FROM
                    pubmed_author pa
                JOIN
                    article_author aa ON pa.author_id = aa.author_id
                JOIN
                    pubmed_article pa2 ON aa.article_id = pa2.article_id
                WHERE
                    pa2.journal_title = %s
                GROUP BY
                    pa.author_name
                ORDER BY
                    pa.author_name ASC;
            """

    cur.execute(query, (journal_title.replace("'", "''"),))
    authors = cur.fetchall()

    cur.close()
    con.close()

    template = loader.get_template('inf553/pubmed_journal.html')
    context = {
        'authors': authors,
        'journal_title': journal_title,
    }
    return render(request, 'inf553/pubmed_journal.html', context)


def author(request, author_name):
    
        # ---------------------------------- Connect to Postgres ---------------------------------- #
    
        con = connect_to_postgres()
        
    
        # ----------------------------------------- Query ------------------------------------------ #
    
        cur = con.cursor()
        query = """ SELECT
                        pa2.title,
                        pa2.journal_title,
                        MAX(coi.coi_text) AS coi_text,
                        MAX(pa2.pubmed_link) AS pubmed_link,
                        MAX(pa2.year) AS year,
                        MAX(gi.grant_val) AS grant_val,
                        STRING_AGG(pa.author_name, ', ') AS author_names
                    FROM
                        pubmed_author pa
                    JOIN
                        article_author aa ON pa.author_id = aa.author_id
                    JOIN
                        pubmed_article pa2 ON aa.article_id = pa2.article_id
                    JOIN 
                        article_coi coi ON pa2.article_id = coi.article_id
                    LEFT JOIN
                        article_grant ag ON pa2.article_id = ag.article_id
                    LEFT JOIN
                        grant_info gi ON ag.grant_id = gi.grant_id
                    WHERE
                        pa2.article_id IN (
                            SELECT article_id
                            FROM article_author
                            WHERE author_id IN (
                                SELECT author_id
                                FROM pubmed_author
                                WHERE author_name = %s
                            )
                        )
                    GROUP BY
                        pa2.title, pa2.journal_title
                    ORDER BY
                        pa2.title ASC;
                """
    
        cur.execute(query, (author_name,))
        articles = cur.fetchall()
        
        cur.close()
        con.close()

        template = loader.get_template('inf553/author.html')
        context = {
            'articles': articles,
            'author_name': author_name,
        }
        return render(request, 'inf553/author.html', context)