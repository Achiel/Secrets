# Secrets exchanger

Microsite to allow users to easily and securely send each other secrets over a possibly untrusted network. Fill in a secret (password, whatever) and hit generate. A random url is generated and provided to the user. Send this link to any other user (email, jabber) and tell them to click the link. The secret is only provided once. 

Although it doesn't prevent people from intercepting the secrets, the receiving party will be aware of the fact that the secret was intercepted and can act accordingly. 

Requirements
-------
 - Python 2.6 & up
 - Flask
 - Redis

Installation
-------
We recommend using virtualenv to install & run the app. 
    ~$ bin/pip install redis Flask

Running 
-------
    ~$ bin/python app.py


Todo
-------
 - installation instructions for running under nginx/fastcgi
 - config file for DTAP modes, urls
