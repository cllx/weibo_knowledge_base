from functools import wraps
from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_
from py2neo import Graph,Node,Relationship,cypher
from pandas import DataFrame
import random
import json
app = Flask(__name__)

def get_node_link(res):
    temp = res.iloc[:,:]
    for i in range(0,len(temp)):
        tmp = {}
        id_list = []
        for dic in node:
            id_list.append(dic['name'])
        if temp.iloc[i]['Person']['id'] not in id_list:
            tmp['name'] = temp.iloc[i]['Person']['id']
            tmp['label'] = temp.iloc[i]['Person']['name']
            tmp['category'] = random.randint(1,10)
            tmp['value'] = random.randint(1,3)
            node.append(tmp)
        tmp = {}
        if temp.iloc[i]['tail']['id'] not in id_list:
            tmp['name'] = temp.iloc[i]['tail']['id']
            tmp['label'] = temp.iloc[i]['tail']['name']
            tmp['category'] = random.randint(1,10)
            tmp['value'] = random.randint(1,3)
            node.append(tmp)
        rela = {}
        rela['source'] = temp.iloc[i]['Person']['id']
        rela['target'] = temp.iloc[i]['tail']['id']
        rela['label'] = temp.iloc[i]['r']['pro1']
        rela['value'] = random.randint(1,10)
        link.append(rela)
    node_link['node'] = node
    node_link['link'] = link

#@app.route('/')
#def hello_world():
#    return 'hello world'

@app.route('/')
def rejson():
    global node
    global link
    global node_link
    node = []
    link = []
    node_link = {}
    test_graph = Graph('http://localhost:7474',username='neo4j',password='8611662')
    res1 = test_graph.run("MATCH (Person {name:'杨小牛'})-[r]-(tail) with Person,r,tail return Person,r,tail").data()
    res1 = DataFrame(res1)
    res2 = test_graph.run("MATCH (Person {name:'邬贺铨'})-[r]-(tail) with Person,r,tail return Person,r,tail").data()
    res2 = DataFrame(res2)
    get_node_link(res1)
    get_node_link(res2)
    node_link = json.dumps(node_link,ensure_ascii=False,indent=4)
    return render_template('test2.html', yuanshi_info=node_link)

if __name__ == '__main__':
    app.run(debug = True)