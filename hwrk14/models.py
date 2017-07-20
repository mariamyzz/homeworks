# -*- coding: utf-8 -*-

from datetime import date
from app import db


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

    body = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.Date, default=date.today)
    is_visible = db.Column(db.Boolean, default=True)

