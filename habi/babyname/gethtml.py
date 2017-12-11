import urllib.request
import sys

'''
获取远程html
'''
req = urllib.request.Request('http://m.hmz.com/xmcs/%B3%C2_%CB%BC%D9%A4_%B9%AB%C0%FA%202018%C4%EA1%D4%C28%C8%D51%CA%B1_%C4%D0/?from=singlemessage&isappinstalled=0')
response = urllib.request.urlopen(req)
the_page = response.read()

local_code = sys.getfilesystemencoding()
print(local_code)

print(the_page)
print(the_page.decode('gbk'))

