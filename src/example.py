from flask import Flask, render_template, make_response, jsonify,g,url_for
from functools import wraps
from flask_cache import Cache
from qpython import qconnection as qc

app=Flask(__name__)


# app configuration
app.config['SECRET_KEY']='!@$RFGAVASDGAQQQ'
cache = Cache(app,config={'CACHE_TYPE': 'simple'})

# connection_string = u'mssql+pymssql://sa:yslstryhhh@sql2k8cluster\mssql2k8/factormodel'
# engine = sqlalchemy.create_engine(connection_string)

def connect_db():
    """Connects to the specific database."""
    # q = qc.QConnection(host='10.0.16.106', port=8866, pandas=True)
    q = qc.QConnection(host='10.0.16.106', port=8866)
    q.open()
    return q

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'q_db'):
        g.q_db = connect_db()
    return g.q_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'q_db'):
        g.q_db.close()
        print('q connection down!')




def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun

@app.route('/wtf/wtf/dtest/wtf')
@allow_cross_domain
@cache.cached(timeout=2, key_prefix='random')
def datatest():
    q=get_db()
    zdata=q.sync('0!rand[.1]+1!select  from f4table[`.zall;2017.12.31;2017.01.01;2017.12.31]')
    zdata2= [list(g) for g in zdata]
    for m in zdata2:
        m[0] = str(m[0],encoding="utf-8")

    pldata= q.sync('100#update rate2:-1+prds 1+rate2 from lj[;1!select date,rate2:rate from .zall.fggBPO ] select date,rate:-1+prds 1+rate from .zall.fgBPO where date>=2017.01.01',numpy_temporals = True)
    pldata2 = [list(g) for g in pldata]
    for m in pldata2:
        m[0] = ''.join(m[0].astype(str).split("-"))

    data= { 'test':zdata2, 'data2':pldata2 }
    return jsonify(data)

@app.route('/test/')
def test():
    return render_template('test.html',names=['因子名称','最近5日','d10','d20','d60','d120','d240','dfu'])

if __name__ == '__main__':
    app.run(debug=True)