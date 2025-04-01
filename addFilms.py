from app import app, db, Film, Actor
from datetime import datetime

with app.app_context():
    # Convert birthday strings to datetime.date objects
    dicaprio = Actor(name="Leonardo DiCaprio", age=49, birthday=datetime.strptime("1974-11-11", "%Y-%m-%d").date(), photo_url="https://cdn.britannica.com/65/227665-050-D74A477E/American-actor-Leonardo-DiCaprio-2016.jpg")
    bale = Actor(name="Christian Bale", age=50, birthday=datetime.strptime("1974-01-30", "%Y-%m-%d").date(), photo_url="https://m.media-amazon.com/images/M/MV5BMTkxMzk4MjQ4MF5BMl5BanBnXkFtZTcwMzExODQxOA@@._V1_.jpg")
    sandler = Actor(name="Adam Sandler", age=57, birthday=datetime.strptime("1966-09-09", "%Y-%m-%d").date(), photo_url="https://cdn.britannica.com/52/243652-050-FEE0A5E4/Actor-Adam-Sandler-2019.jpg")
    carrey = Actor(name="Jim Carrey", age=62, birthday=datetime.strptime("1962-01-17", "%Y-%m-%d").date(), photo_url="https://m.media-amazon.com/images/M/MV5BMTQwMjAwNzI0M15BMl5BanBnXkFtZTcwOTY1MTMyOQ@@._V1_.jpg")

    db.session.add_all([dicaprio, bale, sandler, carrey])
    db.session.commit()

    # Create films and assign actors
    inception = Film(
        title="Inception",
        description="A mind-bending thriller about dream manipulation.",
        release_year=2010,
        poster_url="https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_FMjpg_UX1000_.jpg",
        genre="Sci-fi",
        director="Christopher Nolan",
        trailer_url="https://www.youtube.com/watch?v=YoHD9XEInc0",
        actors=[dicaprio],
        rating=4.1
    )

    dark_knight = Film(
        title="The Dark Knight",
        description="A superhero film about Batman's fight against the Joker.",
        release_year=2008,
        poster_url="https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_FMjpg_UX1000_.jpg",
        genre="Action",
        director="Christopher Nolan",
        trailer_url="https://www.youtube.com/watch?v=EXeTwQWrcwY",
        actors=[bale],
        rating=4.5
    )

    click = Film(
        title="Click",
        description="American comedy drama.",
        release_year=2006,
        poster_url="https://upload.wikimedia.org/wikipedia/en/b/bd/Click_film.jpg",
        genre="Comedy",
        director="Frank Coraci",
        trailer_url="https://www.youtube.com/watch?v=R8NDy8Ke1cc",
        actors=[sandler],
        rating=3.8
    )

    truman_show = Film(
        title="The Truman Show",
        description="A psychological comedy-drama film.",
        release_year=1998,
        poster_url="https://upload.wikimedia.org/wikipedia/en/thumb/b/b8/TheTrumanShowSoundtrack.jpg/220px-TheTrumanShowSoundtrack.jpg",
        genre="Comedy",
        director="Peter Weir",
        trailer_url="https://www.youtube.com/watch?v=dlnmQbPGuls",
        actors=[carrey],
        rating=4.8
    )

    db.session.add_all([inception, dark_knight, click, truman_show])
    db.session.commit()


'''with app.app_context():
    db.session.query(Film).delete()  # Delete all rows from the Film table
    db.session.query(Actor).delete()
    db.session.commit()  # Save changes
    print("All films deleted!")'''