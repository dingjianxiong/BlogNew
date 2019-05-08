'''
只处理与主题相关的路由和视图
'''

from . import main
import datetime
from flask import render_template,request,session,redirect,make_response
from .. import db
from ..models import *
# from app.models import *
import os
# @main.route('/')
# def index_views():
#     return '这是Blog项目中的首页'



@main.route('/')
@main.route('/index')
def index_views():
    #查询Topic中所有的数据并发送到index.html做显示
    topics=Topic.query.limit(15).all()
    categories=Category.query.all()
    #读取Category中的所有内容并发送到index.htnl显示
    category=Category.query.all()
    if 'id' in session and 'loginname' in session:
        id=session['id']
        user=User.query.filter_by(ID=id).first()
    return render_template('index.html',params=locals())






@main.route('/release',methods=['GET','POST'])
def release_views():
    if request.method=='GET':
        #判断session 是否有登录用户
        if 'id' in session and 'loginname' in session:
            id = session['id']
            user = User.query.filter_by(ID=id).first()
            if user.is_author:
                # 1.查询Category的所有的信息
                categories = Category.query.all()
                # 2.查询BlogType的所有的信息
                blogTypes = BlogType.query.all();
                return render_template("release.html", params=locals())
        return redirect('/')
    else:
        #创建Topic对象
        topic=Topic()
        #获取标题(author)为Topic赋值
        #获取文章类型list为Topic.blogType_id赋值
        #获取内容类型(category）为Topic.categroy_id赋值
        #获取内容（content）为Topic.content赋值
        #从session中获取id为Topic.user_id赋值
        topic.title=request.form['author']
        topic.blogtype_id=request.form['list']
        topic.category_id = request.form['category']
        topic.content= request.form['content']
        topic.user_id=session['id']
        #获取系统时间为Topic.pub_data赋值
        topic.pub_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #判断文件是否有上传图片，处理上传图片，为Topic.imges赋值

        if request.files:
            #获取上传文件,
            #处理文件名:时间.扩展名
            #处理上传的路径：static/upload
            #上传文件
            f = request.files['picture']
            ftime=datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            ext=f.filename.split('.')[-1]
            filename=ftime+'.'+ext
            topic.images='upload/'+filename
            basedir = os.path.dirname(os.path.dirname(__file__))
            upload_path = os.path.join(basedir, 'static/upload', filename)
            # 上传文件
            f.save(upload_path)
            # 将Topic的对象保存进数据库
        db.session.add(topic)
        return redirect('/')

# @main.route('/info',methods=['GET','POST'])
# def release_views():
#     return render_template('')


@main.route('/list')
def list_views():
    return render_template('list.html')