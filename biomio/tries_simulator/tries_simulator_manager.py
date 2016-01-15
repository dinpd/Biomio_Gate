from random import randint
from threading import Lock
from os import urandom
from hashlib import sha1


class TriesSimulatorManager:
    _instance = None
    _lock = Lock()

    _try_request_template = dict(
        oid='try',
        resource=[],
        policy=dict(condition='any'),
        try_id=sha1(urandom(32)).hexdigest()[:8],
        authTimeout=300,
        message='Authentication'
    )

    _try_resources_by_type = dict(
        face=dict(rType='front-cam', rProperties="1280x720"),
        fp=dict(rType='fp-scanner', rProperties=""),
        push_button=dict(rType='interact', rProperties=""),
        pin_code=dict(rType='input', rProperties="%s" % randint(100000, 999999)),
        location=dict(rType='location', rProperties="100"),
        credit_card=dict(rType='back-cam', rProperties=""),
    )

    def __init__(self):
        self._current_connections = {}

    @classmethod
    def instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = TriesSimulatorManager()
        return cls._instance

    def add_active_connection(self, app_id, connection_instance):
        self._current_connections.update({app_id: connection_instance})

    def remove_active_connection(self, app_id):
        if app_id in self._current_connections:
            del self._current_connections[app_id]

    def get_active_connections(self):
        return self._current_connections.keys()

    def send_try_request(self, auth_types, condition, app_id):
        self._try_request_template.get('policy').update({'condition': condition})
        resources = []
        for auth_type in auth_types:
            t_resource = dict(
                tType=auth_type,
                resource=self._try_resources_by_type.get(auth_type),
                samples=1
            )
            resources.append(t_resource)
        self._try_request_template.update({'resource': resources})
        current_connection = self._current_connections.get(app_id)
        if current_connection is not None:
            message = current_connection.create_next_message(
                request_seq=current_connection._last_received_message.header.seq,
                **self._try_request_template
            )
            current_connection.send_message(responce=message)
