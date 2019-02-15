from pymongo import MongoClient 
from requests import get
from bs4 import BeautifulSoup
try: 
    conn = MongoClient('mongodb://asmit:Mama123456@ds127825.mlab.com:27825/data_imdb') 
    conn1=MongoClient('mongodb://asmit:Mama123456@ds043062.mlab.com:43062/imdb') 
    print("Connected successfully!!!") 
except:   
    print("Could not connect to MongoDB") 
  
# database 
db2 = conn1.imdb
db1=conn.data_imdb
# Created or Switched to collection names: my_gfg_collection 
collection1 = db1.movies
collection2=db1.dummies
collection3=db2.movies
coll=db2.inst
collection4=db2.dummies
cursor1=collection1.find()
cursor2=collection2.find()
cursor3=coll.find()
#creatinga new final database and adding poster links
for row in cursor1:
    dic={}
    if(len(str(row['imdbId']))==6):
        url='https://www.imdb.com/title/tt0'+str(row['imdbId'])+"/"
    elif(len(str(row['imdbId']))==7):
        url='https://www.imdb.com/title/tt'+str(row['imdbId'])+"/"
    elif(len(str(row['imdbId']))==5):
        url='https://www.imdb.com/title/tt00'+str(row['imdbId'])+"/"
    elif(len(str(row['imdbId']))==4):
        url='https://www.imdb.com/title/tt000'+str(row['imdbId'])+"/"
    
    dic['movieId']=row['movieId']
    dic['title']=row['title']
    dic['genres']=row['genres']
    dic['imdbId']=row['imdbId']
    dic['tmdbId']=row['tmdbId']
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    movie_container=html_soup.find_all('div',class_="poster")
    if len(movie_container)!=0:
        a=movie_container[0].a.img['src']
    else:
        a='NA'
    span=html_soup.find("span",id="titleYear")
    if(span!=None):
        dic['year']=span.a.text
    #if year not prsesnt
    else:
        dic['year']='1997'

    dic['poslink']=a
    coll.insert(dic)
    print(dic)


#copying user rating data
for row in cursor2:
    dic={}
    dic['movieId']=row['movieId']
    dic['userId']=row['userId']
    dic['rating']=row['rating']
    dic['timestamp']=row['timestamp']
    collection4.insert(dic)
    print(dic)    

