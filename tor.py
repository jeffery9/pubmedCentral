import urllib2
# using TOR !
proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"} )
opener = urllib2.build_opener(proxy_support)
urllib2.install_opener(opener)
# every urlopen connection will then use the TOR proxy like this one :
urllib2.urlopen('http://www.google.fr').read()
# and to renew my route when i need to change the IP :
print "Renewing tor route wait a bit for 5 seconds"
from TorCtl import TorCtl
conn = TorCtl.connect(passphrase="1234")
conn.sendAndRecv('signal newnym\r\n')
conn.close()
import time
time.sleep(5)
print "renewed"
