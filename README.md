freeswitch-collectd-plugin
==========================

A [FreeSWITCH](http://www.freeswitch.org/) plugin for [collectd](http://collectd.org) using collectd's [Python plugin](http://collectd.org/documentation/manpages/collectd-python.5.shtml).

Data captured includes:

 * Number of active channels

Install
-------
 1. Place freeswitch_channels.py in /opt/collectd/lib/collectd/plugins/python (assuming you have collectd installed to /opt/collectd).
 2. Configure the plugin (see below).
 3. Restart collectd.

Configuration
-------------
Add the following to your collectd config **or** use the included freeswitch.conf.

    <LoadPlugin python>
      Globals true
    </LoadPlugin>
    
    <Plugin python>
      ModulePath "/opt/collectd/lib/collectd/plugins/python"
      Import "freeswitch_channels"
    
      <Module freeswitch_channels>
        Host "localhost"
        Port 8021
        Username "freeswitch"
        Password "works"
        Verbose false
      </Module>
    </Plugin>
