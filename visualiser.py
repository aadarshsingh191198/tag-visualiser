from flask import Flask
from flask import render_template, make_response
from markupsafe import Markup
# import pdfkit
import pandas as pd
app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')
app.jinja_env.filters['zip'] = zip

def get_markup(sent,tags):
    sent = sent.split()
    tags = tags.split()
    prev = None
    markup = ""
    for i in range(len(sent)):
        if tags[i] != prev:
            if prev and prev!='O': 
                markup+= "</mark>"
            if tags[i]!="O":
                markup += f' <mark data-entity="{tags[i]}">{sent[i]}'
            else:
                markup += f' {sent[i]}'
            prev = tags[i]
        elif tags[i] == prev:
            markup += f' {sent[i]}'
    if prev != "O": markup+= "</mark>"
    return markup.strip()

def bioless_tags(tags):
    return tags.replace("B-short","short").replace("I-short","short")\
        .replace("B-long","long").replace("I-long","long")

@app.route('/')
def visualise_route():
    # https://explosion.ai/blog/displacy-ent-named-entity-visualizer
    # https://codepen.io/explosion/pen/ALxpQO
    
    markup = []
    markup_gold = []

    data = pd.read_csv("demo_data/analysis_data.csv")
    
    for i in range(data.shape[0]):
        gold_tags = data["labels"][i]
        tags = data['predictions'][i]
        sent = data['tokens'][i]
        gold_tags = bioless_tags(gold_tags)
        tags = bioless_tags(tags)
        markup.append(Markup(get_markup(sent,tags)))
        markup_gold.append(Markup(get_markup(sent,gold_tags)))

    html = render_template('visualise.html', markup =markup, markup_gold = markup_gold)

    return html


## To run on windows
# set FLASK_APP=visualiser.py
# python -m flask run or flask run
# export FLASK_DEBUG=1 or app.run(debug=True) for Hot reload
