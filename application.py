from flask import Flask, Response, render_template, request
import json

app = Flask(__name__)

import wtforms as wt
from wtforms import TextField, Form

NAMES=["abc","abcd","abcde","abcdef"]

class SearchForm(Form):
    autocomp= TextField('autocomp',id='autocomplete')

@app.route('/autocomplete',methods=['GET'])
def autocomplete():
    search = request.args.get('term')

    app.logger.debug(search)
    return Response(json.dumps(NAMES), mimetype='application/json')

@app.route('/',methods=['GET','POST'])
def index():
    form = SearchForm(request.form)
    return render_template("search.html",form=form)

if __name__ == '__main__':
    app.run(debug=True)