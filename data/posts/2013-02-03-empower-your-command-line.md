title: Empower your Command-Line
date: 2013-02-03

Most developers spend a lot of time in the command-line. Nothing to wonder
about: it's a [powerful
tool](http://blog.slezica.me/2012/06/29/stop-trying-to-get-rid-of-the-keyboard).
Oh, but it can get even better.

We'll start with simple `bash` and `.profile` tricks, and move on to crazier
stuff.

## Don't repeat yourself

Everyone knows to search history with `<Ctrl>+R`. Two other, little known `bash`
features are also amazing time-savers:

1.  The `!!` sequence grabs the last command you entered. You'll love it when
you forget to prepend `sudo` to a long line: `~$ sudo !!`.

2.  The `<Alt>+.` combination brings back in the latest entered tokens.
Fantastic for repeating file names and URLs.

3.  [Brace expansion](http://www.gnu.org/software/bash/manual/html_node/Brace-Expansion.html)
allows you to write similar names with minimal hassle.

Let me show you the tip of the iceberg:

    :::bash
    ~$ echo dir/{foo,bar,baz}.zip
    dir/foo.zip dir/bar.zip dir/baz.zip

There's a whole world of functionality aimed at reusing entries from your [history](http://www.gnu.org/software/bash/manual/html_node/Event-Designators.html#Event-Designators) and [expanding tokens](http://www.gnu.org/software/bash/manual/html_node/Shell-Expansions.html#Shell-Expansions).

## Move around fast

First, let's remove the pain of typing `cd ../../..`:
    
    :::bash
    alias ..="cd .."
    alias ...="cd ../.."
    alias ....="cd ../../.."

Combine that with the fact that `cd -` brings you back to the previous directory
you were in, and now you can quickly jump to your project's root and back to the
subdirectory you were working in.

## Keep your context at hand

If you need to perform a one-off task unrelated to your current workflow, don't
`cd` away and drop garbage in your `history`. Instead, invoke a subshell running
`bash`, do what you must, and `<Ctrl>+D` back to where you were.

## Never wait on grep again

The [Silver Searcher](https://github.com/ggreer/the_silver_searcher),
command-named `ag`, is a blazing fast drop-in replacement for `grep`/`awk`.
**Several** times as fast.

The author details some of the optimizations he made:

1.  Searching for literals (no regex) uses Boyer-Moore-Horspool strstr.
2.  Files are mmap()ed instead of read into a buffer.
3.  If you're building with PCRE 8.21 or greater, regex searches use the JIT
compiler.
4.  Ag calls pcre_study() before executing the regex on a jillion files.
5.  Instead of calling fnmatch() on every pattern in your ignore files,
non-regex patterns are loaded into an array and binary searched.
6.  Ag uses Pthreads to take advantage of multiple CPU cores and search files
in parallel.

Clone the repo, `make install`, and you're good to go.

## Interact with the clipboard

Copying and pasting to and from the system clipboard can get messy. You'll know
what I mean if you ever had to wait on a **long** stream of `command not found`
events after mistakenly pasting text with newlines, all the time wondering if
any line was a valid command.

Install `xclip`, and define two simple aliases:

    :::bash
    alias xc="xclip -selection clipboard"
    alias xp="xclip -selection clipboard -o"

Now you can copy text from your browser, and bring it into your command-line
painlessly, as well copy files or program outputs:

    :::bash
    ~$ cat foo | awk '{print $2}' | xc  # Copy!
    ~$ xp | grep 'foo' > bar            # Paste!

## Open files with the right tool

The `gnome-open` program (which has equivalents in every desktop environment I
know of) will open a file just as it would from a graphical file manager. You
can `alias` it to `open`, and pull off neat tricks like `open .` to quickly
bring up your current working directory in a GUI.

## Show the current branch in your prompt

If you're into branching, merging and rebasing your git repositories, you'll
find yourself typing `git branch` way too often. Why not just show it right
there in your prompt?

    :::bash
    ~/projects/foo (master)$

The following function grabs the git branch _if there is one_, and echoes its
name with a preceeding space. This way, you won't even notice this in your
profile until you `cd` into a `git` repo.

    :::bash
    function echo_git_branch {
        git status 2> /dev/null | head -n 1 | grep -o '[^ ]\+$' | sed "s/\(.*\)/ (\1)/"
    }

You can put this in your prompt by exporting `$PS1`. Let's add some color into
the mix while we're at it, so that it never goes unnoticed:

    :::bash
    function set_prompt {
        local RESET="\[\033[00m\]"
        local BLUE="\[\033[1;34m\]"
        local RED="\[\033[1;31m\]"
        local GREEN="\[\033[1;32m\]"

        local USER="${debian_chroot:+($debian_chroot)}${GREEN}\u@\h${RESET}"
        local DIR="${BLUE}\w${RESET}"
        local SYMB="\$ "
        local BRANCH="${RED}\$(echo_git_branch)${RESET}"

        export PS1="${USER}:${DIR}${BRANCH}${SYMB}"
    }

    set_prompt

Customize at will!

## Handle archives uniformly

A recent [xkcd post](http://xkcd.com/1168/) may strike you as both funny and
sad. For whatever reason, `tar`, `7z`, `zip`, `rar` and their bunch all take
different flags and arguments, uplifting quick archive managing into a form of
art.

That is, unless you have `atool` installed. Three simple commands with a uniform
interface across all different archive types: `apack`, `aunpack`, `als`. I don't
need to tell you what each of those does.

The program is available in pretty much every package repository out there. Go
get it and save yourself (and `man`) some headaches!

## Generate passwords, IDs and crypto keys

You could just smash the keyboard and produce a perfectly good alphanumeric
combination, but who does that? Instead, generate a random, secure and legible
sequence using `base64`:

    :::bash
    head -c 24 /dev/urandom | base64

The `head` part just limits the number of bytes read. You can `cat` instead if
you want to see an infinitely scrolling output of sheer cryptographic goodness.

## Serve the current working directory

Writing static html? Want to instantly share a file to a friend on the same
network? Python's got your back:

    :::bash
    alias serve="python -m SimpleHTTPServer"

Now, you can just `serve` from your shell. 5 characters.

## Open up a port to the world

After running the previous trick, you might want your server to reach beyond the
walls of the router. Pick up [localtunnel](http://progrium.com/localtunnel/), a
tool that makes tunneling a one-command affair.

    :::bash
    ~$ serve &
    Serving HTTP on 0.0.0.0 port 8000 ...

    ~$ localtunnel 8000
    Port 8000 is now publicly accessible from http://foo1.localtunnel.com ...

If someone was watching, you can now take off your hat and accept tips.

## Monitor files and directories

The `inotifywait` tool blocks on file events. It's great to pull off a simple
monitor-rebuild cycle. For example:

    :::bash
    ~$ while true; do inotifywait foo/ -re modify; make; done

The `man` page contains all the details you need for extending the techinique.

Note that `inotifywait` will set watches in a potentially slow manner. For more
complex monitoring, you might consider specialized tools like
[watchr](https://github.com/mynyml/watchr).

## Talk to web APIs

The `curl` command can perform most of the tasks you face when testing an API
you just ran across. Let me give you some basic examples:

    :::bash
    # Issue a GET request, stdout the response:
    ~$ curl some.api/things

    # POST a string:
    ~$ curl some.api/things -d 'raw post data'

    # PUT a file:
    ~$ curl -X PUT some.api/things -d @file

    # POST from stdin:
    ~$ foo | curl some.api/things -d @-

    # POST form-encoded parameters:
    ~$ curl some.api/things -d foo=one -d bar=two -d baz=three

Forget API consoles. The full power of your command-line workflow is available
by using `curl`.

## Pretty-print API responses

With the recent explosion of JSON-based web-apis, you might frequently find
yourself struggling to read minified responses to a `curl` command. Once again,
Python's got you covered:

    :::bash
    alias jsont="python -m json.tool"

Pipe json into `jsont`, and rejoice on the readability of well-indented object
notation.

## Clean off background tasks

If you ran `inotifywait`, `serve` and `localtunnel` with `&`; you now have
more jobs in the background than you want to manually terminate. No problem:

    :::bash
    ~$ kill `jobs -p`

That's it. `jobs -p` outputs the `pids` of all background jobs.

## The end

Enough for now. I can't think of anything else. This is a fun subject, though, I
may get back to it with new tricks when I learn any.
