# coding: utf-8
# datatest.py
from flask import Blueprint,render_template,request,jsonify
import json

datatest = Blueprint('datatest',__name__)

@datatest.route('/')
def index():
    return render_template('data_index.html')


@datatest.route('/mystring')
def mystring():
    return 'my string'


# @datatest.route('/dataFromAjax')
# def dataFromAjax():
#     test = request.args.get('mydata')
#     print(test)
#     return 'dataFromAjax'


# @datatest.route('/mydict', methods=['GET', 'POST'])
# def mydict():
#     print('post')
#     if request.method == 'POST':
#         a = request.form['mydata']
#         print(a)
#     d = {'name': 'xmr', 'age': 18}
#     return jsonify(d)


# @datatest.route('/name', methods=['POST'])
# def getname():
#     firstname = request.form['firstname']
#     lastname = request.form['lastname']
#     d = {'name': firstname + ' ' + lastname, 'age': 18}
#     print(d)
#     return jsonify(d)


# @datatest.route('/myform', methods=['POST'])
# def myform():
#     print('post')
#     a = request.form['FirstName']
#     print(a)
#     d = {'name': 'xmr', 'age': 18}
#     return jsonify(d)


# @datatest.route('/mylist')
# def mylist():
#     l = ['xmr', 18]
#     print('mylist')
#     return json.dumps(l)  # 用jsonify前端会出错


# @datatest.route('/mytable')
# def mytable():
#     table = [('id', 'name', 'age', 'score'),
#         ('1', 'xiemanrui', '18', '100'),
#         ('2', 'yxx', '18', '100'),
#         ('3', 'yaoming', '37', '88')]

#     print('mytable')
#     data = json.dumps(table)
#     print(data)
#     return data
