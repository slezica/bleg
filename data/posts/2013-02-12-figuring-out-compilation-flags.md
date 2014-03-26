title: Figuring out Compilation Flags
date: 2013-02-12

I've spent endless time over the years digging up correct compilation flags from
manuals and google results. I decided to learn, once and for all, how to obtain
them from my system.

Turns out, the `pkg-config` utility can be made to print `--cflags` and/or
`--libs` (link flags) painlessly:

    :::bash
    ~$ pkg-config --cflags --libs sdl
    -D_GNU_SOURCE=1 -D_REENTRANT -I/usr/include/SDL  -lSDL

Moreover, to list all available options (if autocompletion is available, you
probably can get this far by pressing tab), just locate the `.pc` files
`pkg-config` uses.

    :::bash
    ~$ locate --regex pkgconfig/.*pc$

The `PKG_CONFIG_PATH` environment variable can also be examined if needed.
