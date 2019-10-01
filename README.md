# GETFLIX
# Precog Project
This is a :movie_camera: movie recommendation system based on collaborative learning (user-user and item-item) which was applied on the IMDB 
database.The recommendation system asks for ratings on 4 or more movies out of approx. 500 movies and returns 4 recommendations each
for User-User and Item-Item collaborative learning algorithms.
![alt text](https://raw.githubusercontent.com/asmitks/images/master/a.png)

## Tools Used
- Python 3.5
- Mongo DB
- Docker
- Heroku
- mlab
- PyMongo
- Flask
- HTML/CSS
- Pandas
- Beautiful soup


## Sources Referred
- **Collective Intelligence** by *Toby Segaran* 

## How to Use?

You can find the hosted app here [GETFLIX](https://get1flix.herokuapp.com/)

### How to use the app?

At the above link you will see a page with approx. 500 movies.You need to rate any 4(k) or more movies and press submit at the bottom of the page 
to get your recommendations

you can rate the movies by moving the slider thumb to 5 possible positions from (1 to 5) initially all sliders are at 0th position

        
      
![alt text](https://raw.githubusercontent.com/asmitks/images/master/123.png)


You will be presented 4 recommendations each of user-user and item-item collaborative learning.
> It is possible that user-user algo doesn't return 4 movies due to its dependency on the data of user ratings.

## Explanation
for explanation behind the algos and a brief report refer to `Report.pdf`

## Code Details
Brief description of folder/files in the repo.

## app.py
The main python3 flask file that contains the main algorithms and logic
#### how to run
```bash
python3 app.py 
```
## templates
#### score.html
Main template that is returned as the home page
#### recommend.html
Template that is returned when both algos return answers
#### recommend1.html
Template is returned when user-user algo does not return answer.
## static
contains the css file style.css
## Other
It contains all raw data taken from movie lense.
### mongs.py
Used for creating mongo db database after data cleaning 
``` bash 
python3 other/mongs.py
```
### scrape.py
Used for scraping thumbnails from dedicated sites of imdb
```bash 
python3 other/scrape.py
```
### change.py
Used for printing required tags that need to be inserted into HTML file.
```
bash python3 other/change.py
```
## Dockerfile
Used to run using docker
commands to run using docker
To run the dockerfile:
```bash 
docker build -t flask-getflix:latest .
```
To run the app:
```bash 
 docker run flask-getflix
```
## How to access mongoDB collections using mongolab.
The mongoDB collections that I used can be accessed thorough 
#### imdb database
``` bash
MONGODB_URI='mongodb://asmit:Mama123456@ds043062.mlab.com:43062/imdb'
```
#### data_imdb
``` bash
MONGODB_URI='mongodb://asmit:Mama123456@ds127825.mlab.com:27825/data_imdb'
```
