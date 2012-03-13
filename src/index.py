from flask import Flask, request
app = Flask(__name__)
import redis
import random, string

r = redis.Redis()
r.set('foo', 'bar')

random_char = lambda : random.choice(string.ascii_uppercase + string.digits)
@app.route("/create/", methods=['POST',])
def create():
    secret = request.form['secret']
    if not secret: 
        secret = ''.join(random_char() for x in range(20))
    return "hello world: %s" % secret

if __name__ == "__main__":
    app.run()
