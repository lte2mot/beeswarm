# Copyright (C) 2013 Aniket Panse <contact@aniketpanse.in>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Aniket Panse <contact@aniketpanse.in> grants Johnny Vestergaard <jkv@unixcluster.dk>
# a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable
# copyright license to reproduce, prepare derivative works of, publicly
# display, publicly perform, sublicense, relicense, and distribute [the] Contributions
# and such derivative works.


import gevent.monkey

from beeswarm.drones.client.baits import telnet as bee_telnet


gevent.monkey.patch_all()

import unittest
import os
import shutil
import tempfile

from gevent.server import StreamServer
from beeswarm.drones.honeypot.honeypot import Honeypot
from beeswarm.drones.honeypot.capabilities import telnet as honeypot_telnet

from beeswarm.drones.client.models.session import BaitSession


class TelnetTest(unittest.TestCase):
    def setUp(self):
        self.work_dir = tempfile.mkdtemp()
        Honeypot.prepare_environment(self.work_dir)

    def tearDown(self):
        if os.path.isdir(self.work_dir):
            shutil.rmtree(self.work_dir)

    def test_login(self):
        """Tests if the Telnet bait can Login to the Telnet capability"""

        options = {'enabled': 'True', 'port': 0, 'protocol_specific_data': {'max_attempts': 3},
                   'users': {'test': 'test'}}
        cap = honeypot_telnet.Telnet(options, self.work_dir)

        srv = StreamServer(('0.0.0.0', 0), cap.handle_session)
        srv.start()

        bait_info = {
            'timing': 'regular',
            'username': 'test',
            'password': 'test',
            'port': srv.server_port,
            'server': '127.0.0.1'
        }


        BaitSession.client_id = 'f51171df-c8f6-4af4-86c0-f4e163cf69e8'
        current_bee = bee_telnet.Telnet(bait_info)
        current_bee.connect()
        current_bee.login(bait_info['username'], bait_info['password'])
        srv.stop()

    def test_validate_senses(self):

        options = {'enabled': 'True', 'port': 0, 'protocol_specific_data': {'max_attempts': 3},
                   'users': {'test': 'test'}}

        cap = honeypot_telnet.Telnet(options, self.work_dir)
        srv = StreamServer(('0.0.0.0', 0), cap.handle_session)
        srv.start()

        bait_info = {
            'timing': 'regular',
            'username': 'test',
            'password': 'test',
            'port': srv.server_port,
            'server': '127.0.0.1'
        }


        BaitSession.client_id = 'f51171df-c8f6-4af4-86c0-f4e163cf69e8'
        current_bee = bee_telnet.Telnet(bait_info)
        for s in current_bee.senses:
            sense = getattr(current_bee, s)
            self.assertTrue(callable(sense))

    def test_command_cd(self):

        options = {'enabled': 'True', 'port': 0, 'protocol_specific_data': {'max_attempts': 3},
                   'users': {'test': 'test'}}
        cap = honeypot_telnet.Telnet(options, self.work_dir)
        srv = StreamServer(('0.0.0.0', 0), cap.handle_session)
        srv.start()

        bait_info = {
            'timing': 'regular',
            'username': 'test',
            'password': 'test',
            'port': srv.server_port,
            'server': '127.0.0.1'
        }


        BaitSession.client_id = 'f51171df-c8f6-4af4-86c0-f4e163cf69e8'
        current_bait = bee_telnet.Telnet(bait_info)

        current_bait.connect()
        current_bait.login(bait_info['username'], bait_info['password'])

        # Command: cd
        self.assertEquals('/', current_bait.state['working_dir'])
        current_bait.cd('/var')
        self.assertEquals('/var', current_bait.state['working_dir'])

    def test_command_pwd(self):

        options = {'enabled': 'True', 'port': 0, 'protocol_specific_data': {'max_attempts': 3},
                   'users': {'test': 'test'}}

        cap = honeypot_telnet.Telnet(options, self.work_dir)
        srv = StreamServer(('0.0.0.0', 0), cap.handle_session)
        srv.start()

        bait_info = {
            'timing': 'regular',
            'username': 'test',
            'password': 'test',
            'port': srv.server_port,
            'server': '127.0.0.1'
        }


        BaitSession.client_id = 'f51171df-c8f6-4af4-86c0-f4e163cf69e8'
        current_bee = bee_telnet.Telnet(bait_info)

        current_bee.connect()
        current_bee.login(bait_info['username'], bait_info['password'])

        current_bee.cd('/var')
        resp = current_bee.pwd()
        self.assertTrue('/var' in resp)

    def test_command_uname(self):

        options = {'enabled': 'True', 'port': 0, 'protocol_specific_data': {'max_attempts': 3},
                   'users': {'test': 'test'}}

        cap = honeypot_telnet.Telnet(options, self.work_dir)
        srv = StreamServer(('0.0.0.0', 0), cap.handle_session)
        srv.start()

        bait_info = {
            'timing': 'regular',
            'username': 'test',
            'password': 'test',
            'port': srv.server_port,
            'server': '127.0.0.1'
        }


        BaitSession.client_id = 'f51171df-c8f6-4af4-86c0-f4e163cf69e8'
        current_bee = bee_telnet.Telnet(bait_info)

        current_bee.connect()
        current_bee.login(bait_info['username'], bait_info['password'])

        resp1 = current_bee.uname('-o')
        self.assertTrue('GNU/Linux' in resp1)

    def test_command_cat(self):

        options = {'enabled': 'True', 'port': 0, 'protocol_specific_data': {'max_attempts': 3},
                   'users': {'test': 'test'}}

        cap = honeypot_telnet.Telnet(options, self.work_dir)
        srv = StreamServer(('0.0.0.0', 0), cap.handle_session)
        srv.start()

        bait_info = {
            'timing': 'regular',
            'username': 'test',
            'password': 'test',
            'port': srv.server_port,
            'server': '127.0.0.1'
        }


        BaitSession.client_id = 'f51171df-c8f6-4af4-86c0-f4e163cf69e8'
        current_bee = bee_telnet.Telnet(bait_info)

        current_bee.connect()
        current_bee.login(bait_info['username'], bait_info['password'])

        resp = current_bee.cat('/var/www/index.html')
        self.assertTrue('</html>' in resp)

    def test_command_uptime(self):

        options = {'enabled': 'True', 'port': 0, 'protocol_specific_data': {'max_attempts': 3},
                   'users': {'test': 'test'}}

        cap = honeypot_telnet.Telnet(options, self.work_dir)
        srv = StreamServer(('0.0.0.0', 0), cap.handle_session)
        srv.start()

        bait_info = {
            'timing': 'regular',
            'username': 'test',
            'password': 'test',
            'port': srv.server_port,
            'server': '127.0.0.1'
        }


        BaitSession.client_id = 'f51171df-c8f6-4af4-86c0-f4e163cf69e8'
        current_bee = bee_telnet.Telnet(bait_info)

        current_bee.connect()
        current_bee.login(bait_info['username'], bait_info['password'])

        resp = current_bee.uptime('-V')
        self.assertTrue('procps version 3.2.8' in resp)

    def test_command_echo(self):

        options = {'enabled': 'True', 'port': 0, 'protocol_specific_data': {'max_attempts': 3},
                   'users': {'test': 'test'}}

        cap = honeypot_telnet.Telnet(options, self.work_dir)
        srv = StreamServer(('0.0.0.0', 0), cap.handle_session)
        srv.start()

        bait_info = {
            'timing': 'regular',
            'username': 'test',
            'password': 'test',
            'port': srv.server_port,
            'server': '127.0.0.1'
        }


        BaitSession.client_id = 'f51171df-c8f6-4af4-86c0-f4e163cf69e8'
        current_bee = bee_telnet.Telnet(bait_info)

        current_bee.connect()
        current_bee.login(bait_info['username'], bait_info['password'])
        resp = current_bee.echo('just testing!')
        self.assertTrue('just testing!' in resp)

    def test_command_list(self):

        options = {'enabled': 'True', 'port': 0, 'protocol_specific_data': {'max_attempts': 3},
                   'users': {'test': 'test'}}

        cap = honeypot_telnet.Telnet(options, self.work_dir)
        srv = StreamServer(('0.0.0.0', 0), cap.handle_session)
        srv.start()

        bait_info = {
            'timing': 'regular',
            'username': 'test',
            'password': 'test',
            'port': srv.server_port,
            'server': '127.0.0.1',
            'honeypot_id': '1234'
        }


        BaitSession.client_id = 'f51171df-c8f6-4af4-86c0-f4e163cf69e8'
        current_bee = bee_telnet.Telnet(bait_info)

        current_bee.connect()
        current_bee.login(bait_info['username'], bait_info['password'])

        resp = current_bee.ls()
        self.assertTrue('var' in resp)


if __name__ == '__main__':
    unittest.main()
