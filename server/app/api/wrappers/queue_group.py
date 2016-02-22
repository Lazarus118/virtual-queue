from app import db
from app.models import Organization, QueueGroup


class QueueGroupManager(object):
    def __init__(self):
        pass

    @staticmethod
    def post_group(request):
        try:
            org_domain = request.form['org_domain']
            organization = Organization.query.filter_by(org_domain=org_domain).first()
            if not organization:
                return dict(
                    status='FAIL',
                    message='That organization does not exist.',
                    request_args=org_domain,
                    error='No such organization.'
                )

            group = QueueGroup(
                group_name=request.form['group_name'],
                group_note=request.form.get('group_note', ''),
                group_org_id=organization.org_id
            )
            db.session.add(group)
            db.session.commit()
            return dict(status='OK', message='Group successfully created.', error=None)

        except Exception as e:
            return dict(
                status='FAIL',
                message='An error has occured.',
                error=str(e),
                request_args=request.form
            )

    @staticmethod
    def get_group(request):
        try:
            org_domain = request.args['org_domain']
            organization = Organization.query.filter_by(org_domain=org_domain).first()
            if not organization:
                return dict(
                    status='FAIL',
                    message='That organization does not exist.',
                    request_args=org_domain,
                    error='No such organization.'
                )
            group_id = request.args['group_id']
            group = QueueGroup.query\
                .filter_by(
                    group_id=group_id,
                    group_org_id=organization.org_id
            ).first()
            return group.serialize

        except Exception as e:
            return dict(
                status='FAIL',
                message='An error has occured.',
                error=str(e),
                request_args=request.args
            )

    @staticmethod
    def get_groups(request):
        try:
            org_domain = request.args['org_domain']
            organization = Organization.query.filter_by(org_domain=org_domain).first()
            if not organization:
                return dict(
                    status='FAIL',
                    message='That organization does not exist.',
                    request_args=org_domain,
                    error='No such organization.'
                )
            groups = QueueGroup.query.filter_by(group_org_id=organization.org_id).all()
            return dict(queue_groups=[i.serialize for i in groups])

        except Exception as e:
            return dict(
                status='FAIL',
                message='An error has occured.',
                error=str(e),
                request_args=request.args
            )

    @staticmethod
    def delete_group(request):
        try:
            org_domain = request.form['org_domain']
            organization = Organization.query.filter_by(org_domain=org_domain).first()

            if not organization:
                return dict(
                    status='FAIL',
                    message='That organization does not exist.',
                    request_args=org_domain,
                    error='No such organization.'
                )

            group_id = request.form['group_id']
            group = QueueGroup.query.filter_by(group_org_domain=organization.org_id, group_id=group_id).first()
            db.session.delete(group)
            db.session.commit()
            return dict(
                status='FAIL',
                message='Group has been deleted successfully.',
                error=None
            )
        except Exception as e:
            return dict(
                status='FAIL',
                message='An error has occured.',
                error=str(e),
                request_args=request.args
            )

    @staticmethod
    def update_group(request):
        try:
            org_domain = request.form['org_domain']
            organization = Organization.query.filter_by(org_domain=org_domain).first()

            if not organization:
                return dict(
                    status='FAIL',
                    message='That organization does not exist.',
                    request_args=org_domain,
                    error='No such organization.'
                )

            group_id = request.form['group_id']
            group_name = request.form['group_name']
            group_note = request.form.get('group_note', '')
            group = QueueGroup.query.get(group_id)
            group.group_name = group_name
            group.group_note = group_note
            db.session.commit()
            return dict(
                status='OK',
                message='Queue group has been updated successfully.',
                error=None
            )
        except Exception as e:
            return dict(
                status='FAIL',
                message='An error has occured.',
                error=str(e),
                request_args=request.args
            )
