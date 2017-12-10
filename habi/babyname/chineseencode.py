from urllib.parse import urlencode, quote_plus, quote

'''
陈_思伽_公历 2018年1月8日1时_男 urlencode
%B3%C2_%CB%BC%D9%A4_%B9%AB%C0%FA%202018%C4%EA1%D4%C28%C8%D51%CA%B1_%C4%D0
'''
in_word =  '思'
str_from = '陈_'+in_word+'伽_公历 2018年1月8日1时_男'

print(str_from)

str_encode = quote(str_from.encode('gbk'))
print(str_encode)


'''
http://m.hmz.com/xmcs/%B3%C2_%CB%BC%D9%A4_%B9%AB%C0%FA%202018%C4%EA1%D4%C28%C8%D51%CA%B1_%C4%D0/?from=singlemessage&isappinstalled=0
http://m.hmz.com/xmcs/陈_思伽_公历 2018年1月8日1时_男/?from=singlemessage&isappinstalled=0
'''

url_to = 'http://m.hmz.com/xmcs/' + str_encode + '/?from=singlemessage&isappinstalled=0'
print(url_to)

