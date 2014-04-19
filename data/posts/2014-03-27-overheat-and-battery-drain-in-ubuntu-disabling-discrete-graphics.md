title: Overheat and Battery Drain in Ubuntu: disabling Discrete Graphics
date: 2014-03-27

A common problem with open source video drivers, specially on the ATI side of
the spectrum, is constant overheat, noisy fans, and battery drain.

The closed source drivers, on the other hand, are not all-around better. They
solve problems, but bring about different ones.

A quick and dirty solution for those that have a sufficiently powerful on-board
graphics card for everyday usage, is to disable the secondary, discrete card.


# Disabling discrete graphics

There's a special file in `sys` that can be used to immediately switch off
the secondary video card.

    :::bash
    echo OFF > /sys/kernel/debug/vgaswitcheroo/switch

Putting the line in `/etc/rc.local` will disable discrete graphics on startup.
Nice and simple.


# Fixing the sleep/wake-up freeze

Resuming the system with discrete graphics already disabled can cause issues
such as black screens or frozen systems.

The obvious way out is to re-enable the secondary card before suspension, and bring it back down after wake-up. This can be easily accomplished by adding a sleep hook in `/etc/pm/sleep.d`.

Create a file named, for example, `11_vgaswitcheroo`:

    :::bash
    #!/bin/bash

    PATH=/bin:/usr/bin
    switchfile=/sys/kernel/debug/vgaswitcheroo/switch

    exitcode=0

    case "$1" in
        hibernate|suspend)
            echo ON > $switchfile
            exitcode=$?
        ;;

        resume|thaw)
            echo OFF > $switchfile
            exitcode=$?
        ;;
    esac

    exit $exitcode
