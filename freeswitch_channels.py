# freeswitch-collectd-plugin - freeswitch_channels.py
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; only version 2 of the License is applicable.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
#
# Authors:
#   Steve Stodola <steve at plytro.com>
#
# About this plugin:
#   This plugin uses collectd's Python plugin to record FreeSWITCH.
#   Based on work by Garret Heaton 
#     https://github.com/powdahound/redis-collectd-plugin
#
# collectd:
#   http://collectd.org
# FreeSWITCH:
#   http://www.freeswitch.org/
# collectd-python:
#   http://collectd.org/documentation/manpages/collectd-python.5.shtml

import re
import collectd

from freeswitchESL import ESL 

FREESWITCH_CONNECT_SUCCESS = 1
FREESWITCH_CONNECT_FAIL = 0

# Host to connect to. Override in config by specifying 'Host'.
FREESWITCH_HOST = 'localhost'

# Port to connect on. Override in config by specifying 'Port'.
FREESWITCH_PORT = 5080

# Password to connect with. Override in config by specifying 'Password'.
FREESWITCH_PASSWORD = 'ClueCon'

# Verbose logging on/off. Override in config by specifying 'Verbose'.
VERBOSE_LOGGING = False

def get_channels():
    """Connect to FreeSWITCH server and get channel count"""
    try:
        conn = ESL.ESLconnection(FREESWITCH_HOST, FREESWITCH_PORT, 
            FREESWITCH_PASSWORD)
        if conn.connected() == FREESWITCH_CONNECT_SUCCESS:
            log_verbose('Connected to FreeSWITCH at %s:%s' 
                % (FREESWITCH_HOST, FREESWITCH_PORT))
        else:
            collectd.error('freeswitch_channels: Error connecting to %s:%d'
                       % (FREESWITCH_HOST, FREESWITCH_PORT))
            return None

    log_verbose('Getting channel count')
    event = conn.api('show', 'channels count')
    num_channels_re = r'\n(?P<chans>\d+) total\.\n'
    reg = re.compile(num_channels_re)
    matches = reg.search(event.getBody())
    return int(matches.group("chans"))

def configure_callback(conf):
    """Receive configuration block"""
    global FREESWITCH_HOST, FREESWITCH_PORT, VERBOSE_LOGGING
    for node in conf.children:
        if node.key == 'Host':
            FREESWITCH_HOST = node.values[0]
        elif node.key == 'Port':
            FREESWITCH_PORT = int(node.values[0])
        elif node.key == 'Password':
            FREESWITCH_PASSWORD = node.values[0]
        elif node.key == 'Verbose':
            VERBOSE_LOGGING = bool(node.values[0])
        else:
            collectd.warning('freeswitch_channels: Unknown config key: %s.'
                             % node.key)
    log_verbose('Configured with host=%s, port=%s' 
        % (FREESWITCH_HOST, FREESWITCH_PORT))

def read_channels():
    log_verbose('Read callback called')
    channels = get_channels()

    if not channels:
        collectd.error('freeswitch channels: No info received')
        return

    log_verbose('Sending value: %s=%s' % ("active_channels", channels))

    val = collectd.Values(plugin='freeswitch_channels', type='gauge')
    val.dispatch(values=channels)

def log_verbose(msg):
    if not VERBOSE_LOGGING:
        return
    collectd.info('freeswitch channels [verbose]: %s' % msg)

# register callbacks
collectd.register_config(configure_callback)
collectd.register_read(read_channels)
