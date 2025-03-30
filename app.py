from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Required for session management

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

# Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String(500), nullable=False)
    genre = db.Column(db.String(100), nullable=False)  # Added genre column

# Create the database tables (Run once)
with app.app_context():
    db.create_all()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))  # Redirect to login if not logged in
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('index'))  # Redirect to film list
        else:
            return render_template('login.html', error="Invalid username or password.")

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not username or not password or not confirm_password:
            return render_template('signup.html', error="Please fill in all fields.")

        if password != confirm_password:
            return render_template('signup.html', error="Passwords do not match.")

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('signup.html', error="Username already taken.")

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/main')
@login_required
def index():
    films = Film.query.all()  # Fetch all films from the database
    return render_template('index.html', films=films)

@app.route('/film/<int:film_id>')
@login_required  # Ensure only logged-in users can access film pages
def film_page(film_id):
    film = Film.query.get_or_404(film_id)  # Fetch film or return 404
    return render_template('film.html', film=film)

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
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

    return render_template('search.html', films=films)

@app.route('/logout')
def logout():
    session.clear()  # Clears ALL session data
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
