import pytest
from main.CollectMemeData import CollectMemeData
from main.user import User
import os

def test_CollectMemeData_sendHTTPGETRequest():
    # Check if HTTP request is successful
    url = 'https://api.imgflip.com/get_memes'    
    crawler = CollectMemeData()
    soup = crawler.sendHTTP(url)
    assert 'Drake Hotline' in soup.text


def test_CollectMemeData_getMemeDF():
    # Check if the meme DataFrame is populated with data
    url = 'https://api.imgflip.com/get_memes' 
    crawler = CollectMemeData()
    soup = crawler.sendHTTP(url)
    meme_df = crawler.getData(soup)
    assert len(meme_df) > 50


def test_CollectMemeData_LoadedData():
    # Check If PostgreSQL has more than 99 records after loading the DataFrame 
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
    assert len(results) > 99

def test_User_searchMeme():
    # Check if a user can search for a meme
    user = User(userId=1, username='bardon', password=1234, email='bdadon50@gmail.com')
    memeName = 'Success Kid'
    link = user.searchMeme(memeName)
    assert 'jpg' in link