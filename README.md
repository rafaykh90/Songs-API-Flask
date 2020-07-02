# Songs Backend API
API Backend for Songs

**Application Environment**
- Backend Framwork: Flask
- Database: MongoDb

**How to run locally**
- Install [Docker](https://www.docker.com/products/docker-desktop) on your local machine.
- Go to the root directory of application and run `docker-compose up`

##### Run without Docker (Not tested) - Alternate approach:
 - Set environment variable `DATABASE_URL` with the host url for MongoDb (managed)  
 - Set environment variable `FLASK_APP` as `src/app.py` with the host url for MongoDb (managed)  
 - Set environment variable `FLASK_ENV` as `development`with the host url for MongoDb (managed)  
 - Run `cd backend-api`
 - Run `pip install -r requirements.txt`
 - Run `flask run --host=0.0.0.0`

 or Run `FLASK_APP=src/app.py FLASK_ENV=development DATABASE_URL=<replace with your db url including db name> flask run --host=0.0.0.0`

Either way, access the backend on `http://localhost:5000`

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

**Known Issues**
- Naming and structure could be better
- `get_song_metrics` method in `songs_repository` has different types for `rating` based on tests and actual API call
- More tests could be included
- Validation schemas not used for request data for simplicity