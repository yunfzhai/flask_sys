from flask import Flask
from flask_cache import Cache

app = Flask(__name__)
app.config['SECRET_KEY']='!@$RFGAVASDGAQQQ'
cache = Cache(app,config={'CACHE_TYPE': 'simple'})

from app import views