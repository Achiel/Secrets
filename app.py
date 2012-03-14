from flask import Flask, request, render_template
import redis
import random, string

url = "http://localhost:5000"
r = redis.Redis()
app = Flask(__name__)

random_char = lambda : random.choice(string.ascii_lowercase + string.digits)
random_string = lambda x : ''.join(random_char() for x in range(x))

@app.route("/index.html")
def index():
    return render_template('index.html')

@app.route("/create/", methods=['POST',])
def create():
    key = random_string(50)
    secret = request.form['secret']
    if not secret: 
        secret = random_string(20)
    r.set(key, secret)
    secret_url = "%s/get/%s" % (url, key)
    return render_template('created.tmpl', url=secret_url)

@app.route("/generate")
def generate():
    secret = random_string(20)
    key = random_string(50)
    r.set(key, secret)
    generated_url = "%s/get/%s" % (url, key)
    return render_template('generate.tmpl', generated=secret, url=generated_url)

@app.route("/get/<key>")
def retrieve(key=None):
    secret = r.get(key)
    r.delete(key)
    return render_template('get.tmpl', secret=secret)

if __name__ == "__main__":
    app.run()
