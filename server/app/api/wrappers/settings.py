from app import db
from app.models import Organization, Settings


class SettingsManager(object):
    def __init__(self):
        pass

    @staticmethod
    def post_setting(request):
        try:
            org_domain = request.form['org_domain']
            organization = Organization.query.filter_by(org_domain=org_domain).first()

            if not organization:
                return dict(
                    status='FAIL',
                    message='That organization does not exist.',
                    request_args=org_domain,
                    error='No such organization.')

            setting_name = request.form['setting_param']
            setting_value = request.form['setting_value']

            setting = Settings(
                setting_name=setting_name,
                setting_value=setting_value,
                setting_org_id=organization.org_id
            )
            db.session.add(setting)
            db.session.commit()
            return dict(
                status='OK',
                message='Setting has been added successfully.',
                error=None
            )
        except Exception as e:
            return dict(
                status='FAIL',
                message='An error has occured.',
                error=str(e),
                request_args=request.form
            )

    @staticmethod
    def update_setting(request):
        try:
            org_domain = request.form['org_domain']
            organization = Organization.query.filter_by(org_domain=org_domain).first()

            if not organization:
                return dict(
                    status='FAIL',
                    message='That organization does not exist.',
                    request_args=org_domain,
                    error='No such organization.')

            setting_id = request.form['setting_id']
            setting_name = request.form['setting_param']
            setting_value = request.form['setting_value']

            setting = Settings.query.filter_by(setting_name=setting_id, setting_org_id=organization.org_id).first()
            setting.setting_name = setting_name
            setting.setting_value = setting_value
            db.session.commit()
            return dict(
                status='OK',
                message='Setting has been updated successfully.',
                error=None
            )

        except Exception as e:
            return dict(
                status='FAIL',
                message='An error has occurred.',
                error=str(e),
                request_args=request.form
            )

    @staticmethod
    def get_setting(request):
        try:
            org_domain = request.args['org_domain']
            organization = Organization.query.filter_by(org_domain=org_domain).first()

            if not organization:
                return dict(
                    status='FAIL',
                    message='That organization does not exist.',
                    request_args=org_domain,
                    error='No such organization.')

            setting_id = request.form['setting_id']
            setting_name = request.form['setting_param']
            setting_value = request.form['setting_value']

            setting = Settings.query.get_404(setting_id)
            setting.setting_name = setting_name
            setting.setting_value = setting_value
            db.session.commit()
            return dict(
                status='OK',
                message='Setting updated successfully.',
                error=None
            )

        except Exception as e:
            return dict(
                status='OK',
                message='An error has occurred.',
                error=str(e),
                request_args=request.args
            )

    @staticmethod
    def delete_setting(request):
        try:
            org_domain = request.form['org_domain']
            organization = Organization.query.filter_by(org_domain=org_domain).first()

            if not organization:
                return dict(
                    status='FAIL',
                    message='That organization does not exist.',
                    request_args=org_domain,
                    error='No such organization.')
            setting_id = request.form['setting_id']
            setting = Settings.query.filter_by(setting_org_id=organization.org_id, setting_id=setting_id).first()
            db.session.delete(setting)
            db.session.commit()
            return dict(
                status='OK',
                message='The settings has been deleted successfully.',
                error=None
            )

        except Exception as e:
            return dict(
                status='OK',
                message='Setting updated successfully.',
                error=None
            )