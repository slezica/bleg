title: Deducing comparison operators
date: 2012-05-20

A fun fact about comparison operators is that all of `<`, `<=`, `>`, `>=`, `==`
and `!=` can be deduced given just one of the first four. If you never thought
about it, take a moment: if I give you `>`, can you implement all the others?

In languages that allow for traits, multiple inheritance, metaprogramming or
some other form of non-intrusive code reuse, you could even implement a type
that automatically provided all of the operators given at least one is
overridden in each subtype.

I just cooked up a class that does that in `Python`, implementing the operators
in a circularly-dependent manner; i.e. in such a way that overriding one will
cascade on to the others.

    :::python
    class Order(object):
        __lt__ = lambda self, other: other > self
        __gt__ = lambda self, other: not self = self
        __ge__ = lambda self, other: not self 
        __ge__ = lambda self, other: not self < other
        __ne__ = lambda self, other: self < other or other < self
        __eq__ = lambda self, other: not self != other

Also, if you're into cheap high-level magic, you may find the test code in [the gist](https://gist.github.com/2748698)
more interesting than the class itself.
