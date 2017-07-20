# -*- coding: utf-8 -*-

import config as config

from datetime import date
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from wtforms_alchemy import ModelForm

app = Flask(__name__, template_folder='templates')
app.config.from_object(config)

db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(140), unique=True, nullable=False)
    content = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.Date, default=date.today)
    is_visible = db.Column(db.Boolean, default=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('post.id'),
        nullable=False,
        index=True
    )

    post = db.relationship(Post, foreign_keys=[post_id, ])

    body = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.Date, default=date.today)
    is_visible = db.Column(db.Boolean, default=True)



class PostForm(ModelForm):
    class Meta:
        model = Post

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		include = ['post_id', ]

@app.route('/create', methods=['GET', 'POST'])
def create_post():
	if request.method == 'GET':
		return render_template('create.html')

	elif request.method == 'POST':
		form = PostForm(request.form)
        
		if form.validate():
			post = Post(**form.data)
			db.session.add(post)
			db.session.commit()
			return 'Thank you for posting.'
        
		else:
			return render_template('validation_error.html')

@app.route('/', methods=['GET'])
def index():
	posts = Post.query.all()
	return render_template('feed.html', posts=posts)

@app.route('/post/<post_id>', methods=['GET', 'POST'])
def post_view(post_id):
	if request.method == 'GET':
		post_id = int(post_id)
		post = Post.query.filter_by(id=post_id).first()
		comments = Comment.query.filter_by(post_id=post_id).all()
		return render_template('post_view.html', post=post, comments=comments)
	else: 
		form = CommentForm(request.form)
		if form.validate():
			comment = Comment(**form.data)
			db.session.add(comment)
			db.session.commit()
			return 'Thank you for leaving a comment.'
		else: 
			return render_template('validation_error.html')


if __name__ == '__main__':
    db.create_all()
    app.run()