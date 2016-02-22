import re
from sqlalchemy.sql import text

from app import db
from app.api.lib import Notify
from app.models import QueueData, Queue

notify = Notify(account_sid='123', auth_token='123', phone_number='123')


def sanitize_number(number):
    """
    :arg number: a string representation of a phone number
    """
    num = re.sub(r'\D', '', number)  # Strip anything that is not a number
    if len(num) >= 7 and len(num) <= 15:
        return num
    else:
        return False


def get_queue_position(queue_id, phone_number, time, ):
    queue = QueueData.query.filter_by(queue_id=queue_id, user_queued=True).all()
    queued_user = QueueData.query \
        .filter_by(
            queue_id=queue_id,
            phone_number=phone_number,
            queue_entry_time=time, user_queued=True).first()

    queue_list = [i.serialize for i in queue]
    index = 0
    for x in queue_list:
        q_num = x.get('phone_number')
        q_time = x.get('queue_entry')
        if q_time == queued_user.queue_entry_time and q_num == queued_user.phone_number:
            return index
        else:
            index += 1

    return index


def notify_queue_position(queue_id):
    queue_entry = Queue.query.filter(Queue.queue_id == queue_id).first()
    if not queue_entry:
        return dict(
                status='FAIL',
                message='That queue does not exist.',
                error='No such queue.',
                request_args=dict(queue_id=queue_id))

    queue = QueueData.query \
        .filter_by(queue_id=queue_id, user_queued=True) \
        .order_by(QueueData.id) \
        .all()
    # queue = queue.order_by(QueueData.id)
    queue_list = [i.serialize for i in queue]

    result = {}

    try:
        first_position = queue_list[0]
        message1 = "You are next in line. Get ready to go to the counter."
        # response1 = notify.send_message(to_number=first_position.get('phone_number'), message=message1)
        response1 = "Dummy Response 1"
        result['first_element'] = first_position
        result['first_response'] = response1


    except:
        print "An error occurred when trying to get the first item in the queue"

    try:
        fifth_position = queue_list[4]
        message2 = "You are now fifth in line. Please make your way to the service area."
        # response2 = notify.send_message(to_number=fifth_position.get('phone_number'), message=message2)
        response2 = "Dummy Response 2"
        result['fifth_element'] = fifth_position
        result['fifth_response'] = response2

    except:
        print "An error occurred when trying to get the fifth item in the queue"

    return result


def get_average_wait_time(queue_id):
    queue_entry = Queue.query.filter(Queue.queue_id == queue_id).first()
    if not queue_entry:
        return dict(
                status='FAIL',
                message='That queue does not exist.',
                error='No such queue.',
                request_args=dict(queue_id=queue_id))

    query = "select coalesce(avg(strftime('%s', queue_entry_time) - strftime('%s', queue_exit_time)),3600) as average_wait_time from queue_data where queue_entry_time >= datetime('now','-1 hour') and queue_id == :queue;"
    sql = text(query)
    result = db.engine.execute(sql, queue=queue_id)
    for row in result:
        return {'average_time': row[0]}
