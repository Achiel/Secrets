from flask import Flask, request, render_template, redirect, escape
import redis
import random
import string
import os
import types

host = "https://secrets-accp.mendix.com"
r = redis.Redis()
app = Flask(__name__)

random_char = lambda: random.choice(string.ascii_lowercase + string.digits)
random_string = lambda x: ''.join(random_char() for x in range(x))

redirect_urls = {'/': '/index.html'}
for (dirpath, dirname, filenames) in os.walk('static'):
    for f in filenames:
        file_url = os.path.join(dirpath, f)
        redirect_urls[file_url[6:]] = '/%s' % file_url


def redirect_url():
    return redirect(redirect_urls[request.path], 301)

for url in redirect_urls:
    app.add_url_rule(url, url, redirect_url)


@app.route("/create/", methods=['POST'])
def create():
    key = random_string(50)
    secret = request.form['secret']
    if not secret:
        secret = random_string(20)
        generated = True
    else:
        generated = False
    while not r.setnx(key, secret):
        key = random_string(redis_key_length)
    secret_url = "%s/get/%s" % (host, key)

    if generated:
        return render_template('generate.tmpl', generated=secret,
                               url=secret_url)

    return render_template('created.tmpl', url=secret_url)


@app.route("/generate")
def generate():
    secret = random_string(20)
    key = random_string(50)
    r.set(key, secret)
    generated_url = "%s/get/%s" % (host, key)
    return render_template('generate.tmpl', generated=secret,
                           url=generated_url)


@app.route("/get/<key>")
def retrieve(key=None):
    secret = r.get(key)
    r.delete(key)
    if type(secret) != types.NoneType:
        secret = escape(secret)
    return render_template('get.tmpl', secret=secret)

if __name__ == "__main__":
    app.run()
