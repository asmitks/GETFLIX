# This is the main flask app file that holds logic for both the recommendations
from flask import Flask, render_template,request,redirect,url_for,jsonify # For flask implementation  
from bson import ObjectId # For ObjectId to work  
from pymongo import MongoClient  
import os  
import math
  
app = Flask(__name__)  
 
 #importing the MONGODB URI 
client = MongoClient("mongodb://asmit:Mama123456@ds043062.mlab.com:43062/imdb") #host uri  
db = client.imdb   #Select the database  
mov = db.inst #Select the collection name  
dum=db.dummies 
 
 

@app.route('/')
#returning the main page that has all the movies
def my_form():
    return render_template('score.html')
#this is to take input from the sliders and predict the recommendations
@app.route('/', methods=['POST'])
def my_form_post():
    #this dictionary seven stores the value of the sliders that was changed in the main page by the user
    seven={}
    i=0
    #finding the values of the changed sliders
    for m in mov.find():
        s='a'+str(i)
        text = request.form[s]
        seven[m['movieId']]=str(text)
        i+=1
    for k in mov.find():
        if(k['poslink']!='NA'):
            if seven[k['movieId']]=='0':
                del seven[k['movieId']]
    last=0
    #since the new user will be added in the mongo db dummies dataset we are find the latest user
    for k in dum.find():
        last=k['userId']
    #setting the user as the new user of the dummies dataset by introducing a new user
    new=float(last)+1
    #we are creating a new user instance in the dummies dataser by taking the ratings from the slider values which were previously
    # stored in the seven dictionary
    for j in seven:
        f={}
        f['userId']=int(new)
        f['movieId']=int(j)
        f['rating']=int(seven[j])
        #giving a random timestamp
        f['timestamp']=7138982
        #inserting an instance into dummies dataset
        dum.insert(f)

    #declaring curors to access the mongoDB data
    cursor1 = mov.find()
    cursor2 =dum.find()


    #Here the logic for reccomendation starts
    
    #this dictionary will contain the user wise data of the movies they have rated this is our pre-existing  user data
    rating_user={}
    
    #this dictionary contains the movie title with key values as the movieId
    movies={}

    ctr=0

    for q in cursor1:

        
        id=q['movieId']
        title=q['title']
        movies[id]=title
        ctr+=1
    #now we have data in movies dic.
    
    ctr=0
    #now we are creating the rating data by setting rating values for the movies each user has rated
    for e in cursor2:
        user=e['userId']
        rating_user.setdefault(user,{})
        rating_user[user][movies[e['movieId']]]=float(e['rating'])



    #calculating our pearson similarity coefficient for two items which can either be users or items depending on thr algo
    #for simplicity lets assume user-user sim
    def sim(rating_user,p1,p2):


        similar={}
        #finding the movies that both users have rated
        for movies in rating_user[p1]:
            for movies2 in rating_user[p2]:
                if movies==movies2:
                    similar[movies]='common'
                
        
        #finding the number of elements
        n=len(similar)
        #if no elements in common 0 correlation
        if n==0:
            return 0
        
        #adding up the rating_user
        #sum all the squares
        sum1=0
        sum2=0
        sumsq1=0
        sumsq2=0
        for mov in similar:
            sum1+=rating_user[p1][mov]
            sum2+=rating_user[p2][mov]
            sumsq1+=pow(rating_user[p1][mov],2)
            sumsq2+=pow(rating_user[p2][mov],2)
        
        
        
        
                
            
            
        #caluculating summation of products
        prod_sum=0
        for mov in similar:
            prod_sum+=rating_user[p1][mov]*rating_user[p2][mov]
            
        
    

        #calculating the pearson score

        num=prod_sum-(sum1*sum2/n)
        den=math.sqrt((sumsq1-pow(sum1,2)/n)*(sumsq2-pow(sum2,2)/n))
        #preventing div by 0 error
        if den==0:
            return 0

        sim=num/den

        #print(sim)
        return sim

    '''Till now we have made a function to calculate the similarity between 2 users but now we need to recommend our user 
    some movies which is done buy ranking the movies considering the similarity between the users'''
    def recommend(rating_user,person):
        totals={}
        simSums={}
        #traversing all the users
        for other in rating_user:
            #checking if the person is not same as the user
            if other==person: 
                continue
            #storing the similarity score of the two usera
            simp=sim(rating_user,person,other)
            
            #not considering negative similarity
            if simp<=0:
                continue
            
            #traversing the movies the other user has rated    
            for item in rating_user[other]:
                #considering movies not rated by both users and adding normalised scored movies
                if item not in rating_user[person] or rating_user[person][item]==0:
                    totals.setdefault(item,0)
                    totals[item]+=rating_user[other][item]*simp
                    simSums.setdefault(item,0)
                    simSums[item]+=simp
        
        #ranking our recommendations            
        ranks=[(total/simSums[item],item) for item,total in totals.items()]
        ranks.sort()
        #using top matched movies
        ranks.reverse()
        return ranks
    #storing user-user movies    
    ww=recommend(rating_user,float(new))


    #item-item algo

    '''for item-item we need to use a new dictionary instead of using user_ratings we will 
    have a movie key which will contain various ratings by the users'''
    #this means we need to virtually reverse our rating_user dictionary
    def trans(rating_user):
        result={}
        for person in rating_user:
            for item in rating_user[person]:
                result.setdefault(item,{})
                result[item][person]=rating_user[person][item]
        return result


    #returning top similar movies to a movie based on pearson's similarity
    def top(rating_user,i1,n=5):
        scores=[(sim(rating_user,i1,i2),i2) for i2 in rating_user if i2!=i1]
        scores.sort()
        scores.reverse()
        return scores[0:n]

    #storing top 10 similar movies for each movie in the data set
    def simitems(rating_user,n=10):
        result={}
        trating_user=trans(rating_user)
        c=0
        for i in trating_user:
            
            scores=top(trating_user,i,n=n)
            result[i]=scores
        return result
        


#finding top similar movies for the movies rated by the user
    def rec(rating_user,itemM,user):
        rat=rating_user[user]
        scores={}
        totalsim={}

        for(item,rating) in rat.items():
            for(simil,item2) in itemM[item]:
                #making sure not the same movie that was rated
                if item2 in rat:
                    continue
                # giving a small non 0 value to the movie to prevent div by 0 error    
                scores.setdefault(item2,0.001)
                #calculating scores considering the similarity and the ratings
                #weighted sum
                scores[item2]+=simil*rating

                totalsim.setdefault(item2,0.001)
                #finding sum of all the similarities
                totalsim[item2]+=simil
        ranking=[(score/totalsim[item],item) for item,score in scores.items()]

        ranking.sort()
        ranking.reverse()
        return ranking

    


    #storing recommendations of item-item 
    wt=rec(rating_user,simitems(rating_user),new)
    #checking if item-item algo has atleat 4 recommendations 
    if len(wt)>=4:  
        lo1=wt[0][1]
        lo2=wt[1][1]
        lo3=wt[2][1]
        lo4=wt[3][1]
        #lo5=wt[4][1]
        #lo6=wt[5][1]
        #lo7=wt[6][1]
    else:
        return("sorry please try again")
    #checking if user-usr algo has atleast 4 recommendations
    if len(ww)>=4:

        n1=ww[0][1]
        n2=ww[1][1]
        n3=ww[2][1]
        n4=ww[3][1]
        
    #giving values to variables
    if(len(ww)>=4):
        for jk in mov.find():
            if jk['title']==n1:
                i1=str(jk['poslink'])
            elif jk['title']==n2:
                i2=str(jk['poslink'])
            elif jk['title']==n3:
                i3=str(jk['poslink'])
            elif jk['title']==n4:
                i4=str(jk['poslink'])
           

    for jk in mov.find():
        if jk['title']==lo1:
        
            it1=str(jk['poslink'])
            
        elif jk['title']==lo2:
            
           
            it2=str(jk['poslink'])
            

        elif jk['title']==lo3:
           
            it3=str(jk['poslink'])
            
        elif jk['title']==lo4:
           
            it4=str(jk['poslink'])
            

    #checking if user-user algo has atleat 4 recommendations
    if(len(ww)<=4):
        return render_template('recommend1.html',it1=it1,lo1=lo1,it2=it2,lo2=lo2,it3=it3,lo3=lo3,it4=it4,lo4=lo4)
    else:
        return render_template('recommend.html',i1=i1,i2=i2,i3=i3,i4=i4,n1=n1,n2=n2,n3=n3,n4=n4,it1=it1,lo1=lo1,it2=it2,lo2=lo2,it3=it3,lo3=lo3,it4=it4,lo4=lo4)

if __name__ == "__main__":  
  
    #app.run(debug=True) 
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


