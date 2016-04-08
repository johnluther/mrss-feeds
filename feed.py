from flask import render_template
import requests
import datetime

baseUrl = 'http://content.jwplatform.com/feeds/%s.json'

def get(key=''):
	r = requests.get(baseUrl % key)
	if r.status_code == 200:
		return r.json()
	else:
		raise Exception('Unable to fetch resource')

def parse(json={}):
	clean = {}
	items = []
	for i in json.get('playlist', []):
		best = {'width': 0, 'url': '', 'duration': 0}
		pubdate = datetime.datetime.fromtimestamp(i.get('pubdate'))
		for s in i.get('sources', []):
			if s.get('width') > best.get('width'):
				best['url']      = s.get('file')
				best['width']    = s.get('width')
				best['duration'] = s.get('duration')
		items.append({ 
			'key'  : i.get('mediaid'),
			'title': i.get('title'),
			'description': i.get('description'),
			'date' : i.get('pubdate'),
			'date_utc': pubdate.strftime('%Y-%m-%d %H:%M:%S'),
			'date_rss': pubdate.strftime("%a, %d %b %Y %H:%M:%S %z"),
			'mediaurl': best.get('url'),
			'duration': best.get('duration'),
			'image': i.get('image'),
			'link': i.get('link'),
			'tags': i.get('tags', ''),
			'custom': i.get('custom', {}),
		})
	clean['items'] = items
	return clean

def toXML(json={}, template_name='roku_template.xml'):
	try:
		rendered = render_template(template_name, name='Cooper', items=json.get('items'))
	except:
		raise
		exit()
		raise Exception('Unable to render: %s' % template_name)
	else:
		return rendered

def fetchParse(key=''):
	try:
		data = get(key)
		parsed = parse(data)
	except:
		raise Exception('Unable to fetch and parse feed')
	else:
		return parsed

def load(key=''):
	try:
		data = get(key)
		parsed = parse(data)
	except:
		raise Exception('Unable to fetch and parse feed')
	else:
		rendered = toXML(parsed)
		return rendered