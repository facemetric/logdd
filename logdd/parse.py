import functools
import re

__REPLACE_CHAR = '__'


def __prepare_pattern(pattern):
    return pattern.replace('\\', '\\\\') \
        .replace('[', '\[').replace(']', '\]') \
        .replace('(', '\(').replace(')', '\)')


def __load_pattern(spec, names, prefix=''):
    pattern = __prepare_pattern(spec['pattern'])
    formats = {}
    complex_formats = {}
    for k, v in spec['variables'].items():
        if isinstance(v, dict):
            complex_formats[k] = __load_pattern(v, names, '{}{}'.format(k, __REPLACE_CHAR))
        else:
            formats[k] = v

    def _format_replacer(match_obj):
        name = match_obj.group(0)[1:]
        if name in formats:
            replaced_name = '{}{}'.format(prefix, name.replace(__REPLACE_CHAR, ''))
            names.append(replaced_name)
            return '(?P<{}>{})'.format(replaced_name, formats[name])
        elif name in complex_formats:
            return complex_formats[name]
        else:
            raise Exception('Failed to load format for {}'.format(name))

    return ('^{}$' if not prefix else '{}').format(re.sub('\$[\w_\d]*\\b', _format_replacer, pattern))


def __str_mapper(name, match):
    return match.group(name)


def __dict_mapper(name_mapping: dict, match):
    return {name: loader(match) for name, loader in name_mapping.items()}


def _load_mappers(names: list, prefix: str = ''):
    analyzed_names = [name[len(prefix):] for name in names if name.startswith(prefix)]
    mappers = {}
    already_load = []
    for name in analyzed_names:
        if __REPLACE_CHAR in name:
            name_start = name.split(__REPLACE_CHAR, 1)[0]
            if name_start not in already_load:
                already_load.append(name_start)
                mappers[name_start] = _load_mappers(names, '{}{}{}'.format(prefix, name_start, __REPLACE_CHAR))
        else:
            mappers[name] = functools.partial(__str_mapper, '{}{}'.format(prefix, name))
    return functools.partial(__dict_mapper, mappers)


class FormatSpec(object):
    def __init__(self, names: list, pattern: str):
        self.result_mapper = _load_mappers(names)
        self.pattern = re.compile(pattern)

    def parse(self, line):
        if line[-1] == '\n':
            line = line[:-1]
        match = self.pattern.match(line)
        if match:
            return self.result_mapper(match)


def load_pattern(spec: dict) -> FormatSpec:
    names = []
    return FormatSpec(names, __load_pattern(spec, names))
