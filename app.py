from flask import (Flask, render_template, url_for, jsonify,
redirect, flash, session, request, g)

import sqlite3

from functools import wraps
from os import urandom
app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.database = "flaskweb.db"
usernames = []
passwords = []
currentuser=[]
users_dict = dict()
usernameAddingPost=None

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login First.")
            return redirect(url_for('login'))
    return wrap


@app.route('/')
def take_to_home():
    return redirect(url_for('home'))
    
@app.route('/homePage')
def home():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error=None
    db= get_db()
    users_dict = dict(db.execute('SELECT username, password from users'))
    print(users_dict)
    usernames = users_dict.keys()
    passwords = users_dict.values()
    if request.method == 'POST':
        if request.form['username'] in usernames:
            get_key = usernames.index(request.form['username'])
            get_pass = passwords[get_key]
            if request.form['password'] != get_pass:
                error='Username Does not match in our database'
                redirect(url_for('login'))
            else:
                session['logged_in']=True
                session['user_in']=True
                usernameAddingPost=request.form['username']
                currentuser.append(request.form['username'] )
                flash('You are logged in as %s' % request.form['username'])
                print(currentuser[0])
                return redirect(url_for('posts'))

        else:
            flash('Unknown user. Please sign up .')

    return render_template('login.html', error=error)

@app.route('/addPost',methods=['GET', 'POST'])
@login_required
def add_post():
    if request.method == 'POST':
        db = get_db()
        db.execute('INSERT INTO posts(author, title, post) values (?, ?, ?)', 
        [request.form['author'], request.form['title'], request.form['post']])
        """if usernameAddingPost == request.form['author']:
            db.commit()
            flash("New Post has been added successfully")
        else:
            flash('''
            You are trying to add a post as another user. 
            It is not allowed. Use the details that you have logged in with.
            That is. Your author name must be the same as the username you logged in with. Try again.
            ''')"""
        db.commit()
        flash("New Post has been added successfully")
            
    return render_template('addpost.html')
    

@app.route('/myposts')
@login_required
def my_posts():
    db = get_db()
    posts = []
    no_of_posts = None
    try:
        cu = db.execute("select count(post) from posts where author='%s' " % currentuser[0])
        no = list(cu.fetchone())
        no_of_posts=no[0]
        cur = db.execute("select * from posts  where author='%s' " % currentuser[0])
        for row in cur.fetchall():
            posts.append(dict(id=row[0], author=row[1], title=row[2], post=row[3]))
        
    except IndexError:
        print('Index Error')
    print(currentuser)
    return render_template('myposts.html', posts=posts, no_of_posts=no_of_posts)
    


@app.route('/posts')
def posts():
    db = get_db()
    cur = db.execute('select * from posts order by id desc')
    posts  = []
    for row in cur.fetchall():
        posts.append(dict(id=row[0], author=row[1], title=row[2], post=row[3]))
    
    return render_template('posts.html', posts=posts)
    
        

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    msg_to_say=None
    if request.method == 'POST':
        try:
            db = get_db()
            cur = db.execute('INSERT INTO users(username, password, email) values (?, ?, ?)',
            [request.form['username'], request.form['password'], request.form['email']])
            db.commit()
            msg_to_say= "%s have been added successfully." % request.form['username']
            
        except sqlite3.IntegrityError:
            msg_to_say = " Seems we have some of your details in our databases. Try to login. Username or email Already exists. or Try using a new one."
        flash(msg_to_say)   
    return render_template('signin.html')
        

@app.route('/delete', methods=['GET', 'POST'])
def deletepost():
    db = connect_db()
    post_id=request.form['postID']
    if request.method == 'POST':
        db.execute('delete from posts where id = ? ' , [post_id])
        flash('Post was deleted.')
        print(request.form['postID'])
    return redirect(url_for('posts'))

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_in', None)
    try:
        print('Removing user %s' % currentuser[0])
        print(currentuser)
        currentuser.remove(currentuser[0])
        print(currentuser)
    except IndexError:
        pass
    flash('You have logged out. Bye!')
    return render_template('logout.html')


@app.route('/moreinfo')
def moreinfo():
    return jsonify({
        "What" : "There is no more information You need to Know."
    })

@app.route('/contactus')
def contactus():
    return jsonify({
        "Email" : "myemail@myname.com",
        "Phone" : "+254709345673",
        "Facebook" : "facebook/myname",
        "twitter" : "@myname"
    })

@app.route('/aboutme')
def aboutme():
    return render_template('aboutme.html')

    
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.errorhandler(404)
def not_found(error):
       return render_template('error.html')



def connect_db():
    return sqlite3.connect(app.database)




if __name__ == '__main__':
    app.run(debug=True)
