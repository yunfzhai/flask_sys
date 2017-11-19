from qpython import qconnection as qc
import numpy as np
from flask import  render_template, make_response, jsonify,g,url_for,redirect,request,flash
from app import app


def connect_db():
    """Connects to the specific database."""
    q = qc.QConnection(host='localhost', port=8866)
    q.open()
    return q

def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    if not hasattr(g, 'q_db'):
        g.q_db = connect_db()
    return g.q_db

def fac_trace_table(range_a,checkdate_a,from_a,end_a,type_a):
    '''range 范围，checkdate查看日期 from开始日期 end结束日期 
    type指定多空组合，还是一定数目的多头 f4table f4tablefg f4tablefgg三种类型'''
    qcmd = type_a+'[`'+range_a+';'+checkdate_a+';'+from_a+';'+end_a+']'
    return qcmd

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'q_db'):
        g.q_db.close()
        print('q connection down!')

# def allow_cross_domain(fun):
#     @wraps(fun)
#     def wrapper_fun(*args, **kwargs):
#         rst = make_response(fun(*args, **kwargs))
#         rst.headers['Access-Control-Allow-Origin'] = '*'
#         rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
#         allow_headers = "Referer,Accept,Origin,User-Agent"
#         rst.headers['Access-Control-Allow-Headers'] = allow_headers
#         return rst
#     return wrapper_fun
@app.route('/')
def index():
    return redirect(url_for('datatest'))

@app.route('/update_table', methods=['POST'])
def update_table():
    # password = request.form.get('password')
    # username = request.args.get('username')
    type_a = request.form.get('type')
    rng = request.form.get('rng')
    cd_a = request.form.get('checkdate')
    fm_a = request.form.get('fmdate')
    ed_a = request.form.get('eddate')
    qcmd = fac_trace_table(rng,cd_a,fm_a,ed_a,type_a)
    flash(qcmd)
    q=get_db()
    t1=q.sync(qcmd,pandas=True)
    t1.fac=[str(x,encoding='utf-8') for x in t1.fac]
    t1.iloc[:,1:]=np.around(t1.iloc[:,1:],3)    
    t11 = [list(g) for g in t1.values]  #横着用
    data= { 'test':t11,'thefuck':'刚刚执行命令:'+qcmd}
    return jsonify(data)



@app.route('/wtf/wtf/dtest/wtf')
# @allow_cross_domain
# @cache.cached(timeout=2, key_prefix='random')
def datatest():
    q=get_db()
    t1=q.sync('f4table[`.zall;2017.12.31;2017.01.01;2017.12.31]',pandas=True)
    t1.fac=[str(x,encoding='utf-8') for x in t1.fac]
    t1.iloc[:,1:]=np.around(t1.iloc[:,1:],3)    
    t11 = [list(g) for g in t1.values]  #横着用

    t2= q.sync('update rate2:-1+prds 1+rate2 from lj[;1!select date,rate2:rate from .zall.fggBPO ] select date,rate:-1+prds 1+rate from .zall.fgBPO where date>=2017.01.01',numpy_temporals = True)
    data2={}
    data2['date'] = [''.join(x.astype(str).split("-")) for x in t2.date]
    data2['rate'] = list(np.around(t2.rate,3)) #竖着用
    data2['rate2'] = list(np.around(t2.rate2,3))

    data= { 'test':t11,'data2t':data2}
    return jsonify(data)

@app.route('/test/')
def test():
    return render_template('test.html',names=['因子名称','最近5日','d10','d20','d60','d120','d240','dfu'])

@app.route('/test2/')
def test2():
    return render_template('test_backup.html',names=['因子名称','最近5日','d10','d20','d60','d120','d240','dfu'])    