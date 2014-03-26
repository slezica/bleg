title: GNU Units conversion
date: 2013-02-13

I just discovered a wonderful specimen in my `/usr/bin` bitpond. `units`
performs unit conversion with the added nicety of reporting both the direct and
inverse relation between the quantities.

Behold:

    :::bash
    ~$ units '1 kilometer' meters
        * 1000
        / 0.001

    ~$ units '1 day' seconds
        * 86400
        / 1.1574074e-05

    ~$ units '10 ohms'
        Definition: 10 kg m^2 / A^2 s^3

    ~$ units '10 newton' kg
    conformability error
        10 kg m / s^2
        1 kg

Smart beast!
