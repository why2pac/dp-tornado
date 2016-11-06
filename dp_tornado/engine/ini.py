# -*- coding: utf-8 -*-

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import os

from .singleton import Singleton as dpSingleton


class IniSection(object):
    def __init__(self, parser, section):
        self.__dict__['_parser'] = parser
        self.__dict__['_section'] = section
        self.__dict__['_options'] = {}

    def __getattr__(self, name):
        try:
            return self.__getattribute__(name)
        except AttributeError:
            pass

        return self.__dict__['_options'][name] if name in self._options else None

    def __setattr__(self, key, value):
        self.__dict__['_options'][key] = value

    def get(self, key, default=None):
        if key in self.__dict__['_options']:
            return self.__dict__['_options'][key]

        got = self.__dict__['_parser'].get(section=self._section, key=key, default=default)
        self.__setattr__(key, got)

        return got

    def set(self, key, val):
        self.__setattr__(key, val)


class IniParser(object):
    def __init__(self, parser):
        self._parser = parser

    def get(self, section, key, default=None):
        try:
            if not self._parser:
                got = False
            else:
                got = self._parser.get(section, key)

            if default is True or default is False:
                return True if got == '1' else False

            elif isinstance(default, str):
                return str(got)

            elif isinstance(default, int):
                return int(got)

            else:
                return got

        except (configparser.NoSectionError, configparser.NoOptionError):
            return default


class Initialization(dpSingleton):
    def __init__(self):
        self.__dict__['_sections'] = {}
        self.__dict__['_parser'] = None

    @property
    def _parser(self):
        if self.__dict__['_parser']:
            return self.__dict__['_parser']

        application_path = os.getenv('DP_APPLICATION_PATH')
        ini_file = os.getenv('DP_APPLICATION_INI')

        if not application_path or not ini_file:
            parser = None

        else:
            parser = configparser.RawConfigParser()
            parser.read(os.path.join(application_path, ini_file))

        ini_parser = IniParser(parser)
        self.__dict__['_parser'] = ini_parser

        return ini_parser

    def __getattr__(self, name):
        try:
            return self.__getattribute__(name)
        except AttributeError:
            pass

        section = self.__dict__['_sections'][name] if name in self.__dict__['_sections'] else None

        if not section:
            section = IniSection(self._parser, name)
            self.__dict__['_sections'][name] = section

        return section
