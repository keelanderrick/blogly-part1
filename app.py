"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'aiosdfnopiwsaern'
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def home():
    return redirect('/users')


@app.route('/users')
def users():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)


@app.route('/users/new', methods=["GET"])
def new_user():
    return render_template('users/newuser.html')


@app.route('/users/new', methods=["POST"])
def new_user_submit():
    user = User(first_name=request.form['first_name'],
                last_name=request.form['last_name'], image_url=request.form['image_url'] or None)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('/users/show.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('/users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')
