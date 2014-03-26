import os
from glob import glob

from cfg import settings
from django.db.models import Model, CharField, DateField, TextField

from tools import strdate, datestr


class Post(Model):
    title = CharField(max_length = 256)
    slug  = CharField(max_length = 256)
    date  = DateField()
    body  = TextField()

    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return '%s %s' % (datestr(self.date), self.slug)

    @property
    def url(self):
        return '/post/' + self.slug

    def next(self):
        try:    return self.get_next_by_date()
        except: return None

    def prev(self):
        try:    return self.get_previous_by_date()
        except: return None


    @staticmethod
    def from_file(filename):
        with open(filename) as f:
            content = f.read().decode('utf8')
            
        header, body = content.split('\n\n', 1)

        meta = {
            key.strip(): value.strip() for key, value in
            (line.split(':', 1) for line in header.split('\n'))
        }

        return Post(
            title = meta['title'],
            slug  = filename.split('-', 3)[-1].rsplit('.')[0],
            date  = strdate(meta['date']),
            body  = body
        )

    @staticmethod
    def load_files():
        files = glob(os.path.join(settings.POST_ROOT , '*.md'))

        for filename in files:
            post = Post.from_file(filename)

            if not Post.objects.filter(slug = post.slug).exists():
                post.save()
