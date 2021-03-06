#
# BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2011 Courgette
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
import logging
import threading
import sys
from b3.config import XmlConfigParser
from b3.fake import FakeConsole
import b3.output # do not remove, needed because the module alters some defaults of the logging module
log = logging.getLogger('output')
log.setLevel(logging.WARNING)

from mock import Mock
import time
import unittest2 as unittest


testcase_lock = threading.Lock() # together with flush_console_streams, helps getting logging output related to the correct
# test in test runners such as the one in PyCharm IDE.

def flush_console_streams():
    sys.stderr.flush()
    sys.stdout.flush()

class B3TestCase(unittest.TestCase):

    def setUp(self):
        testcase_lock.acquire()
        flush_console_streams()

        # create a FakeConsole parser
        self.parser_conf = XmlConfigParser()
        self.parser_conf.loadFromString(r"""<configuration/>""")
        self.console = FakeConsole(self.parser_conf)

        self.console.screen = Mock()
        self.console.time = time.time
        self.console.upTime = Mock(return_value=3)

        self.console.cron.stop()
        
        def myError(msg, *args, **kwargs):
            print(("ERROR: %s" % msg) % args)
        self.console.error = myError

    def tearDown(self):
        flush_console_streams()
        testcase_lock.release()