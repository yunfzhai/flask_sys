#!/Users/yunfzhai/www/ven3/bin/python
# -*- coding:utf-8 -*-
# 从网上学来的！！！
from flask import Flask,request,url_for,make_response
app = Flask(__name__)

@app.route('/')
def index():
	return '<h1> Hello World, Cash!</h1>'
#访问ck页面时设置cookie，访问page2时读取cookie
#主要是 make_response的用法
@app.route('/ck')
def v_indexck():
    rsp = make_response('go <a href="%s">page2</a>' % url_for('v_page2'))
    rsp.set_cookie('user','JJJJJohnny')
    return rsp

@app.route('/page2')
def v_page2():
    user = request.cookies['user']
    return 'you are %s' % user



#用make_response()函数来构造一个Response对象，第一个参数为响应的正文
@app.route('/zping')
def v_index():
    return '<a href="%s">ping</a>' % url_for('v_ping')

@app.route('/ping')
def v_ping():
    rsp = make_response('pong')
    rsp.mimetype = 'text/plain'
    rsp.headers['x-tag'] = 'sth.magic'
    return rsp



# get方式，则是args方式
@app.route('/get')
def v_index_get():
    return '''
        <form method="GET" action="/search">
            <input type="text" placeholder="input keywords" value="Python Flask" name="q"> <br />
            <input type="text" name="page"> <br />
            <input type="submit" value="search">
        </form>
    '''

@app.route('/search')          
def v_search():
    if 'q' in request.args:
        ret = '<p>searching %s...</p><p> %s </p>' % (request.args['q'], request.args['page'])
    else:
        ret = 'what do you want to search?'
    return ret




# post方式提取数据是form字典方式
@app.route('/post')
def v_index_post():
    return  '''
        <form action="/login" method="POST">
            <input type="text" name="system" placeholder="input your system id"> <br />
            <input type="text" name="uid" placeholder="input your user id"> <br />
            <input type="password" name="pwd" placeholder="input your password"> <br />
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/login',methods=['POST'])
def v_login():
    uid = request.form['uid']
    pwd = request.form['pwd']
    system = request.form['system']
    if uid=='admin' and pwd=='admin' and system=='CRM':
        return 'Authorized successfully!'
    else:
        return 'your input is uid=%s,pwd=%s,system=%s' % (uid,pwd,system)

app.run(debug=True)
# app.run(host='0.0.0.0',port=8080)
