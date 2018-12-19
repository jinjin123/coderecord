#!/usr/bin/env python
# -*- coding:utf-8 -*-

import ansible
from ansible.playbook import PlayBook
from ansible.inventory import Inventory
from ansible import callbacks
from ansible import utils
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
stats = callbacks.AggregateStats()
runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)
playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
ansible_command = "/usr/local/bin/ansible-playbook -f 10"

def ansible_playbook(playbook,host):
  pb = PlayBook(
    playbook=playbook, 
    callbacks = playbook_cb,
    runner_callbacks = runner_cb,
    stats = stats,
    extra_vars = {'host':host}
  )
  return pb.run()

if __name__ == "__main__": 
  ansible_playbook(sys.argv[1],sys.argv[2])
