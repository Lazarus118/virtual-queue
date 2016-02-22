from app import db


class Organization(db.Model):
    __tablename__ = 'organization'
    org_id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    org_name = db.Column(db.String(45), nullable=False, default='Default Name')
    org_domain = db.Column(db.String(45), nullable=False, unique=True, index=True)
    org_country = db.Column(db.String(45), nullable=False)
    org_address = db.Column(db.String(80), nullable=False)
    org_phone = db.Column(db.String(15))
    org_email = db.Column(db.String(45))
    org_contact = db.Column(db.String(45))
    org_queue_groups = db.relationship('QueueGroup', backref='org_queue_groups', lazy='dynamic')
    org_queues = db.relationship('Queue', backref='org_queues', lazy='dynamic')
    org_settings = db.relationship('Settings', backref='org_settings', lazy='dynamic')

    @property
    def serialize(self):
        return {
            'org_id': self.org_id,
            'org_name': self.org_name,
            'org_domain': self.org_domain,
            'org_country': self.org_country,
            'org_address': self.org_address,
            'org_phone': self.org_phone,
            'org_email': self.org_email,
            'org_contact': self.org_contact,
            'org_queue_groups': [i.serialize for i in self.org_queue_groups],
            'org_settings': [i.serialize for i in self.org_settings]
        }


class QueueGroup(db.Model):
    __tablename__ = 'queue_group'
    group_id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    group_name = db.Column(db.String(45))
    group_note = db.Column(db.String(200))
    group_org_id = db.Column(db.Integer, db.ForeignKey('organization.org_id'))
    group_queues = db.relationship('Queue', backref='group_queues', lazy='dynamic')

    @property
    def serialize(self):
        return {
            'group_id': self.group_id,
            'group_name': self.group_name,
            'group_note': self.group_note,
            'group_queues': [i.serialize for i in self.group_queues]
        }


class Queue(db.Model):
    __tablename__ = 'queue'
    queue_id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    queue_name = db.Column(db.String(45), nullable=False)
    queue_org_id = db.Column(db.Integer, db.ForeignKey('organization.org_id'), nullable=False)
    queue_group_id = db.Column(db.Integer, db.ForeignKey('queue_group.group_id'), nullable=False)
    queue_org_name = db.relationship('Organization', backref='queue_org', uselist=False)
    queue_group_name = db.relationship('QueueGroup', backref='queue_group', uselist=False)
    queue_data = db.relationship('QueueData', backref='queue_data', lazy='dynamic')

    def __repr__(self):
        return '<Queue: %s>' % self.queue_name

    @property
    def serialize(self):
        return {
            'queue_id': self.queue_id,
            'queue_name': self.queue_name,
            'queue_wait': 3600
        }


class QueueData(db.Model):
    __tablename__ = 'queue_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone_number = db.Column(db.String(15), nullable=False)
    user_queued = db.Column(db.Boolean, default=True)
    queue_entry_time = db.Column(db.DateTime)
    queue_exit_time = db.Column(db.DateTime)
    queue_id = db.Column(db.Integer, db.ForeignKey('queue.queue_id'))

    @property
    def serialize(self):
        return {
            'data_id': self.id,
            'phone_number': self.phone_number,
            'queue_entry': self.queue_entry_time,
            'queue_exit': self.queue_exit_time,
            'queue_id': self.queue_id,
            'user_queued': self.user_queued
        }


class Settings(db.Model):
    __tablename__ = 'system_settings'
    setting_id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    setting_name = db.Column(db.String(80), index=True)
    setting_value = db.Column(db.String(250))
    setting_org_id = db.Column(db.Integer, db.ForeignKey('organization.org_id'))

    @property
    def serialize(self):
        return {
            'setting_id': self.setting_id,
            'setting_name': self.setting_name,
            'setting_value': self.setting_value,
            'setting_org_id': self.setting_org_id
        }

