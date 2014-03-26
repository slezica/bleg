title: Stochastic generation
date: 2012-05-19

Today, I've been looking into using non-deterministic (let's say randomized)
methods to generate information based on samples.

Broadly speaking, the idea is to analyze an input stream to detect patterns, and
then produce an output stream of non-deterministic information that resembles
the original. The information can be text, music, or basically anything
[_discrete_](http://en.wikipedia.org/wiki/Discrete_space), anything you can
separate into a series of items – letters/words, musical notes, etc.

Specifically, I've been toying with [Markov chains](http://en.wikipedia.org/wiki/Markov_chain)
configured from the input. If you're not familiar with the concept, and choose
not to read through a mile of Wikipedia text, allow me a quick introduction.

## Markov Chains

[{% img right http://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Markovkate_01.svg/220px-Markovkate_01.svg.png "2-state Markov chain" %}](http://en.wikipedia.org/wiki/Markov_chain)

A Russian mathematician named Andrey Markov described a way to model processes
by breaking them up into _states_, and then for each _state_ offering the
probability of passing to another _state_. _Markov chains_ are part of his
theory.

Take a look at the image to the right. It's showing a 2-state process, as
described by a Markov chain. What it means is:

*   There's two states: **A**, and **E**

*   When the process is in state **A**, it has a 60% probability of remaining in
that state, and a 40% probability of changing to **E**

*   When the process is in state **E**, it has a 30% probability of remaining in
that state, and a 70% probability of changing to **A**

Markov chains have no long-term memory: the probability of going from **A** to
**E** is always the same, it doesn't matter if we've been in **A** for a while,
or if we just jumped back from **E**. In other words, _the next state depends
solely on the current one_.

Well, that's not always true: a Markov chain is said to be of _order 1_ in that
case. In a _Markov chain of order 2_, the probability of reaching a state next
depends on the _two previous states_. In general, _order **n**_ means the
short-term memory of the Markov chain includes the last **n** states visted.

Good? Good. So what does this have to do with generating text or music?

## Analyzing a stream

A Markov chain can created from any stream of information. Items that come out
of the stream are considered **states**, and whenever an item **X** follows an
item **Y**, we reflect that in the chain by appropriately increasing the
probability of going from state **X** to state **Y**.

For example, say you analyzed the following text and built a Markov chain based
on letters you find:

### Lorem ipsum dolor sit amet, consectetur adipiscing elit

You could then ask what letters can follow an 'i', and what's the probability of
each doing so – you'd get _33% 'p', 18% 's', 33% 't', and 16% 'n'_.

## Generating a similar stream

Once the **Nth-order** chain is built, and probabilities are known as above, it
can used to answer the following question:

### Given a group of **n** known items, what can the next item be?

The answer will be in the form of _"30% chance that it's this, 25% chance that
it's that, etc"_. So, starting with any known **n** items, the information in
the Markov chain can be used to generate any amount of following items randomly,
but taking into account how those were related in the original stream.

The higher the quality and quantity of the information you feed into the stream,
the better its predictions will be and the more sense the generated stream will
make – up to a point, of course. Markov chains of higher order tend to
generate better results, too, since they make predictions based on more
contextual information.

## Example: analyzing an ESPN sports article

I fed an ESPN sports article into my handy Markovifier-X2000 (_[don't you have
one?](https://gist.github.com/2732680)_), and had its letters analyzed to then
spit out a short text. Leaving aside the quality of information taken from ESPN
articles (thought they certainly are numerous), let me show the results for
varying orders of the underlying Markov chain so you can appreciate the effect.

**Order 1 chain (only last letter considered when picking next letter):**

> Hens's. wis af pe terect'sd o He. p mpaseen s hesil ongutecon go in jan f
tofreverat atee tin l gonspherd athensrenot a d d Ster

**Order 2 chain (last two letters considered):**

> uot fou witech th wanch the Pactiff himes fres play-Z aftess way. Heame, ing a
sectful durit. Game, beek. Games' guareplayery on t

**Order 3 chain:**

> Wization," Stevenson? You was ver their of the Heat LeBron the Pacers' com
one-hit again." The shown respectful. "I'm not use. "

**Order 4 chain:**

> He played one time, and the Miami Heat. He player, is not seen it. But it
again." The repeatedly over do it did that. It was flat

Getting better, huh?

**Order 10 chain:**

> Stevenson in 2007 during a playoff tiff he had with then Washington Wizards'
guard DeShawn Stevenson to one-hit wonder Soulja Boy.

Look at that. You could throw that below a picture in ESPN.com and nobody would
notice.

## Next steps

If it doesn't bore me first, I want to try this method for two more things:

*   Generating midi music from samples
*   Generating a (remotely) coherent text, using [Google's concept
database](http://googleresearch.blogspot.com.ar/2012/05/from-words-to-concepts-and-back.html).

The second item sounds exciting, though I have a feeling the results will be
dissapointing. I'll let you know.
