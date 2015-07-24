# -*- coding: utf-8 -*-
# Project server.pyportal
from __future__ import unicode_literals

__author__ = 'alexeyymnaikin'

# Списки эквивалентности доменов, используются для схлопывания ns/mx
eq_domains = {
    'google.com': 'googlemail.com',
    'timeweb.ru': 'timeweb.org',

    # The Secondary (Slave) Domain Name System (DNS) Server of Itlibitum, Corp.
    'primary.su': 'secondary.su',
    # Hetzner Online AG DNS Service
    'first-ns.de': 'second-ns.de',
    'second-ns.de': 'second-ns.com'
}