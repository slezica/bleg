import glob, os
import markdown as md
import bleach

import tools
from tools import templatefilter, admincommand
from cfg import settings


@templatefilter
def datestr(date, spaces = True):
    return tools.datestr(date, spaces)

@templatefilter
def markdown(text):
    return md.markdown(text, extensions = [
        'codehilite',
        'smarty' # HTML-izes ', ", --, ---, ... to &lsquo;, &rsquo;, etc.
    ])

@templatefilter
def sanitize(html):
    return bleach.clean(html, tags = bleach.ALLOWED_TAGS + ['p'])


@admincommand
def loadposts(*args, **opts):
    from models import Post

    files = glob.glob(os.path.join(settings.POST_ROOT, '*.md'))

    for filename in files:
        new_post = Post.from_file(filename)

        try:
            old_post = Post.objects.get(slug = new_post.slug)
            changed  = False

            for attr in ('body', 'date', 'title'):
                new_value = getattr(new_post, attr)
                old_value = getattr(old_post, attr)

                if new_value != old_value:
                    setattr(old_post, attr, new_value)
                    changed = True

            if changed:
                old_post.save()
                print '\033[1;33m' 'CHG' '\033[00m', old_post
            else:
                print '\033[1;31m' 'OLD' '\033[00m', old_post

        except Post.DoesNotExist:
            print '\033[1;32m' 'NEW' '\033[00m', new_post
            new_post.save()
