import psycopg2
import configparser
from CollectMemeData import CollectMemeData
import os

path = '/projects/python_price_comparison/main'
os.chdir(path)

# Creating a parser object and reading from the config file
parser = configparser.ConfigParser()
parser.read("project.conf")

# Grabing the values from the config file
hostname = parser.get("postgres_config", "hostname")
port = parser.get("postgres_config", "port")
username = parser.get("postgres_config", "username")
dbname = parser.get("postgres_config", "database")
password = parser.get("postgres_config", "password")

class User:

    def __init__(self, userId, username, password, email) -> None:
        self._userId = userId
        self._username = username
        self._password = password
        self._email = email

    @property
    def getUserId(self):
        return self._userId

    @property
    def username(self):
        return self._username

    @username.setter
    def setUserName(self, new_username):
        self._username = new_username

    @property
    def password(self):
        return self._password

    @password.setter
    def setPassword(self, new_password):
        self._password = new_password
        

    def searchMeme(self, memeName: str):
        crawler = CollectMemeData()
        conn = crawler.connectToPostgres()
        cursor = conn.cursor()
        query = f'''
        select url
        from memes
        where name = '{memeName}'
        '''
        cursor.execute(query)
        link = cursor.fetchone()[0]
        return link


if __name__ == '__main__':
    user = User(userId=1, username='bardon', password=1234, email='bdadon50@gmail.com')
    link = user.searchMeme(memeName = 'Success Kid')
    print(link)
