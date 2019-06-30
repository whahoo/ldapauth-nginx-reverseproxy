# Ldap Authentication reverse proxy

This project sets up a very targeted LDAP authentication endpoint integrated to nginx


# Setup for Development

Work in progress : This can be improved
## Dependencis

 * nginx
 * python3
 * Docker

## Running everything
```
# Run Mock LDAP server
docker run -d --rm --name ldap -p 8389:389 -p 8636:636 osixia/openldap

# install python dependencies
virtualenv .venv 
pip install -r requirements.txt

# Start Nginx with this sample config
nginx -c ${PWD}/nginx.conf

# Start the uwsgi server
uwsgi --ini wsgi.ini
```

## Send through a test request 

nginx is listening on 8080

`curl localhost:8080`

irequest invokes auth_request in nginx, which makes a socket call to uwsgi server which connects to OpenLdap running in docker on port 8389

*currently lots of hardcoded values* needing to be parameterised






