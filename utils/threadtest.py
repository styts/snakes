import os
import re
import time
import sys
from threading import Thread

class testit(Thread):
   def __init__ (self,ip):
      Thread.__init__(self)
      self.ip = ip
      self.status = -1
   def run(self):
      pingaling = os.popen("ping "+self.ip,"r")
      while 1:
        line = pingaling.readline()
        if not line: break
        igot = re.findall(testit.lifeline,line)
        if igot:
           self.status = int(igot[0])

testit.lifeline = re.compile(r"(\d) received")
report = ("No response","Partial Response","Alive")

print time.ctime()

pinglist = []

for host in range(-2,10):
   ip = "192.168.1."+str(host)
   current = testit(ip)
   pinglist.append(current)
   current.start()

for pingle in pinglist:
   pingle.join()
   print "Status from ",pingle.ip,"is",report[pingle.status]

print time.ctime()