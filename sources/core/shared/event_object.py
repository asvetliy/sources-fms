import json
import importlib

from sources.core.helpers import get_from_path


class EventObject:
    def __init__(self, name, attributes, options):
        self.options = options
        self.name = name
        self.attributes = attributes

    @classmethod
    def make_from_event(cls, event_message: dict, event_name: str, event_config: dict):
        options = event_config
        name = event_name
        attributes = {}
        for key, value in options['attributes'].items():
            attributes[key] = get_from_path(event_message, value)
        return cls(name, attributes, options['options'])

    def to_dict(self):
        return {
            'attributes': self.attributes,
            'name': self.name,
            'options': self.options
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def make_request_object(self):
        if 'request_object_type' not in self.options:
            return None
        class_name = self.options['request_object_type'] + 'RequestObject'
        module = importlib.import_module('app.core.use_cases.request_objects')
        request_object_class = getattr(module, class_name, None)
        if request_object_class is None:
            return None
        return request_object_class.validate(self.attributes)

    @classmethod
    def unpack_event(cls, entrypoint, event):
        name_path = entrypoint.options['listener']['events']['events_params']['name_path']
        events_array = entrypoint.options['listener']['events']['events_array']
        event_name = get_from_path(event, name_path)
        if event_name is None or event_name not in events_array:
            return None
        return cls.make_from_event(event, event_name, events_array[event_name])


