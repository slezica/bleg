import sys, functools
from datetime import datetime

import django
from django.shortcuts import render
from django.core import paginator
from django.core.management import ManagementUtility
from django.core.management.base import BaseCommand, CommandError


def strdate(string):
    return datetime.strptime(string, '%Y-%m-%d')

def datestr(date, spaces = False):
    return datetime.strftime(date, '%Y - %m - %d' if spaces else '%Y-%m-%d')


def view(f):
    template = f.__name__ + '.html'

    def wrapper(request, *args, **kwargs):
        return render(request, template, f(request, *args, **kwargs))

    functools.update_wrapper(wrapper, f)
    return wrapper


class Paginator(paginator.Paginator):
    def page(self, number):
        sself = super(Paginator, self)

        try:
            return sself.page(number)

        except paginator.PageNotAnInteger:
            return sself.page(1)

        except paginator.EmptyPage:
            return sself.page(self.num_pages)


def module(path):
    def decorator(cls):
        if '.' in path:
            parent_path, name = path.rsplit('.', 1)
            module(parent_path)(type(name, (object,), { name: cls }))
        
        return sys.modules.setdefault(path, cls)
    return decorator


@module('app.templatetags.extras')
class TemplateExtra(object):
    class register:
        tags    = {}
        filters = {}

def templatetag(f):
    return TemplateExtra.register.tags.setdefault(f.__name__, f)

def templatefilter(f):
    return TemplateExtra.register.filters.setdefault(f.__name__, f)

django.template.libraries['app.templatetags.extras'] = TemplateExtra
django.template.base.add_to_builtins('app.templatetags.extras')


class ManagementExtra(ManagementUtility):
    commands = {}

    def fetch_command(self, name):
        cmd = ManagementExtra.commands.get(name)
        return cmd or super(ManagementExtra, self).fetch_command(name)

class Command(BaseCommand):
    def __init__(self, f):
        super(Command, self).__init__()
        self.f = f

    def handle(self, *args, **kwargs):
        return self.f(*args, **kwargs)

def admincommand(f):
    return ManagementExtra.commands.setdefault(f.__name__, Command(f))