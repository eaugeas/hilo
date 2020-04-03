from typing import Any, Dict, List, Text, Type


class Directive(object):
    """Directive is a base class for directives that can be
    executed in specifications"""
    def __init__(self, command: Text, *args, **kwargs):
        pass

    def execute(self) -> Text:
        raise NotImplementedError()


class EnvironDirective(Directive):
    """EnvironDirective maps an environment variable to its value"""
    def __init__(self, command: Text, *args, **kwargs):
        if command != 'env':
            raise ValueError(
                'EnvironDirective must be initialized '
                'with `env` command. Received {0}'.format(command))
        super().__init__(command, *args, **kwargs)

        self._args = args
        self._kwargs = kwargs

        if 'env' in self._kwargs:
            self._kwargs = self._kwargs['env']
        elif self._kwargs.get('use_os_environ', False):
            import os
            self._kwargs = os.environ
        elif self._kwargs.get('use_os_environ', None) is None:
            import os
            self._kwargs = os.environ

    def execute(self) -> Text:
        if len(self._args) != 1:
            raise ValueError(
                '`env` directive only supports one argument.'
                ' Received {0}'.format(self._args))

        variable = self._args[0]
        if variable not in self._kwargs:
            raise KeyError(
                '`env` directive cannot find environment variable {0} '
                'defined in environment'.format(variable))
        return self._kwargs[variable]


def starts_as_directive(s: Text) -> bool:
    return s.startswith('$')


def parse_directive(s: Text) -> List[Text]:
    """parse_directive parses the directive
    $(command arg1 arg2 ...) into a list [command, arg1, arg2, ...]"""
    if not s.startswith('$(') and s.endswith(')'):
        raise ValueError(
            'not a directive. A directive follows the '
            'format $(command arg1 arg2 ...). Received {0}'.format(s))

    stripped = s.lstrip('$(').rstrip(')')
    split = stripped.split(' ')
    if len(split) < 1:
        raise ValueError(
            'not a directive. A directive follows the '
            'format $(command arg1 arg2 ...). Received {0}'.format(s))
    return split


def create(s: Text, **kwargs) -> Directive:
    """create a new directive from the text specifying
    the directive. THe format of a directive is
    $(command arg1 arg2 ...)"""
    args = parse_directive(s)
    return build(args[0], *args[1:], **kwargs)


def build(command: Text, *args, **kwargs) -> Directive:
    """build a new instance of a directive from its
    command and its arguments"""
    directives: Dict[Text, Type[Directive]] = {
        'env': EnvironDirective
    }

    if command in directives:
        return directives[command](command, *args, **kwargs)
    else:
        raise ValueError(
            'Unknown directive `{0}`. Valid directives are: {1}'.format(
                command, ', '.join(directives.keys())))


def execute(o: Any, **kwargs) -> Any:
    """execute applies all the directives on the object"""
    if isinstance(o, dict):
        for key in o:
            o[key] = execute(o[key])
        return o
    elif isinstance(o, list):
        for i in range(0, len(o)):
            o[i] = execute(o[i])
        return o
    elif isinstance(o, Text):
        if starts_as_directive(o):
            directive = create(o, **kwargs)
            return directive.execute()
        else:
            return o
    else:
        return o
