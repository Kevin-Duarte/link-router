from turtle import reset
from unittest import result
from global_config import *
import html
api_anon = Blueprint('api_anon', __name__)

# Anon - Sign up
@api_anon.route('/anon/signup', methods=['POST'])
@limiter.limit("6 per hour")
def anon_signup():
    email = request.form['email'].lower()
    firstname = request.form['firstname']
    lastname = request.form['lastname']


    if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
        raise Exception('Invalid email format')
    elif not re.fullmatch(r'^[A-Za-z]{1,20}$', firstname) or not re.fullmatch(r'^[A-Za-z]{1,20}$', lastname):
        raise Exception('Name can only be letters')
    elif database.existsUserEmail(email):
        raise Exception('Email already exists')
    
    addResult = database.addUser(email, None, firstname, lastname)
    userResult = database.setUserPassReset(addResult['id'], 1) 
    database.addEvent('ANON_SIGNUP', getIPAddr(), -1,  json.dumps([x for x in userResult]))
    smtp.send(email, 'Activate Your Account', 'Thank you for signing up. Click on this link to activate your account: http://' + HOST_BASE +'/set_password?key=' + str(userResult['resetKey']))
    return jsonify(message='Sign up successful'), 200


# Anon - Authenticate
@api_anon.route("/anon/auth", methods=['POST'])
@limiter.limit("1 per second")
def anon_auth():

    email = html.escape(request.form['email'])
    password = request.form['password']
    remember = 'remember' in request.form

    if int(BAN_FAIL_AUTH) <= database.checkAuthFailsToday(getIPAddr()):
        banResult = database.addBan(getIPAddr(), 'SYSTEM BANNED: Auth abuse')
        database.addEvent('SYSTEM_BANNED', getIPAddr(), '-1', json.dumps([x for x in banResult]))

 
    if current_user.is_authenticated:
        raise Exception("User already logged in")

    if (database.existsUserEmail(email) == False):
        raise Exception('Bad email/password combination (' + email + ')')

    userId = database.getIdByEmail(email)
    userData = load_user(userId)
    if hashlib.sha256(password.encode()).hexdigest() != userData.password:
        raise Exception('Bad email/password combination (' + email + ')')
    
    if userData.accountActive == False:
        raise Exception("Your account must be activated before logging in (" + email + ")")
    
    if userData.disabled == True:
        raise Exception("Your account has been disabled (" + email + ")")

    login_user(userData, remember=remember)
    result = database.setLastLogin(userId, datetime.now())
    database.addEvent('ANON_AUTH', getIPAddr(), -1, json.dumps([x for x in result]))
    cookieInject = make_response(jsonify(message='Successful login'))
    cookieInject.set_cookie('loggedIn', '1')

    isAdmin = '0'
    if userData.admin == True:
        isAdmin = '1'
    cookieInject.set_cookie('admin', isAdmin)
    return cookieInject, 200


# Anon - Add link
@api_anon.route('/anon/add_link', methods=['POST'])
@limiter.limit("5 per minute")
def anon_addLink():
    key = request.args.get('key')
    link = request.args.get('url')
    result = validateAndAddLink(key, link, -1, 7)
    database.addEvent('ANON_ADD_LINK', getIPAddr(), -1, json.dumps([x for x in result]))
    return jsonify(key=key, link=link), 200

# Anon - Password reset request
@api_anon.route('/anon/password_reset_request', methods=['POST'])
@limiter.limit("6 per hour")
def anon_password_reset_request():
    email = html.escape(request.form['email'])
    database.addEvent('ANON_PASSWORD_RESET_REQUEST', getIPAddr(), -1, str(email) )
    if database.existsUserEmail(email):
        id = database.getIdByEmail(email)
        lastResetRequest = database.getUserLastResetRequest(id)
        if lastResetRequest == None or datetime.fromisoformat(lastResetRequest) < datetime.now() + timedelta(minutes=-5):
            database.setUserLastResetRequest(id, datetime.now())
            key = database.setUserPassReset(id, 1)['resetKey']
            smtp.send(email, 'Password Reset Request', 'Click here to reset your password: http://' + HOST_BASE +'/set_password?key=' + str(key))
    return jsonify(message='Password reset has been sent')

# Anon - Password reset update
@api_anon.route('/anon/password_reset_update', methods=['POST'])
@limiter.limit("1 per second")
def anon_password_reset_update():
    resetKey = html.escape(request.args.get('key'))
    password = request.form['password']
    
    if database.existsUserResetKey(resetKey) == False:
        raise Exception("Key does not exist")
    
    id = database.getIdByResetKey(resetKey)
    validateAndSetPassword(id, password)
    database.deleteUserPassReset(id)
    result = database.setUserAccountActive(id, 1)
    database.addEvent('ANON_PASSWORD_RESET_UPDATE', getIPAddr(), -1, json.dumps([x for x in result]))
    return jsonify(message='Password has been updated')
