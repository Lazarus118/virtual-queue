from app import db
from app.models import Organization, Queue, QueueData
from app.api import tools
from app.api.lib import Notify
from datetime import datetime

notify = Notify(account_sid='123', auth_token='123', phone_number='123')


class QueueManager(object):
    """
    This section tries to document the methods and their respective arguments that belong to this object.
    :arg queue_id: integer - integer representation of the queue's ID in the database\
    :arg phone_number: string - string representation of a phone number
    :arg org_domain: string - string representation of an organization's domain name

    """

    def __init__(self):
        pass

    @staticmethod
    def post_queue(request):
        try:
            org_domain = request.form['org_domain']
            organization = Organization.query.filter_by(org_domain=org_domain).first()

            if not organization:
                return dict(
                    status='FAIL',
                    message='No such organization',
                    error='Invalid number format',
                    request_args=request.form
                )

            queue_name = request.form['queue_name']
            queue_org_id = organization.org_id
            queue_group_id = request.form['queue_group_id']
            queue = Queue(
                queue_name=queue_name,
                queue_org_id=queue_org_id,
                queue_group_id=queue_group_id
            )
            db.session.add(queue)
            db.session.commit()

            return dict(
                status='OK',
                message='Queue created successfully.',
                error=None
            )
        except Exception as e:
                return dict(
                    status='FAIL',
                    message='Could not create that queue.',
                    error=str(e), request_args=request.form
                )

    @staticmethod
    def update_queue(request):
        try:
            org_domain = request.form['org_domain']
            organization = Organization.query.filter_by(org_domain=org_domain).first()
            if not organization:
                return dict(
                    status='FAIL',
                    message='No such organization',
                    error='Invalid number format',
                    request_args=request.form
                )

            queue_id = request.form['queue_id']
            queue_name = request.form['queue_name']
            queue = Queue.query.filter_by(queue_org_id=organization.org_id, queue_id=queue_id).first()
            queue.queue_name = queue_name
            db.session.commit()
            return dict(
                status='OK',
                message='Successfully updated this queue.',
                error=None
            )

        except Exception as e:
            return dict(
                status='FAIL',
                message='Could not update that queue.',
                error=str(e), request_args=request.form
            )

    @staticmethod
    def delete_queue(request):
        try:
            org_domain = request.form['org_domain']
            organization = Organization.query.filter_by(org_domain=org_domain).first()
            if not organization:
                return dict(
                    status='FAIL',
                    message='No such organization',
                    error='Invalid number format',
                    request_args=request.form
                )
            queue_id = request.form['queue_id']
            queue = Queue.query.get(queue_id)
            db.session.delete(queue)
            db.session.commit()
            return dict(
                status='OK',
                message='Queue deleted successfully.',
                error=None
            )

        except Exception as e:
            return dict(
                status='FAIL',
                message='Could not delete queue.',
                error=str(e),
                request_args=request.form
            )

    @staticmethod
    def enqueue(phone_number, queue_id):
        queued_time = datetime.utcnow()
        valid_number = tools.sanitize_number(phone_number)
        if not valid_number:
            return dict(
                status='FAIL',
                message='Invalid number format.',
                error='Invalid number format',
                request_args=dict(phone_number=phone_number, queue_id=queue_id)
            )

        entry = QueueData(
            phone_number=phone_number,
            queue_id=queue_id,
            queue_entry_time=queued_time)
        db.session.add(entry)
        db.session.commit()

        position = tools.get_queue_position(queue_id, valid_number, queued_time)
        message = 'Thank you for joining the virtual queue. You are currently in position %s.' % position
        # notify.send_message(to_number=phone_number, message=message)
        return dict(status='OK', message='User has been queued.', queue_position=position, error=None)

    @staticmethod
    def dequeue(phone_number, queue_id):
        entry = QueueData.query.filter_by(
            phone_number=phone_number,
            queue_id=queue_id,
            user_queued=True).first()

        if not entry:
            return dict(
                status='FAIL',
                message='Queued user does not exist.',
                error='Queued user does not exist.',
                request_args=dict(phone_number=phone_number, queue_id=queue_id))

        entry.queue_exit_time = datetime.utcnow()
        entry.user_queued = False
        db.session.commit()

        tools.notify_queue_position(queue_id)

        return dict(status='OK', message='User has successfully been dequeued.', error=None)

    @staticmethod
    def get_queue(org_domain, queue_id):
        queue = Queue.query \
            .join(Organization) \
            .filter(Queue.queue_id == queue_id) \
            .filter(Organization.org_domain == org_domain).first()

        if not queue:
            return dict(
                status='FAIL',
                message='That queue does not exist.',
                error='No such queue.',
                request_args=dict(org_domain=org_domain, queue_id=queue_id))

        data = QueueData.query \
            .filter(QueueData.queue_id == queue.queue_id) \
            .filter(QueueData.user_queued == True).all()
        queue_data = dict(queue=queue.serialize, queue_data=[i.serialize for i in data])
        return queue_data

    @staticmethod
    def get_queues(org_domain):
        # this has been quickly hacked together...
        q_data = []
        queues = Queue.query \
            .join(Organization) \
            .filter(Organization.org_domain == org_domain).all()

        for queue in queues:
            data = QueueData.query \
                .filter_by(
                queue_id=queue.queue_id,
                user_queued=True).all()
            if data:
                for x in data:
                    serialize = x.serialize
                    q_data.append(serialize)

        queue_data = dict(queues=[i.serialize for i in queues], queue_data=q_data)
        return queue_data
