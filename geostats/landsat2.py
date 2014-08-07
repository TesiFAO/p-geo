import urllib2

dict = {
    'username' :'murzilli',
    'password' : 'vlasta83',
    'rememberMe' : 0
}


req = urllib2.Request(url='https://earthexplorer.usgs.gov/login',data="username=murzilli&password=vlasta83")
f = urllib2.urlopen(req)

print "here"

req2 = urllib2.Request("http://earthexplorer.usgs.gov/download/4923/LC81080072014174LGN00/STANDARD/EE?operation=get")
f2 = urllib2.urlopen(req2)
print f2.read()