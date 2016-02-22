from app import app
from app.api import api
from app.api.wrappers import Manager
from flask import jsonify, request
from app.api import tools


manage = Manager()  # App Manager


@api.route('/organization/', methods=['GET'])
def get_org_data():
    org_domain = request.args.get('org_domain', None)
    response = manage.organization.get_org(org_domain)
    return jsonify(data=response)


@api.route('/organization/', methods=['POST'])
def post_org():
    response = manage.organization.post_org(request)
    return jsonify(data=response)


@api.route('/organization/', methods=['PUT'])
def update_org():
    response = manage.organization.update_org(request)
    return jsonify(data=response)


@api.route('/organization/', methods=['DELETE'])
def delete_org():
    response = manage.organization.delete_org(request)
    return jsonify(data=response)


@api.route('/organization/settings/', methods=['GET'])
def get_setting():
    response = manage.settings.get_setting(request)
    return jsonify(data=response)


@api.route('/organization/settings/', methods=['POST'])
def post_setting():
    response = manage.settings.post_setting(request)
    return jsonify(data=response)


@api.route('/organization/settings/', methods=['PUT'])
def update_setting():
    response = manage.settings.update_setting(request)
    return jsonify(data=response)


@api.route('/organization/settings/', methods=['DELETE'])
def delete_setting():
    response = manage.settings.delete_setting(request)
    return jsonify(data=response)


@api.route('/queues/', methods=['GET'])
def get_queue():
    org_domain = request.args.get('org_domain')
    queue_id = request.args.get('queue_id')
    if not queue_id:
        response = manage.queue.get_queues(org_domain)
        return jsonify(data=response)
    else:
        response = manage.queue.get_queue(org_domain, queue_id)
        return jsonify(data=response)


@api.route('/queues/', methods=['POST'])
def post_queue():
    response = manage.queue.post_queue(request)
    return jsonify(data=response)


@api.route('/queues/', methods=['PUT'])
def update_queue():
    response = manage.queue.update_queue(request)
    return jsonify(data=response)


@api.route('/queues/', methods=['DELETE'])
def delete_queue():
    response = manage.queue.delete_queue(request)
    return jsonify(data=response)


@api.route('/queues/users/', methods=['POST'])
def enqueue_user():
    phone_number = request.form.get('phone_number')
    queue_id = request.form.get('queue_id')
    response = manage.queue.enqueue(str(phone_number), queue_id)
    return jsonify(data=response)


@api.route('/queues/users/', methods=['PUT'])
def dequeue_user():
    phone_number = request.form.get('phone_number')
    queue_id = request.form.get('queue_id')
    response = manage.queue.dequeue(phone_number, queue_id)
    return jsonify(data=response)


@api.route('/queue_groups/', methods=['GET'])
def get_groups():
    group_id = request.args.get('group_id')
    if not group_id:
        response = manage.group.get_groups(request)
        return jsonify(data=response)
    else:
        response = manage.group.get_group(request)
        return jsonify(data=response)


@api.route('/queue_groups/', methods=['POST'])
def post_group():
    response = manage.group.post_group(request)
    return jsonify(data=response)


@api.route('/queue_groups/', methods=['PUT'])
def update_group():
    response = manage.group.update_group(request)
    return jsonify(data=response)


@api.route('/queue_groups/', methods=['DELETE'])
def delete_group():
    response = manage.group.delete_group(request)
    return jsonify(data=response)


@api.route('/notify/', methods=['GET'])
def notofy_queue():
    queue_id = request.args.get('queue_id')
    response = tools.notify_queue_position(queue_id)
    return jsonify(data=response)

@api.route('/get_average_wait_time/', methods=['GET'])
def get_average_wait_time():
    queue_id = request.args.get('queue_id')
    response = tools.get_average_wait_time(queue_id)
    return jsonify(data=response)


@app.errorhandler(404)
def page_404(e):
    response = dict(status='FAIL', message='Sorry. We could not find what you are looking for', error=str(e))
    return jsonify(data=response)


@app.errorhandler(500)
def page_500(e):
    response = dict(status='FAIL', message='Oops... something went horribly wrong', error=str(e))
    return jsonify(data=response)
