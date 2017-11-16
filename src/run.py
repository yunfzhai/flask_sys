# -*- coding:utf-8 -*-  
# example for data transform
from flask import Flask, render_template, session, redirect, url_for, flash,request
from flask import jsonify
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
# from werkzeug.serving import run_with_reloader
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = "dfdfdffdad"

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

g=[]

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    g.append(1)
    print g
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    g.append(1)
    print g
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))

from datatest import datatest
app.register_blueprint(datatest,url_prefix='/test')

if __name__ == '__main__':
    manager.run()
