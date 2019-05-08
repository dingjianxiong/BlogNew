'''
与用户相关的视图和路由
'''

from . import users
from flask import render_template,request,session,redirect,make_response,url_for
from .. import db
from ..models import *
# from app.models import *
from app.main import viwes


#
# @users.route('/')
# @users.route('/index')
# def index_views():
#     #读取Category中的所有内容并发送到index.htnl显示
#     category=Category.query.all()
#     return render_template('index.html',category=category)

@users.route('/list')
def list_views():
    return render_template('list.html')



@users.route('/login',methods=['GET','POST'])
def login_views():
    if request.method=='GET':
        #获取请求原地址，将地址保存进cookies
        resp=make_response(render_template('login.html'))
        #有就获取地址，没有就返回首页　'/'
        url=request.headers.get('Referer','/')
        resp.set_cookie('url',url)
        return resp
    else:
        username=request.form['username']
        password = request.form['password']
        user=User.query.filter_by(loginname=username,upwd=password).first()
        if user:
            #登录
            # 1.先将登录信息保存进sesson
            #2.从哪儿来回哪儿去（从cookies中获取请求原地址
            session['id']=user.ID
            session['loginname']=user.loginname
            url=request.cookies.get('url')
            return redirect(url)
        else:
            #登录失败
            return render_template('login.html')

@users.route('/logout')
def logout_views():
    #获取请求原地址
    url=request.headers.get('Referer','/')
    #判断session中是否有登录信息，如果有就删除
    if 'id' in session and 'loginname' in session:
        del session['id']
        del session['loginname']
    #重定向到原地址
    return redirect(url)

@users.route('/register',methods=['POST','GET'])
def register_views():
    if request.method=='GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        users = User.query.filter_by(loginname=username).first()
        if users:
            return render_template('login.html')
        else:

            email = request.form['email']
            url = request.form['url']
            password = request.form['password']
            user=User()
            user.loginname=username
            user.uname =username
            user.email=email
            user.url=url
            user.upwd=password
            user.is_author=True
            db.session.add(user)
            session['id'] = user.ID
            session['loginname'] = username

            topics = Topic.query.limit(15).all()
            categories = Category.query.all()

        return render_template('index.html',params=locals())


