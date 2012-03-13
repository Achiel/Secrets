from flask import Flask, request
app = Flask(__name__)
import redis
import random, string

url = "http://localhost:5000"
r = redis.Redis()

random_char = lambda : random.choice(string.ascii_uppercase + string.digits)
random_string = lambda x : ''.join(random_char() for x in range(x))

@app.route("/create/", methods=['POST',])
def create():
    key = random_string(50)
    secret = request.form['secret']
    if not secret: 
        secret = random_string(20)
    r.set(key, secret)
    return "your secret is stored at %s/get/%s" % (url, key)

@app.route("/get/<key>")
def retrieve(key=None):
    if not key or not r.get(key):
        return "key not found"
    
    val = r.get(key)
    r.delete(key)
    return "the following secret was retrieved: <br/> %s <br/> \
            Please note that you will only be able to retrieve this secret once" \
            % val

if __name__ == "__main__":
    app.run()
