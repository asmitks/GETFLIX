# this file is for getting html tags of the images that need to be dtored in the html file
from pymongo import MongoClient 


try: 
    
    conn=MongoClient('mongodb://asmit:Mama123456@ds043062.mlab.com:43062/imdb') 
    print("Connected successfully!!!") 
except:   
    print("Could not connect to MongoDB") 
  
# database 
db = conn.imdb

collection=db.inst
cursor=collection.find()




# printing the required tags for insertion in html file 
i=0
for row in cursor:
        
    s='<div class="box"><div class="movie"><div class="movie-image"> <span class="play"><span class="name">X-MAN</span></span> <a href="#"><img src=\''+str(row['poslink'])+'\''+'></a> </div><div class="rating"><p>'+str(row['title'])+'</p><div class="slidecontainer"><input type="range" min="0" max="5" value="0" class="slider" id="myRange" name=\'a'+str(i)+'\'></div></div></div></div>'
    if i==107:
    
        print(s)
    i+=1    
