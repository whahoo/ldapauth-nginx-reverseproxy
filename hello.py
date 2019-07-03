from flask import Flask, abort, request
import ldap

app = Flask(__name__)

bind_dn = 'cn={},dc={},dc={}'.format( 'admin', 'example', 'org')
bind_password = 'admin'
base_dn = 'dc={},dc={}'.format( 'example', 'org')

def ldap_auth( username, password, group, ldap_connection ):
    ldap_obj = ldap.initialize(ldap_connection['uri'])
    ldap_obj.protocol_version = ldap.VERSION3

    ldap_obj.bind_s( ldap_connection['bind_dn'], ldap_connection['bind_pw'], ldap.AUTH_SIMPLE )

    search_filter = '(cn={})'.format( username )

    results = ldap_obj.search_s( base_dn, ldap.SCOPE_SUBTREE, search_filter )

    if len(results) < 1:
        abort(401)

    try:
        ldap_obj.bind_s( 'cn={},dc={},dc={}'.format(username, 'example', 'org'), password, ldap.AUTH_SIMPLE)
    except:
        abort(401)

    return

@app.errorhandler(404)
def page_not_found(error):
        print( request.url );
        return 'This route does not exist {}'.format(request.url), 404

@app.route("/auth_proxy/<group>")
def auth(group):
    print( request.headers )
    ldap_connection = {
            'uri':  request.headers['X-Ldap-Uri'],
            'bind_dn' : request.headers['X-LDAP-BIND-DN'],
            'bind_pw' : request.headers['X-LDAP-BIND-PW']
            }
    ldap_auth('admin','admin',group, ldap_connection)


    return '', 200
