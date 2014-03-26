title: Goodbye GNU cut
date: 2014-03-07

GNU `cut` is one of those small programs that embody the Unix philosophy. `cut`
does exactly one thing, and is ready to work with pipes. From a modern
perspective, however, `cut` is simply too primitive.

The shortcomings of `cut` drive people to use `grep`, `sed` or `awk` for inline
field selection, which is theoretically `cut`'s responsibility. These
regex-powered tools, however, are meant for more complex operations, and require
advanced know-how and special syntax.

So I wrote [`sel`](http://github.com/slezica/sel).

[`sel`](http://github.com/slezica/sel) serves the same purpose as `cut`, with
notably improved syntax and better, more flexible features. It's a zero-googling
field selection and table transformation tool, a strict superset of `cut` that
doesn't require a DSL to operate.

Goodbye, `cut`.