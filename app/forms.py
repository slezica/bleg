from datetime import datetime

from django.forms import ModelForm

from models import Comment


class CommentForm(ModelForm):
    class Meta:
        model  = Comment
        fields = ('post', 'body',)

    def save(self):
        if not self.instance.id:
            self.instance.date = datetime.now().date()

        return super(CommentForm, self).save()
