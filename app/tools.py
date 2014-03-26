import functools
from datetime import datetime

from django.shortcuts import render
from django.core import paginator


def strdate(string):
    return datetime.strptime(string, '%Y-%m-%d')

def datestr(date):
    return datetime.strftime(date, '%Y-%m-%d')


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