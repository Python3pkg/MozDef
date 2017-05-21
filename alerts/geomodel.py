#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Copyright (c) 2015 Mozilla Corporation
#
# Contributors:
# Aaron Meihm <ameihm@mozilla.com>

from .lib.alerttask import AlertTask
import pyes

class AlertGeomodel(AlertTask):
    # The minimum event severity we will create an alert for
    MINSEVERITY = 2

    def main(self):
        date_timedelta = dict(minutes=30)

        must = [
            pyes.TermFilter('_type', 'event'),
            pyes.TermFilter('category', 'geomodelnotice'),
        ]
        self.filtersManual(date_timedelta, must=must, must_not=[])
        self.searchEventsSimple()
        self.walkEvents()

    # Set alert properties
    def onEvent(self, event):
        category = 'geomodel'
        tags = ['geomodel']
        severity = 'WARNING'

        ev = event['_source']

        # If the event severity is below what we want, just ignore
        # the event.
        if 'details' not in ev or 'severity' not in ev['details']:
            return None
        if ev['details']['severity'] < self.MINSEVERITY:
            return None

        summary = ev['summary']
        return self.createAlertDict(summary, category, tags, [event], severity)
