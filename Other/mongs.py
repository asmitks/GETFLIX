from pymongo import MongoClient 
import pandas as pd
movies=pd.read_csv('movies.csv')
links=pd.read_csv('links.csv')
ratings=pd.read_csv('ratings.csv')
Movie=pd.merge(links,movies,on='movieId',how='inner')
# 


try: 
    conn = MongoClient('mongodb://asmit:Mama123456@ds127825.mlab.com:27825/data_imdb') 
    print("Connected successfully!!!") 
except:   
    print("Could not connect to MongoDB") 
  
# database 
db = conn.data_imdb
  
# Created or Switched to collection names:  
collection1 = db.movies
collection2=db.dummies
  

  
# Printing the data inserted 
cursor = collection1.find() 
ctr=0
Movie=Movie.sample(frac=0.051)
q=ratings.copy()
k=ratings.copy()
arr=[]

for index,row in Movie.iterrows():
    arr.append(row['movieId']) 

#cleaning the data 
for index,row in q.iterrows():
    if row['movieId'] not in arr :
        k.drop(index,inplace=True)
        
#inserting to database      
for index, row in Movie.iterrows():
    dic={}
    dic['movieId']=str(row['movieId'])
    dic['title']=row['title']
    dic['genres']=row['genres']
    dic['imdbId']=str(row['imdbId'])
    dic['tmdbId']=str(row['tmdbId'])
    collection1.insert(dic)
    print(dic)

for index, row in k.iterrows():
    dic={}
    dic['movieId']=str(row['movieId'])
    dic['rating']=row['rating']
    dic['userId']=str(row['userId'])
    dic['timestamp']=79823794
    collection1.insert(dic)
    print(dic)
           

    