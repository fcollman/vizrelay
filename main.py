#!/usr/bin/env python3

import json
import pprint
import settings

from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def main():
    mod = settings.get_settings(request.args)
    result =  "<html><head></head><body>"
    result += "<h2>Current settings</h2>"
    result += "<pre>" + pprint.PrettyPrinter(indent=4).pformat(mod.args) +"</pre>"
    result += "</body>"
    return json.dumps(mod.args)

# Sample URL http://ibs-forrestc-ux1:8002/render/ibs-forrestc-ux1.corp.alleninstitute.org/Forrest/H16_03_005_HSV_HEF1AG65_R2An15dTom/ACQGephyrin/
@app.route("/render/<server>/<owner>/<project>/<stack>/", defaults={'channel' : None})
@app.route("/render/<server>/<owner>/<project>/<stack>/<channel>/")
def render(server, owner, project, stack, channel):
    mod = settings.get_settings(request.args)
    ngmod = mod.args['neuroglancer']

    render_params = [owner, project, stack]
    if channel:
        render_params.append(channel)
        
    protocol = "http"
    render_source = "render://{0}://{1}/{2}".format(protocol, server, '/'.join(render_params))

    layer = {'type': 'image', 'source': render_source}
    layer_parents =  {stack : layer}
    params = {}
    params['layers'] = layer_parents
    params['blend'] = ngmod['blend']

    new_url = "{0}/#!{1}".format(ngmod['base_url'], json.dumps(params, separators=(',', ':'))).replace('"',"'")

    return '<a href="{0}">{0}</a>'.format(new_url)

if __name__ == "__main__":
    app.run(host='0.0.0.0')