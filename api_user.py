from global_config import *
import html
api_user = Blueprint('api_user', __name__)

# User - Logout
@api_user.route("/user/logout")
@login_required
def user_logout():
    database.addEvent('USER_LOGOUT', getIPAddr(), current_user.get_id(), "Logout" )
    current_user.authenticated = False
    logout_user()
    cookieInject = make_response(jsonify(message='Successfully logged out'))
    cookieInject.delete_cookie('loggedIn')
    cookieInject.delete_cookie('admin')
    return cookieInject, 200

# User - Get Links
@api_user.route('/user/links', methods=['GET'])
@login_required
def user_get_links():
    database.addEvent('USER_GET_LINKS', getIPAddr(), current_user.get_id(), "Current user links" )
    data = database.getLinksByUserId(current_user.get_id())
    converted = json.dumps([dict(ix) for ix in data])
    return converted, 200

# User - Add link
@api_user.route('/user/add_link', methods=['POST'])
@limiter.limit("5 per minute")
@login_required
def user_add_Link():
    key = request.args.get('key')
    link = request.args.get('url')
    result = validateAndAddLink(key, link,current_user.get_id(), 30)
    database.addEvent('USER_ADD_LINK', getIPAddr(), current_user.get_id(), json.dumps([x for x in result]))
    return jsonify(key=key, link=link), 200

# User - renew link
@api_user.route('/user/renew_link', methods=['POST'])
@login_required
def user_renew_link():
    renewId = int(request.args.get('id'))
    
    data = database.getLinksByUserId(current_user.get_id())
    allowedUserLinkIDs = [ x['id'] for x in data]
    if renewId not in allowedUserLinkIDs:
        raise Exception("User does not own the link")
    result = database.renewLinkExpiration(renewId, 30)
    database.addEvent('USER_RENEW_LINK', getIPAddr(), current_user.get_id(), json.dumps([x for x in result]))
    return jsonify(id=renewId), 200


# User - Delete Link
@api_user.route('/user/delete_link', methods=['DELETE'])
@login_required
def user_delete_link():
    deleteId = int(request.args.get('id'))
    data = database.getLinksByUserId(current_user.get_id())
    allowedUserLinkIDs = [ x['id'] for x in data]
    if deleteId not in allowedUserLinkIDs:
        raise Exception("User does not own the link")
    result = database.deleteLink(deleteId)
    database.addEvent('USER_DELETE_LINK', getIPAddr(), current_user.get_id(), json.dumps([x for x in result]))
    return jsonify(id=deleteId), 200

# User - Get info
@api_user.route('/user/account_info', methods=['GET'])
@login_required
def user_account_info():
    data = database.getUserNoPass(current_user.get_id())
    converted = json.dumps([x for x in data])
    database.addEvent('USER_ACCOUNT_INFO', getIPAddr(), current_user.get_id(), converted)
    return converted, 200