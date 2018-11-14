# coding:utf8
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import pymysql

app = Flask(__name__)
app.config.from_object('settings.DevConfig')
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://%s:%s@%s/movie" % (
    app.config.get('DB_USER'), app.config.get('DB_PWD'), app.config.get('DB_URI'))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


# 会员表
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    pwd = db.Column(db.String(200))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(11), unique=True)
    info = db.Column(db.Text)
    face = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    uuid = db.Column(db.String(255), unique=True)
    isdelete = db.Column(db.Boolean, default=False)
    userlogs = db.relationship('Userlog', backref='user')  # 会员日志表外键关系绑定
    comments = db.relationship('Comment', backref='user')
    moviecols = db.relationship('Moviecol', backref='user')

    def __repr__(self):
        return '<User %r>' % self.name


# 会员登录日志表
class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)
    used_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    uuid = db.Column(db.String(255), unique=True)
    isdelete = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Userlog %r>' % self.id


# 标签
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    isdelete = db.Column(db.Boolean, default=False)
    movies = db.relationship("Movie", backref='tag')

    def __repr__(self):
        return '<Tag %r>' % self.name


# 电影
class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    info = db.Column(db.Text)
    logo = db.Column(db.String(255), unique=True)
    star = db.Column(db.SmallInteger)
    playnum = db.Column(db.BigInteger)
    commentnum = db.Column(db.BigInteger)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    area = db.Column(db.String(255))
    release_time = db.Column(db.Date)
    length = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    isdelete = db.Column(db.Boolean, default=False)
    comments = db.relationship('Comment', backref='movie')
    moviecols = db.relationship('Moviecol', backref='movie')

    def __repr__(self):
        return '<Movie %r>' % self.title


# 上映预告
class Preview(db.Model):
    __tablename__ = "preview"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    logo = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    isdelete = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Preview %r>' % self.title


# 评论
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    isdelete = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Comment %r>' % self.id


# 电影收藏
class Moviecol(db.Model):
    __tablename__ = "moviecol"
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    isdelete = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Moviecol %r>' % self.id


# 权限
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    isdelete = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Auth %r>' % self.name


# 角色
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    auths = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    isdelete = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Role %r>' % self.name


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    pwd = db.Column(db.String(200))
    is_super = db.Column(db.SmallInteger)  # 0为超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    isdelete = db.Column(db.Boolean, default=False)
    adminlogs = db.relationship('Adminlog', backref='admin')
    oplogs = db.relationship('Oplog', backref='admin')

    def __repr__(self):
        return '<Admin %r>' % self.name


# 管理员登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    isdelete = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Adminlog %r>' % self.id


# 操作日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    isdelete = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Oplog %r>' % self.id


if __name__ == "__main__":
    # db.create_all()
    '''
    role = Role(name="suncheng",auths='power')
    db.session.add(role)
    db.session.commit()
    '''
    '''
    from werkzeug.security import generate_password_hash
    admin = Admin(
        name='sun',
        pwd=generate_password_hash('123456'),
        is_super=0,
        role_id=1)
    db.session.add(admin)
    db.session.commit()
    '''
    '''
    from modeles import Admin
    for user in Admin.query.all():
        print '***'
        print(user.id, user.name, user.pwd)
    '''