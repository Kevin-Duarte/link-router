import email
from global_config import *
api_admin = Blueprint('api_admin', __name__)

# Admin - Update Admin Rights
@api_admin.route('/admin/update_admin_rights', methods=['PATCH'])
@admin_required
def admin_update_admin_rights():
    userId = int(request.args.get('id'))
    admin = (request.args.get('admin') == '1')
    result = database.setUserAdminRights(userId, admin)
    database.addEvent('ADMIN_UPDATE_ADMIN_RIGHTS', getIPAddr(), current_user.get_id(), json.dumps([x for x in result]))
    return jsonify(message='Admin rights updated'), 200

# Admin - Disable User 
@api_admin.route('/admin/update_disable_user', methods=['PATCH'])
@admin_required
def admin_update_disable_user():
    userId = int(request.args.get('id'))
    disable = (request.args.get('disable') == '1')
    result = database.setUserAccountDisable(userId, disable)
    database.addEvent('ADMIN_UPDATE_DISABLE_USER', getIPAddr(), current_user.get_id(), json.dumps([x for x in result]))
    return jsonify(message='Account Disabled status updated'), 200


# Admin - Get all links
@api_admin.route('/admin/get_links', methods=['GET'])
@admin_required
def admin_get_links():
    data = database.getAllLinks()
    database.addEvent('ADMIN_GET_LINKS', getIPAddr(), current_user.get_id(), "All links")
    converted = json.dumps([dict(ix) for ix in data])
    return converted, 200 

# Admin - Delete link
@api_admin.route('/admin/delete_link', methods=['DELETE'])
@admin_required
def admin_delete_link():
    deleteId = int(request.args.get('id'))
    result = database.deleteLink(deleteId)
    database.addEvent('ADMIN_DELETE_LINK', getIPAddr(), current_user.get_id(), json.dumps([x for x in result]))
    return jsonify(id=deleteId), 200   

# Admin - get users
@api_admin.route('/admin/get_users', methods=['GET'])
@admin_required
def admin_get_users():
    database.addEvent('ADMIN_GET_USERS', getIPAddr(), current_user.get_id(), "All users")
    data = database.getAllUsersNoPass()
    return json.dumps([dict(ix) for ix in data]), 200

# Admin - delete user
@api_admin.route('/admin/delete_user', methods=['DELETE'])
@admin_required
def admin_delete_user():
    id = int(request.args.get('id'))
    user = database.getUserNoPass(id)
    database.addEvent('ADMIN_DELETE_USER', getIPAddr(), current_user.get_id(), json.dumps([x for x in user]))
    database.deleteUser(id)
    return jsonify(message=id), 200

# Admin - get banned
@api_admin.route('/admin/get_banned', methods=['GET'])
@admin_required
def admin_get_banned():
    database.addEvent('ADMIN_GET_BANNED', getIPAddr(), current_user.get_id(), "All banned")
    data = database.getBannedList()
    return json.dumps([dict(ix) for ix in data]), 200

# Admin - delete ban
@api_admin.route('/admin/delete_ban', methods=['DELETE'])
@admin_required
def admin_delete_ban():
    id = int(request.args.get('id'))
    ban = database.getBanFromId(id)
    database.addEvent('ADMIN_DELETE_BAN', getIPAddr(), current_user.get_id(), json.dumps([x for x in ban]))
    database.deleteBan(id)
    return jsonify(message=id), 200

# Admin - add ban
@api_admin.route('/admin/add_ban', methods=['POST'])
@admin_required
def admin_add_ban():
    ipaddr = html.escape(request.form['ipaddr'])
    reason = html.escape(request.form['reason'])
    result = database.addBan(ipaddr, reason)
    database.addEvent('ADMIN_ADD_BAN', getIPAddr(), current_user.get_id(), json.dumps([x for x in result]))
    return jsonify(ipaddr=ipaddr, reason=reason), 200

def requestArgWithDefault(variable, default):
    variable = html.escape(variable)
    return request.args.get(variable) or default

# Admin - get events
@api_admin.route('/admin/get_events', methods=['GET'])
@admin_required
def admin_get_events():
    ipaddr = requestArgWithDefault('ipaddr', '%')
    type = requestArgWithDefault('type', '%')
    description = requestArgWithDefault('description', '%')
    email = requestArgWithDefault('email', '%')
    startDate = requestArgWithDefault('startDate', '%')
    endDate = requestArgWithDefault('endDate', '%')
    limit = requestArgWithDefault('limit', '%')
    result = database.getEvents(
        ipaddr=ipaddr,
        type=type,
        description=description,
        email=email,
        startDate=startDate,
        endDate=endDate,
        limit=limit
    )

    #print(str([ipaddr, type, description, user, startDate, endDate, limit]), file=sys.stdout)
    database.addEvent('ADMIN_GET_EVENTS', getIPAddr(), current_user.get_id(), str([ipaddr, type, description, email, startDate, endDate, limit]))
    return json.dumps([dict(ix) for ix in result]), 200