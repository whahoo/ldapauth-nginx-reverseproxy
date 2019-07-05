from flask import Flask, abort, request, jsonify
import ldap
from lxml import etree
import io

app = Flask(__name__)

bind_dn = 'cn={},dc={},dc={}'.format( 'admin', 'example', 'org')
bind_password = 'admin'
base_dn = 'dc={},dc={}'.format( 'example', 'org')

ldap_obj = ldap.initialize('ldap://localhost:8389');
ldap_obj.protocol_version = ldap.VERSION3
ldap_obj.bind_s( bind_dn, bind_password, ldap.AUTH_SIMPLE );

def ldap_auth( username, password, group, ldap_obj ):

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

@app.route("/auth_proxy/<group>", methods=['POST'])
def auth(group):
    print('auth', request)
    xml = request.get_data(as_text=True)
    credentials = parse_soap(xml)
    print( request.headers )
    ldap_connection = {
            'uri':  request.headers['X-Ldap-Uri'],
            'bind_dn' : request.headers['X-LDAP-BIND-DN'],
            'bind_pw' : request.headers['X-LDAP-BIND-PW']
            }
    ldap_auth(credentials['username'], credentials['password'], group, ldap_obj)


    return '', 200

@app.route("/")
def index():
    return 'you are authorised to visit this page'

@app.route("/xml", methods=[ 'POST'])
def receive_xml():
    credentials = parse_soap(request.data)
    return jsonify(credentials), 200

def parse_soap(xml):
    print('start xml')
    tree = etree.fromstring(xml)
    user_name = tree.xpath('/SE:Envelope/SE:Header/wsse:Security/wsse:UsernameToken/wsse:Username',
            namespaces={'SE':'http://www.w3.org/2003/05/soap-envelope',
                      'wsse':'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd'}
            )
    password = tree.xpath('/SE:Envelope/SE:Header/wsse:Security/wsse:UsernameToken/wsse:Password',
               namespaces={'SE':'http://www.w3.org/2003/05/soap-envelope',
                         'wsse':'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd'}
                                        )
    user_name_string =  user_name[0].text
    password_string = password[0].text
    print ('xml')
    return {
            'username': user_name_string,
            'password': password_string
            }

