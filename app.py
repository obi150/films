from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from functools import wraps # Szükséges library-k meghívása

app = Flask(__name__) # App létrahozása
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Adatbázis betöltése
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'  # Fontos a session kapcsolathoz

db = SQLAlchemy(app) # Adatbázis inicializálása
bcrypt = Bcrypt(app) # Jelszavak cryptálására alkalmazott objetktum
migrate = Migrate(app, db)  # Migráláshoz használt obj

# Adatbázis modelek
class User(db.Model): # Felhasználó
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Favorite(db.Model): # Kedvenc filmek
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('favorites', lazy=True))
    film = db.relationship('Film', backref=db.backref('favorited_by', lazy=True))

class FilmActor(db.Model): # Film - szereplő kapcsolat
    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'), nullable=False)

class Film(db.Model): # Filmek
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String(500), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    trailer_url = db.Column(db.String(500), nullable=False)
    actors = db.relationship('Actor', secondary='film_actor', backref='films')
    rating = db.Column(db.Float, nullable=False)

class Actor(db.Model): # Szereplők
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    photo_url = db.Column(db.String(500), nullable=True)

# Változtatások létrehozása/elmentése
with app.app_context():
    db.create_all()

# A függvény, amely nem enged be nem jelentkezett embereket belépni, ezeket átirányitja a login page-re
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Kezdő út/route
@app.route('/')
def home():
    return redirect(url_for('login')) # Átirányítja a login page-re

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'] # Megkapja a felhasználónevet és a jelszót
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password): # Vizsgálja hogy benne van e
            session['username'] = username
            return redirect(url_for('index'))  # Ha benne van átirányítja a main-re
        else:
            return render_template('login.html', error="Invalid username or password.") # Ha nincs hibaüzenet

    return render_template('login.html')

# Signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'] # Lekéri az adatokat
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not username or not password or not confirm_password: # Vizsgálja a létezését
            return render_template('signup.html', error="Please fill in all fields.")

        if password != confirm_password: # Vizsgálja hogy egyenlő e a két adott jelszó
            return render_template('signup.html', error="Passwords do not match.")

        existing_user = User.query.filter_by(username=username).first()
        if existing_user: # Nem engedi hogy két ugyanolyan username legyen
            return render_template('signup.html', error="Username already taken.")

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') # cryptálja és menti a felhasználót
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login')) # Visszairányítja a login pagera

    return render_template('signup.html')

@app.route('/main')
@login_required
def index():
    user = User.query.filter_by(username=session['username']).first()
    films = Film.query.all()

    # Get the list of film IDs the user has favorited
    user_favorites = [fav.film_id for fav in user.favorites]

    return render_template('index.html', films=films, user_favorites=user_favorites)


@app.route('/film/<int:film_id>')
@login_required
def film_page(film_id):
    user = User.query.filter_by(username=session['username']).first()
    user_favorites = [fav.film_id for fav in user.favorites]
    film = Film.query.get_or_404(film_id)

    return render_template('film.html', film=film, actors=film.actors, user_favorites=user_favorites)


@app.route('/actor/<int:actor_id>')
@login_required
def actor_page(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    
    # Get all films where the actor starred
    films = Film.query.join(FilmActor).filter(FilmActor.actor_id == actor.id).all()

    return render_template('actor.html', actor=actor, films=films)

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    user = User.query.filter_by(username=session['username']).first()
    user_favorites = [fav.film_id for fav in user.favorites]
    genre = request.args.get('genre')  # Get genre filter if available
    query = request.args.get('query')  # Get search query if available

    # If a genre is specified, filter by genre
    if genre:
        films = Film.query.filter_by(genre=genre).all()
    # If a search query is provided, search by title
    elif query:
        films = Film.query.filter(Film.title.ilike(f'%{query}%')).all()
    else:
        films = Film.query.all()  # Fetch all films if no filters are applied

    return render_template('search.html', films=films, user_favorites=user_favorites)

@app.route('/search-actor', methods=['GET', 'POST'])
@login_required
def search_actor():
    user = User.query.filter_by(username=session['username']).first()
    query = request.args.get('query')
    if query:
        actors = Actor.query.filter(Actor.name.ilike(f'%{query}%')).all()  # Fetch all actors if no query is provided
    else
        actors = Actor.query.all()

    return render_template('search_actor.html', actors=actors)

@app.route('/favorites', methods=['GET', 'POST'])
@login_required
def your_favorites():
    user = User.query.filter_by(username=session['username']).first()
    user_favorites = [fav.film_id for fav in user.favorites]
    films = Film.query.all()

    return render_template('favorites.html', films=films, user_favorites=user_favorites)


@app.route('/favorite', methods=['POST'])
@login_required
def toggle_favorite():
    user = User.query.filter_by(username=session['username']).first()
    data = request.get_json()
    film_id = data.get("film_id")

    existing_favorite = Favorite.query.filter_by(user_id=user.id, film_id=film_id).first()

    if existing_favorite:
        db.session.delete(existing_favorite)
        db.session.commit()
        return jsonify({"success": True, "favorited": False})  # Unfavorited

    new_favorite = Favorite(user_id=user.id, film_id=film_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"success": True, "favorited": True})  # Favorited



@app.route('/logout')
def logout():
    session.clear()  # Clears ALL session data
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
