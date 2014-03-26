title: Fixing Bash commands
date: 2013-03-12

Bash provides some editor integration to ease writing of long, complex commands.

1.  <kbd>ctrl</kbd> <kbd>x</kbd> <kbd>ctrl</kbd> <kbd>e</kbd> will bring up an
editor to write a new command. Upon saving and exiting, it gets executed.

2.  Likewise, the `fc` command opens an editor to edit the previous command.

I knew about the keybinding, but I learned of `fc` fairly recently. If you use a
powerful command-line editor, it's game-changing, specially when dealing with
long pipes and/or regular expressions.
