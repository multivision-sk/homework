import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbmusic

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# 아래 빈 칸('')을 채워보세요
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20201016', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.number
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis

row_line = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

for line in row_line :
    rank = line.select_one('td.number').text[0:2].strip()
    title = line.select_one('td.info > a.title.ellipsis').text.strip()
    artist = line.select_one('td.info > a.artist.ellipsis').text

    print(rank,title,artist)

    doc = {
        'rank' : rank,
        'title' : title,
        'artist' : artist
    }

    db.musics.insert_one(doc)


first_rank = db.musics.find_one({'rank':'1'})
first_title = first_rank['title']
first_artist = first_rank['artist']
print()

print(f'이번주 1위곡은 {first_artist}의 {first_title}입니다.')






