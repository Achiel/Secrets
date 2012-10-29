# Secrets exchanger

Microsite to allow users to easily and securely send each other secrets over a possibly untrusted network. Fill in a secret (password, whatever) and hit generate. A random url is generated and provided to the user. Send this link to any other user (email, jabber) and tell them to click the link. The secret is only provided once. 

Although it doesn't prevent people from intercepting the secrets, the receiving party will be aware of the fact that the secret was intercepted and can act accordingly. 

Requirements
-------
 - Python 2.6 & up
 - Flask
 - Redis
 - flup (only if you do fastcgi)

Installation
-------
We recommend using virtualenv to install & run the app. 
    ~$ bin/pip install redis Flask

Running 
-------
    ~$ bin/python app.py

Deployment
-------

Supervisor, fastCGI with Nginx:

Tell `flup` to bind to TCP localhost:3000 in `secrets.fcgi`:
    WSGIServer(app, bindAddress=('127.0.0.1',3000)).run()

Setup a supervisor config. e.g. `/etc/supervisor/conf.d/secrets.conf`:
    [program:secrets]
    user=secretst
    command=/srv/www/secrets.example.org/venv/bin/python src/secrets.fcgi
    stdout_logfile=/var/log/supervisor/secret/out.log
    stderr_logfile=/var/log/supervisor/secret/error.log
    directory=/srv/www/secrets.example.org/
    stopsignal=KILL
    umask=022

Nginx site config e.g. `/etc/nginx/conf.d/secrets.conf`:
    server {
        listen [::]:80;
        server_name secrets.example.org;

        location / {
            rewrite "^/index.html$" /static/index.html last;
            include fastcgi_params;
            fastcgi_split_path_info ^(/)(.*)$;
            fastcgi_param PATH_INFO $fastcgi_path_info;
            fastcgi_param SCRIPT_NAME $fastcgi_script_name;
            fastcgi_pass localhost:3002;
        }
    }

You can also stick with file socket instead of TCP. It is also recommended to set password for redis-server.

Todo
-------
 - config file for DTAP modes, urls
