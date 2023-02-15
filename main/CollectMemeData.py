import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import psycopg2
import configparser

# Creating a parser object and reading from the config file
parser = configparser.ConfigParser()
parser.read("main/project.conf")

# Grabing the values from the config file
hostname = parser.get("postgres_config", "hostname")
port = parser.get("postgres_config", "port")
username = parser.get("postgres_config", "username")
dbname = parser.get("postgres_config", "database")
password = parser.get("postgres_config", "password")

class CollectMemeData:
    
    def sendHTTP(self, url: str) -> BeautifulSoup:
    
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
        

    def getData(self, soup: BeautifulSoup):

        # Extract meme dictionary
        meme_data = json.loads(soup.text)['data']['memes']
        meme_df = pd.DataFrame(columns=['id', 'name', 'url', 'width', 'height', 'box_count', 'captions'])

        # Extract memes from dictionary and convert to Pandas DataFrame
        for meme in meme_data:

            temp_df = pd.DataFrame(meme, index=[0])
            meme_df = pd.concat([meme_df, temp_df])

        # Pre-processing
        meme_df[['id', 'width', 'height','box_count', 'captions']] = meme_df[['id', 'width', 'height','box_count', 'captions']].astype('int64')
        meme_df = meme_df.sort_values('id', ascending=False).reset_index().drop(columns=['index'], axis = 1)
        meme_df['name'] = meme_df.name.str.replace("'", '')

        return meme_df

    def connectToPostgres(self):

        # Connecting to Postgres
        conn = psycopg2.connect(host=hostname,
                user=username,
                password=password,
                database=dbname,
                port=int(port))

        return conn


    def loadData(self, meme_df: pd.DataFrame):

        conn = self.connectToPostgres()

        cursor = conn.cursor()

        # Convert the Dataframe into a list of arrays
        records = meme_df.to_records(index=False)

        # Convert the list of arrays into a tuple of tuples
        result = tuple(records)

        for data in range(0,len(result)):

            # Create a new record
            query = "insert into memes (meme_id,name,url,width,height,box_count,captions) values {}".format(result[data])

            # Execute the query
            cursor.execute(query)

            # Commit the transaction
            conn.commit()

        conn.close()

    def cleanDatabase(self):

        conn = self.connectToPostgres()
        cursor = conn.cursor()
        query = '''
        drop table if exists memes;
        create table memes(
            meme_id int not null primary key,
            name varchar(100) not null,
            url varchar(100) not null,
            width int not null,
            height int not null,
            box_count int not null,
            captions int not null
        );
        '''
        cursor.execute(query)
        conn.commit()
        conn.close()


if __name__ == '__main__':
    url = 'https://api.imgflip.com/get_memes'
    crawler = CollectMemeData()
    soup = crawler.sendHTTP(url)
    meme_df = crawler.getData(soup)
    crawler.cleanDatabase()
    crawler.loadData(meme_df)

    conn = crawler.connectToPostgres()
    cursor = conn.cursor()
    query = '''
    select *
    from memes;
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    print(len(results))
    






