from app import db
from sqlalchemy.exc import IntegrityError
from app.models import Organization, Queue


class OrganizationManager(object):
    def __init__(self):
        pass

    @staticmethod
    def post_org(request):
        try:
            org_name = request.form.get('org_name')
            org_domain = request.form.get('org_domain')
            org_address = request.form.get('org_address')
            org_country = request.form.get('org_country')
            org_phone = request.form.get('org_phone', '')
            org_email = request.form.get('org_email', '')
            org_contact = request.form.get('org_contact', '')

            org = Organization(
                org_name=org_name,
                org_domain=org_domain,
                org_address=org_address,
                org_country=org_country,
                org_phone=org_phone,
                org_email=org_email,
                org_contact=org_contact
            )
            db.session.add(org)
            db.session.commit()
            return dict(status='OK', message='Orgnization created successfully.', error=None)
        except IntegrityError as e:
            return dict(status='FAIL', message='A similar organization already exists.', error=str(e))
        except Exception as e:
            return dict(status='FAIL', message='Could not create organization.', error=str(e))

    @staticmethod
    def get_org(org_domain):
        org = Organization.query.filter_by(org_domain=org_domain).first()
        if not org:
            return dict(
                status='FAIL',
                message='No such organization.',
                request_args=dict(org_domain=org_domain))
        return org.serialize

    @staticmethod
    def update_org(request):
        try:
            org_domain = request.form.get('org_domain')
            organization = Organization.query.filter_by(org_domain=org_domain).first()
            if not organization:
                return dict(
                    status='FAIL',
                    message='No such organization',
                    request_args=request.form,
                    error='No such organization')

            org_name = request.form.get('org_name')
            org_address = request.form.get('org_address')
            org_country = request.form.get('org_country')
            org_phone = request.form.get('org_phone', '')
            org_email = request.form.get('org_email', '')
            org_contact = request.form.get('org_contact', '')

            organization.org_name = org_name
            organization.org_address = org_address
            organization.org_country = org_country
            organization.org_phone = org_phone
            organization.org_email = org_email
            organization.org_contact = org_contact

            db.session.commit()
            return dict(status='OK', message='Organization updated successfully.', error=None)

        except Exception as e:
            return dict(
                status='FAIL',
                message='Could not updated this organization. An unexpected error has occured.',
                request_args=request.form,
                error=str(e))

    @staticmethod
    def delete_org(request):
        """
        TODO: Create cleanup script for clearing queue data
        """
        try:
            org_domain = request.form.get('org_domain')
            organization = Organization.query.filter_by(org_domain=org_domain).first()
            if not organization:
                return dict(
                    status='FAIL',
                    message='That organization does not exist.',
                    request_args=org_domain,
                    error='No such organization.')

            Queue.query.filter_by(queue_org_id=organization.org_id).delete()
            db.session.delete(organization)
            db.session.commit()
            return dict(status='OK', message='Organization deleted successfully.', error=None)

        except Exception as e:
            return dict(
                status='FAIL',
                message='Could not delete this organization. An unexpected error has occured.',
                request_args=request.form,
                error=str(e)
            )
