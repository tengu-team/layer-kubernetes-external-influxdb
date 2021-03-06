#!/usr/bin/env python3
# Copyright (C) 2017  Ghent University
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
from charmhelpers.core import hookenv, unitdata
from charmhelpers.core.hookenv import status_set, log
from charms.reactive import when, when_not, set_state, remove_state
from charms.layer.externalservicehelpers import configure_headless_service


@when('influxdb.available')
@when_not('k8s-external-influxdb.requested')
def set_up(influxdb):
    log("Setting up influxdb request")
    connection_info = {
        'hostname': influxdb.hostname,
        'port': influxdb.port
    }
    if all(connection_info.values()):
        configure_headless_service(ips=[connection_info['hostname']()],
                                   port=connection_info['port']())
        set_state('k8s-external-influxdb.requested')


@when('influxdb-service.available', 'kubernetes-deployer.available')
def service_requested(relation, deployer):
    log("Sending service_name if possible")
    relation.send_service_name(unitdata.kv().get('service_name', ''))


@when('influxdb-service.available')
@when_not('kubernetes-deployer.available')
def service_requested(relation):
    log("Sending empty service_name")
    relation.send_service_name('')
