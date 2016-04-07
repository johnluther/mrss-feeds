import feed
import data
import util
import json
from flask import Flask, Response, jsonify
from flask import render_template
from flask import request
from jinja2 import Template
from access import crossdomain
app = Flask(__name__)

def render(template='', context={}):
    t = Template(template)
    return t.render(**context)

def renderAll(templates={'head': '', 'body': '', 'foot': ''}, context={}):
    return render(templates.get('head'), context) \
            + render(templates.get('body'), context) \
            + render(templates.get('foot'), context)

def replaceInsert():
    hasOne = data.Template.objects.first()
    if not hasOne:
        hasOne = data.Template(head='', body='', foot='')
        hasOne.save()
    return hasOne

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/templates")
def templates():
    resp = {'templates': json.loads(data.Template.objects.only('body', 'foot', 'head').to_json())}
    return jsonify(**resp)

@app.route("/tool", methods=['GET', 'POST'])
def tool():    
    saveTemplate = replaceInsert()
    if request.method.lower() == 'post':        
        saveTemplate.head = request.form.get('head')
        saveTemplate.body = request.form.get('body')
        saveTemplate.foot = request.form.get('foot')
        saveTemplate.save()
    return render_template('tool/index.html', head=saveTemplate.head, foot=saveTemplate.foot, body=saveTemplate.body)

@crossdomain(origin='*')
@app.route('/dummy.rss')
def dummy():
    return Response(render_template('dummy.xml'), mimetype='application/rss+xml'), 200

# aovxTElR
@crossdomain(origin='*')
@app.route('/xml/<key>')
def xml(key=''):
    loadTemplate      = replaceInsert()
    feedJSON          = feed.fetchParse(key)
    feedJSON['first'] = feedJSON.get('items', [])[0]
    body              = "{% for item in items %}" + loadTemplate.body + "{% endfor %}"
    renderedXML       = renderAll({'head': loadTemplate.head, 'body': body, 'foot': loadTemplate.foot}, feedJSON)
    # util.string2s3(renderedXML, '%s.rss' % key)
    return Response(renderedXML, mimetype='text/xml'), 200

if __name__ == "__main__":
    app.debug = True
    app.run()

