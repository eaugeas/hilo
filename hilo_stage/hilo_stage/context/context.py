from typing import Any, Dict, List, Optional, Text


class Context(object):
    def __init__(
            self,
            current: Text,
            parents: Optional[List[Text]] = None,
            context: Optional[Dict[Text, Any]] = None
    ):
        self._current: Text = current
        self._parents: List[Text] = parents if parents else []
        self._context: Dict[Text, Any] = context if context else {}

    @property
    def current(self) -> Text:
        return self._current

    @property
    def abs_current(self) -> Text:
        return self.abs_path(self._current)

    def abs_path(self, rel_path) -> Text:
        return '/'.join(self._parents + [rel_path])

    @property
    def abs_current_url_friendly(self) -> Text:
        abs_current = self.abs_current
        return abs_current.lstrip('/').replace('/', '_')

    def child(self, current: Text) -> 'Context':
        return Context(
            current,
            self._parents + [self._current],
            self._context)

    def has(self, resource: Text) -> bool:
        if resource in self._context:
            return True

        abs_current = self.abs_path(resource)
        return abs_current in self._context

    def get(self, resource: Text, default: Optional[Any] = None) -> Any:
        if resource in self._context:
            return self._context[resource]

        for i in range(0, len(self._parents)):
            abs_resource = '/'.join(
                self._parents[0:len(self._parents) - i] + [resource])
            if abs_resource in self._context:
                return self._context[abs_resource]

        abs_current = '/'.join(self._parents + [self._current] + [resource])
        if abs_current in self._context:
            return self._context[abs_current]

        if default is not None:
            return default

        raise KeyError(
            'Resource `{0}` not found in context'.format(resource))

    def put(self, resource: Text, o: Any):
        if not resource.startswith('/'):
            resource = '/'.join(self._parents + [self._current] + [resource])

        if not resource.startswith('/'.join(self._parents)):
            raise KeyError(
                'Attempt to write to resource without permission '
                'for resource: {0}'.format(resource))

        if resource in self._context:
            raise KeyError(
                'Resource `{0}` already in context'.format(resource))

        self._context[resource] = o
