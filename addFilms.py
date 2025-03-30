from app import db, Film, app  # Import app from your main file

#with app.app_context():
 #   film1 = Film(title="Click", description="American comedy drama.", release_year=2006, poster_url="https://upload.wikimedia.org/wikipedia/en/b/bd/Click_film.jpg")
  #  film2 = Film(title="Truman Show", description="American psychological comedy-drama film.", release_year=1998, poster_url="https://upload.wikimedia.org/wikipedia/en/thumb/b/b8/TheTrumanShowSoundtrack.jpg/220px-TheTrumanShowSoundtrack.jpg")
  #
    #db.session.add_all([film1, film2])
    #db.session.commit()

#print("Films added successfully!")

from app import app, db, Film

# Create a new film with a genre
with app.app_context():
    new_film = Film(
        title="Inception",
        description="A mind-bending thriller about dream manipulation.",
        release_year=2010,
        poster_url="https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_FMjpg_UX1000_.jpg",
        genre="Sci-fi"  # Adding genre here
    )
    db.session.add(new_film)
    db.session.commit()

    new_film2 = Film(
        title="The Dark Knight",
        description="A superhero film about Batman's fight against the Joker.",
        release_year=2008,
        poster_url="https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_FMjpg_UX1000_.jpg",
        genre="Action"  # Adding genre here
    )

    db.session.add(new_film2)
    db.session.commit()

    new_film3 = Film(
        title="Click",
        description="American comedy drama.",
        release_year=2006,
        poster_url="https://upload.wikimedia.org/wikipedia/en/b/bd/Click_film.jpg",
        genre="Comedy"  # Adding genre here
    )
    db.session.add(new_film3)
    db.session.commit()

    new_film4 = Film(
        title="Truman Show",
        description="American psychological comedy-drama film.",
        release_year=1998,
        poster_url="https://upload.wikimedia.org/wikipedia/en/thumb/b/b8/TheTrumanShowSoundtrack.jpg/220px-TheTrumanShowSoundtrack.jpg",
        genre="Comedy"  # Adding genre here
    )
    db.session.add(new_film4)
    db.session.commit()

#with app.app_context():
 #   db.session.query(Film).delete()  # Delete all rows from the Film table
  #  db.session.commit()  # Save changes
   # print("All films deleted!")