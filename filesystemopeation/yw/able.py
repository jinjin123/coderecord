#!/usr/bin/python
#-*- coding:
import ansible.runner
import sys
reload(sys) 
sys.setdefaultencoding('utf8')

# construct the ansible runner and execute on all hosts
results = ansible.runner.Runner(
pattern='*', forks=10,
module_name='shell', module_args='ansible all -m shell -a date',
).run()

if results is None:
   print "No hosts found"
   sys.exit(1)

#print "UP ***********"
for (hostname, result) in results['contacted'].items():
	if not 'failed' in result:
		try:
			f = open('/root/yw/cmd_return2.txt','a+')
			f.write("UP ***********\r")
			f.write("%s\r" % result['stdout'])
			f.close()
		except:
			f.close()

#print "FAILED *******"
for (hostname, result) in results['contacted'].items():
	if 'failed' in result:
		try:
			f = open('/root/yw/cmd_return2.txt','a+')
			f.write("UP ***********\r")
			f.write("%s\r" % result['msg'])
			f.close()
		except:
			f.close()

#print "DOWN *********"
for (hostname, result) in results['dark'].items():
		try:
			f = open('/root/yw/cmd_return2.txt','a+')
			f.write("DOWN ***********\r")
			f.write( "%s\r" % result)
			f.close()
		except:
			f.close()

"""
try:
	output = commands.getoutput('cat  /root/yw/cmd_return.txt ')
        print output
        self.render('host_cmd.html',**{'result':output})
except:
	pass
"""
