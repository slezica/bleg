import markdown as md

import tools
from tools import templatefilter, admincommand

@templatefilter
def datestr(date, spaces = True):
    return tools.datestr(date, spaces)

@templatefilter
def markdown(text):
    return md.markdown(text, extensions = [
        'codehilite',
        'smarty' # HTML-izes ', ", --, ---, ... to &lsquo;, &rsquo;, etc.
    ])


@admincommand
def jaja(*args, **opts):
    print 'hola'