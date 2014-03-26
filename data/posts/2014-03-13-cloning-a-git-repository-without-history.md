title: Cloning a git repository without history
date: 2014-03-13

Large `git` repositories tend to owe a very large portion of their size to
commit history. Most of the time, however, when cloning a large project for
local usage, history is of no interest.

Take the `django` project, for example. To get the latest development version,
you have to clone a repository of no less than 158 megabytes. If you could
only grab just the latest code...
    
    :::bash
    git clone git://github.com/django/django.git --depth 1 

The `--depth` flag does the trick, bringing the number down to 61 megabytes.