Songs API
===========================================================

A simple REST API developed using Flask, which provides endpoints to get and search songs, post ratings, and get average ratings and difficulties for songs stored in MongoDb database

**How to run locally**
- Install [Docker](https://www.docker.com/products/docker-desktop) on your local machine (if not installed).
- Go to the root directory of application and run `docker-compose up`

Flask API is accessible on `http://localhost:5000`

**How to run test**
- Go to the root directory of application and run `docker-compose run --rm backend pytest`


**Supported endpoints**

|Path                  |Description                                  | Method |
|--------------------- |---------------------------------------------|--------|
/api/songs      | Get list of songs in Db. Query param: page (int)                       | GET    |
/api/songs/search              | Search songs using keyword. Query Param: message (string)                                   | GET    |
/api/songs/avg/difficulty          | Gets average difficulty for all songs of in certain difficulty. Query param: level (int)                        | GET    |
/api/songs/rating| Post a rating for a song                 | POST    |
/api/songs/avg/rating/<song_id>          | Gets average rating of a song by Id                        | GET   |


Relevant Background Information and Pre-Requisites
--------------------------------------------------

  The developer should be familiar with Python programming, basic understanding of RESTful APIs and Flask. The application uses MongoDb as the main database, therefore understanding of NoSQL databases is important. pytest is used for testing.

  The API itself is a standalone application but uses local MongoDb, therefore, in this task the application is run in docker container, where there is one container for Db and the other for the application

  Keywords: Python, Flask, Docker, MongoDb, pytest

Requirements Overview
---------------------

  1. Get songs (support pagination)
  2. Search songs where keyword exists in 'artist' or 'title' 
  3. API to add ratings for a song
  4. Get average difficulty of all songs or songs in a particular difficulty level
  5. Get average rating of a song
  6. All responses should be in JSON
  7. Tests to validate the functionality

Technical Constraints
---------------------

| Constraint | Description                                                                                                                          |
|------------|--------------------------------------------------------------------------------------------------------------------------------------|
| Flask     | We have to implement a backend REST API which requires Flask as the framework.                                                                              |
| MongoDb  | We need a NoSQL database which can store songs and ratings, where schema can be modified easily                                                                               |
| pytest     | Testing needs to be done in order to validate the logic.                                                                     |
| Docker       | We need to be able to run the application locally, without managed MongoDb server |


**Known Issues**
- Test coverage is not exhaustive and could be improved upon.
- Validation schemas can be used for http requests.

**Extensibility and Future work**
- Models could have be used for Songs and Ratings
- If data scales, sharding can be applied to the songs collection to improve query performace
- More tests can be included
