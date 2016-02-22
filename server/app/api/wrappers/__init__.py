from organization import OrganizationManager
from queues import QueueManager
from queue_group import QueueGroupManager
from settings import SettingsManager


class Manager(object):
    def __init__(self):
        self.organization = OrganizationManager()
        self.queue = QueueManager()
        self.group = QueueGroupManager()
        self.settings = SettingsManager()