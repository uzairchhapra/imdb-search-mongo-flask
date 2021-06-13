from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from flask_pymongo import PyMongo
import bcrypt
import secrets
from flask.json import JSONEncoder
from bson import ObjectId
from encoder import CustomJSONEncoder
from customSearch import customSearch

app = Flask(__name__)

app.json_encoder = CustomJSONEncoder

app.config['MONGO_DBNAME'] = 'myFirstDatabase'
app.config['MONGO_URI'] = 'mongodb+srv://test:test@cluster0.n7kq9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getAdminStatus')
def getAdminStatus():
    isAdmin = False
    if not session.get("username") is None:
        user = mongo.db.users.find_one({'name':session['username']})
        if user['admin']:
            isAdmin = True

    return jsonify({'isAdmin':isAdmin})

@app.route('/genre')
def genre():
    """Fetches a distinct list of all genres in the database.

    Returns:
        JSON: JSONArray of Unique Genres in the Database
    """
    genreList=list(mongo.db.movies.distinct('genre'))
    # response=[]
    # for i in range(len(genreList)):
    #     response.append({'name': genreList[i], 'id':genreList[i]})
    # print(response)
    # return jsonify(response)
    return jsonify(genreList)

@app.route('/delete', methods=['POST'])
def delete():
    """Deletes a Particular Movie and all its parameters using the unique Mongodb ObjectId

    Returns:
        JSON: Returns the delted movie object
    """
    if request.method == 'POST':
        print(request.values.get('id'))
        deletedMovie=mongo.db.movies.find_one_and_delete({'_id' : ObjectId(request.form['id'])})
        return jsonify(deletedMovie)

@app.route('/login', methods=['POST','GET'])
def login():
    """If the request is a GET request, it renders the login page.
    If the request is a POST request, it validates user's credentials.
    If the credentials are valid, it sets the session attribute. Else, it returns an error string.
    """
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'name' : request.form['username']})

        if login_user:
            if bcrypt.checkpw(request.form['pass'].encode('utf-8'),login_user['password']):
                session['username'] = request.form['username']
                session['admin'] = login_user['admin']
                return redirect(url_for('index'))

        return 'Invalid username/password combination'
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register(): 
    """If the request is a GET request, it renders the register page.
    If the request is a POST request, it checks if the user already exists.
    If not, then it creates a new record in the database. The password is encrypted and stored.

    """
    if request.method == 'POST':
        users = mongo.db.users
        admin=False
        existing_user = users.find_one({'name' : request.form['username']})
        print('Admin',request.form.get('admin'))

        if existing_user is None:
            hashpass = bcrypt.hashpw(str(request.form['pass']).encode('utf-8'), bcrypt.gensalt())
            if request.form.get('admin'):
                admin=True
            users.insert_one({'name' : request.form['username'], 'password' : hashpass, 'admin':admin})
            session['username'] = request.form['username']
            session['admin'] = admin
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')

@app.route('/logout')
def logout():
    """Logs out the user by clearing the session.

    Returns:
        IndexPage: Redirects to the Home Page
    """
    session.clear()
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search():
    """A POST API that takes all name, director, genre, 99popularity, imdb_score as 

    Returns:
        [type]: [description]
    """
    if request.method == 'POST':
        query=customSearch(request.form.get('name'),request.form.get('director'),request.form.getlist('genre'), request.form.getlist('99popularity'), request.form.getlist('imdb_score'))
        print(query)
        result = list(mongo.db.movies.find(query))
        response={}
        isAdmin = False
        if not session.get("username") is None:
            user = mongo.db.users.find_one({'name':session['username']})
            if user['admin']:
                isAdmin = True
        response['admin']=isAdmin
        response['data']=result
        return jsonify(response)

@app.route('/edit', methods=['POST'])
def edit():
    if request.method == 'POST':
        try:
            print(request.form['genre'], type(request.form['genre']))
            genreList = request.form['genre'].split(',')
            genre = list(map(lambda x: x.strip(), genreList,))
            print(genre)
            selectedMovie = mongo.db.movies.find_one({'_id' : ObjectId(request.form['id'])})
            mongo.db.movies.find_one_and_update(
            {'_id' : ObjectId(request.form['id'])},
            {'$set': {
            'name': request.form['name'],
            'director': request.form['director'],
            'genre':genre,
            '99popularity': float(request.form['99popularity']),
            'imdb_score': float(request.form['imdb_score'])
            }},
            )
            print(selectedMovie)
            return render_template('index.html',success='Movie Edited!')
        except Exception:
            return render_template('index.html',fail='Failed to Edit Movie!')


@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        try:
            print('new')
            values = dict(request.form.items())
            genreList = request.form['genre'].split(',')
            genre = list(map(lambda x: x.strip(), genreList,))
            values['genre']=genre
            values.pop('_id','No Key Found')
            values['99popularity']=float(values['99popularity'])
            values['imdb_score']=float(values['imdb_score'])

            newMovie = mongo.db.movies.insert_one(values)
            return render_template('index.html',success='New Movie Inserted!')
        except Exception:
            return render_template('index.html',fail='Failed to Insert Movie!')

if __name__ == '__main__':
    app.secret_key = secrets.token_urlsafe(16)
    app.run(debug=True)