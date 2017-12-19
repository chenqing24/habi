# coding=gbk
from bs4 import BeautifulSoup
from urllib.parse import urlencode, quote_plus, quote
import os
import urllib.request
import sys
import time, threading
import pygame

'''
�������ֵ�
'''
print(os.path.abspath('.'))

dict_zi = {}
set_zi = []


def dict2list(dic:dict):
    '''
    ���ֵ�ת��Ϊ�б�
    :param dic:
    :return:
    '''
    keys = dic.keys()
    vals = dic.values()
    lst = [(key, val) for key, val in zip(keys, vals)]
    return lst


# with open(os.path.abspath('.') + '\\4s5j_v2.txt', 'r', encoding='utf-8') as f:
with open(os.path.abspath('.') + '\\3500zi.txt', 'r') as f:
    # print(f.read())
    for x in f.read():
        # print(x)
        # print(ord(x))
        x_ord = ord(x)
        if x_ord and (x_ord not in dict_zi):
            if 19968 < x_ord <= 41863:
                dict_zi[x_ord] = x

    # print(sorted(dict2list(dict_zi), key=lambda x:x[0], reverse=False))
    for char in sorted(dict2list(dict_zi), key=lambda x:x[0], reverse=False):
        set_zi.append(char[1])

print(set_zi)
print(len(set_zi))


def analysishtml(html):
    '''
    ������ҳ
    '''
    soup = BeautifulSoup(html, 'lxml')

    # print(soup)

    row_data = {}

    print('============== all html ==============')
    # ����
    younam = soup.find_all(id='youname')[0]['value']
    print(younam)
    row_data['����'] = younam
    print('============== youname ==============')

    # ����������֡���ϰ�������
    tag_data = soup.find_all("div", attrs={'class': 'data'})
    print(tag_data[0].ul.find_all("li")[0].span.text)
    print(tag_data[0].ul.find_all("li")[1].span.text)

    row_data['�����������'] = int(tag_data[0].ul.find_all("li")[0].span.text)
    row_data['��������'] = int(tag_data[0].ul.find_all("li")[1].span.text)
    print('============== ����������֡���ϰ������� ==============')

    '''
    ��֯�������ݣ���,�ŷָ
    ����,�����������,��������,���,�˸�,�ظ�,���,�ܸ�,��������,������,�ɹ���,�˼ʹ�ϵ
    '''

    # <div class="ge_detail"><em ><span class="ji">��</span>��������</em>
    #         <p><strong class="red">�� �� ��</strong>�ɻ������ɹ���չ��������˫�յ������������ȹ̣�ƽ�����������������ֻ����ɵ��Ҹ����١�</p>
    #       </div>
    tagb = soup.find_all("div", attrs={'class': 'ge_detail'})
    # print(tagb)

    for child_cont in tagb:
        text = str(child_cont.em.text)
        print(text)
        if (text.startswith('���')):
            print(child_cont.em.span.text)
            row_data['���'] = child_cont.em.span.text
        if (text.startswith('�˸�')):
            print(child_cont.em.span.text)
            row_data['�˸�'] = child_cont.em.span.text
        if (text.startswith('�ظ�')):
            print(child_cont.em.span.text)
            row_data['�ظ�'] = child_cont.em.span.text
        if (text.startswith('���')):
            print(child_cont.em.span.text)
            row_data['���'] = child_cont.em.span.text
        if (text.startswith('�ܸ�')):
            print(child_cont.em.span.text)
            row_data['�ܸ�'] = child_cont.em.span.text
        if (text.endswith('��������')):
            print(child_cont.em.span.text)
            row_data['��������'] = child_cont.em.span.text
        if (text.endswith('�����˵�Ӱ��')):
            print(child_cont.em.span.text)
            row_data['������'] = child_cont.em.span.text
        if (text.endswith('�ɹ��˵�Ӱ��')):
            print(child_cont.em.span.text)
            row_data['�ɹ���'] = child_cont.em.span.text
        if (text.endswith('�˼ʹ�ϵ��Ӱ��')):
            print(child_cont.em.span.text)
            row_data['�˼ʹ�ϵ'] = child_cont.em.span.text
            print('============================================')

    print(row_data)
    return row_data


def gethtml(url):
    '''
    ��ȡԶ��html
    '''
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    the_page = response.read()

    local_code = sys.getfilesystemencoding()
    print(local_code)

    # print(the_page)
    # print(the_page.decode('gbk'))
    return the_page.decode('gbk')


'''
Ŀ��urlȷ��
��_˼٤_���� 2018��1��8��1ʱ_�� urlencode
%B3%C2_%CB%BC%D9%A4_%B9%AB%C0%FA%202018%C4%EA1%D4%C28%C8%D51%CA%B1_%C4%D0
'''
i = 0

# start time
start_time = time.gmtime(time.time())


def wirte_csv(all_data, word):
    with open(os.path.abspath('.') + '\\result_' + word + '.csv', 'w+', encoding='gbk') as f:
        f.write('����,�����������,��������,���,�˸�,�ظ�,���,�ܸ�,��������,������,�ɹ���,�˼ʹ�ϵ\n')
        for row in all_data:
            print(row)
            f.write(row['����'])
            f.write(',' + str(row['�����������']))
            f.write(',' + str(row['��������']))
            f.write(',' + row['���'])
            f.write(',' + row['�˸�'])
            f.write(',' + row['�ظ�'])
            f.write(',' + row['���'])
            f.write(',' + row['�ܸ�'])
            f.write(',' + row['��������'])
            f.write(',' + row['������'])
            f.write(',' + row['�ɹ���'])
            f.write(',' + row['�ɹ���'] + '\n')




for in_word in set_zi:
    i += 1
    all_data = []
    # # TODO �����ڼ䣬ֻ��ǰn��
    if i % 100 == 0:
        print('=========== ' + str(i))

    write_flg = False
    for out_word in set_zi:
        # ����
        str_from = '��_' + out_word + in_word + '_���� 2018��1��8��1ʱ_��'
        print(str_from)
        str_encode = quote(str_from.encode('gbk'))
        # print(str_encode)
        '''
        http://m.hmz.com/xmcs/%B3%C2_%CB%BC%D9%A4_%B9%AB%C0%FA%202018%C4%EA1%D4%C28%C8%D51%CA%B1_%C4%D0/?from=singlemessage&isappinstalled=0
        http://m.hmz.com/xmcs/��_˼٤_���� 2018��1��8��1ʱ_��/?from=singlemessage&isappinstalled=0
        '''
        url_to = 'http://m.hmz.com/xmcs/' + str_encode + '/?from=singlemessage&isappinstalled=0'
        print(url_to)
        try:
            html = gethtml(url_to)

            row_data = analysishtml(html)
            all_data.append(row_data)

            if not write_flg:
                if row_data['��������'] == '��':
                    write_flg = True
        except Exception as e:
            print(e)
            continue

    # ��������м������ļ����
    if write_flg:
        wirte_csv(all_data=all_data, word=in_word)
        file = os.path.abspath('.') + '\\faded.mp3'

        pygame.mixer.init()

        track = pygame.mixer.music.load(file)
        pygame.mixer.music.play()

        time.sleep(10)
        pygame.mixer.music.stop()


end_time =  time.gmtime(time.time())

print('============ start time' + str(start_time))
print('============ end time' + str(end_time))





html =r'''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
<title>��˼٤�������Դ��,��˼٤��������-��������</title>
<meta name="keywords" content="�������Դ��,�����ֲ��Դ��,�����ִ������" />
<meta name="description" content="�����������ݴ�ͳ����������������������Ϊ���ṩ��׼���������Դ�֣������ִ�֣��������ֲ��Դ�ַ������������ѧ�Ƕ�֪����һ��������˥.�������.���飬��ҵ�����������ˣ���Ů�������һ���߷ֵĺ����ֽ�����һ����" />
<meta charset="gbk" />
<meta name="format-detection" content="telephone=no">
<meta name="viewport" content="initial-scale=1.0, user-scalable=0, minimum-scale=1.0, maximum-scale=1.0">
<meta name="apple-mobile-web-app-status-bar-style" content="black" />
<meta name="apple-mobile-web-app-title" content="������">
<meta name="apple-mobile-web-app-capable" content="yes">
<link rel="stylesheet" href="/static/css/public.css" />
<link rel="stylesheet" href="/static/css/index.css" />
<link rel="stylesheet" href="/static/css/mobiscroll.custom-2.14.4.min.css" />
<script type="text/javascript" src="/webstatic/js/jquery.min.js"></script>
<script type="text/javascript" src="/static/js/global.js"></script>
<script type="text/javascript" src="/webstatic/js/calendar.js"></script>
<script type="text/javascript" src="/static/js/mobiscroll-2.14.4.js"></script>
<script type="text/javascript" src="/static/js/solar-moni.js"></script>
<script type="text/javascript" src="/static/js/myads.js"></script>
<style>
body { background: #fcf8f5 url(/static/images/syst/bg2.jpg) no-repeat scroll 0 0; background-size:100%;}
</style>
</head>

<body>
<div class="wrapper result_page">
<div class="brother_left">
<div class="header">
  <div class="hide_nav"><a href="javascript:void(0);"></a></div>
  <div class="logo"><a href="/"></a></div>
  <div class="back_up"><a href="javascript:history.go(-1);"></a></div>
</div>
<div class="nav">
  <ul>
    <li><a href="/">��ҳ</a><span></span></li>
    <li><a href="/qiming/">����</a><span></span></li>
    <li><a href="/suanming/">����</a><span></span></li>
    <li><a href="/fengshui/">��ˮ</a><span></span></li>
    <li><a href="/xiangxue/">��ѧ</a></li>
    <li><a href="/shiershengxiao/">��Ф</a><span></span></li>
    <li><a href="/zhouyi/">����</a><span></span></li>
    <li><a href="/huangli/">����</a><span></span></li>
    <li><a href="/jiemeng/">����</a><span></span></li>
    <li><a href="/app/" class="nav_app"><i class="app_icon"></i>Ӧ��</a></li>
    <div class="z"></div>
  </ul>
</div><a class="qm_banner" href="http://qm.hmz.com/"><img src="/static/images/qm_banner.gif" /></a>


    <div class="center">
    
    <div class="xmcs">
	<form id="login" name="login" method="post" action="/xmcs/xmjg/">
      <div class="xmcs_top">
        <div class="x_right"><span class="sex1 sexbtn on" onclick="selbtn('.sexbtn',this,'on','��','sex');">��</span><span class="sex2 sexbtn" onclick="selbtn('.sexbtn',this,'on','Ů','sex');">Ů</span><input type="hidden" id="sex" name="sex" value="��" /></div>
        <div class="x_left">����:</div>
        <div class="x_mid">
          <input class="xmcs_txt" type="text" id="youname" name="youname" value="��˼٤" onfocus="if(value==defaultValue){value='';}" onblur="if(!value){value=defaultValue;}" onkeydown="keydown(event, 'xmcs')">
        </div>
      </div>
      <div class="xmcs_bom">
        <div class="x_right">
          <input class="xmcs_btn" type="button" value="����" onclick="return xmcsCheck();">
        </div>
        <div class="x_left">����:</div>
        <div class="x_mid">
          <input class="xmcs_txt" type="text" id="birthday" name="birthday" value="���� 2018��1��8��1ʱ"  readonly="readonly">
        </div>
      </div>
	</form>
    </div>
    
    
    
      <div class="name">
        <ul>
			<li><span>��</span><i class="huo">��</i></li>
									<li><span>˼</span><i class="jin">��</i></li>
									<li><span>٤</span><i class="mu">ľ</i></li>
			        </ul>
      </div>
      <div class="data">
        <ul>
          <li><strong>��������������֣�</strong><span class="redred">93</span><a href="http://qm.hmz.com/" class="qm_icon2"></a></li>
          <li><strong>������ϰ������֣�</strong><span class="redred">93</span></li>
          <li class="ption"><span>�����ڹ�Ԫ<strong>2018</strong>�� <strong>1</strong>��<strong>8</strong>��<strong> 1 </strong>�� (ũ��2017�궬 �� إ���� ʱ)�����֧Ϊ���� ����������<span class="red">��</span>��ȱ<span>ľ</span>���������Ϊ<strong>����</strong>������<strong>��</strong>�£�ϲ����Ϊ��<strong>ˮ</strong>��<strong>ľ</strong>��</span></li>
          <li><strong>���֣�</strong><span>����	���	����	����</span></li>
          <li><strong>���У�</strong><span>���	ˮ��	��ˮ	����</span></li>
          <li><strong>���壺</strong><span>�    ˼  ٤</span></li>
          <li><strong>ƴ����</strong><span>chen  si ga</span></li>
          <li><strong>���У�</strong><span>��    ��  ľ</span></li>
          <li><strong>���ף�</strong><span class="red">��    ��  ��</span></li>
          <li><strong>�ʻ���</strong><span>16    9  7</span></li>
        </ul>
      </div>
    </div>
    <div class="z"></div>
    <div class="name_list">
      <div class="ge">
        <div class="tg">
          <dl>
            <dt>���-> 17(��)</dt>
            <dd><span style="width:17%;"></span></dd>
          </dl>
        </div>
        <div class="rg">
          <dl>
            <dt>�˸�-> 25(��)</dt>
            <dd><span style="width:25%;"></span></dd>
          </dl>
        </div>
        <div class="dg">
          <dl>
            <dt>�ظ�-> 16(��)</dt>
            <dd><span style="width:16%;"></span></dd>
          </dl>
        </div>
        <div class="wg">
          <dl>
            <dt>���-> 8(��)</dt>
            <dd><span style="width:8%;"></span></dd>
          </dl>
        </div>
        <div class="zg">
          <dl>
            <dt>�ܸ�-> 32(��)</dt>
            <dd><span style="width:32%;"></span></dd>
          </dl>
        </div>
      </div>
      <div class="ge_detail"><em>���17�Ľ���<span class="ping">ƽ</span></em>
        <p>ƽ[��ǿ]Ȩ����ǿ��ͻ�����ѣ��������̣��ػ�ɹ�����������������������ģ����������Ӱ�첻��</p>
      </div>
      <div class="ge_detail"><em>�˸�25�Ľ���<span class="ping">ƽ</span></em>
        <p>ƽ[�ٿ�]����Ӣ�����������أ��˷��������пɳɹ����˸����ֳ����ˣ����������������ĵ㣬Ӱ���˵�һ�����ˡ�</p>
      </div>
      <div class="ge_detail"><em>�ظ�16�Ľ���<span class="ji">��</span></em>
        <p>��[����]�����ص£��������٣��ƹ�˫�����������͡��ظ����ֳ�ǰ�ˣ�Ӱ����������ǰ�Ļ����</p>
      </div>
      <div class="ge_detail"><em>���8�Ľ���<span class="ping">ƽ</span></em>
        <p>ƽ[����֮��]����֮����Ǭ�������������ң������޾��������Ӱ������֮�������</p>
      </div>
      <div class="ge_detail"><em>�ܸ�32�Ľ���<span class="ji">��</span></em>
        <p>��[�����]���Ҷ��������˵������Ʋ���ԣ���������ϡ��ܸ��ֳƺ��ˣ�Ӱ������������������ˡ�</p>
      </div>
      <div class="ge_detail"><em ><span class="ji">��</span>��������</em>
        <p><strong class="red">�� �� ��</strong>�ɻ������ɹ���չ��������˫�յ������������ȹ̣�ƽ�����������������ֻ����ɵ��Ҹ����١�</p>
      </div>
      <div class="ge_detail"><em ><span class="ji">��</span>�Ի����˵�Ӱ��</em>
        <p>�Ը����гٶۣ����أ����׽�Ҳ���뿪���ɹ���Ȼ�ϳ٣������������Ҹ��ġ�</p>
      </div>
      <div class="ge_detail"><em ><span class="ji">��</span>�Գɹ��˵�Ӱ��</em>
        <p>�ɹ�˳������ƽ��˳���شﵽĿ�ġ�</p>
      </div>
      <div class="ge_detail"><em ><span class="ji">��</span>���˼ʹ�ϵ��Ӱ��</em>
        <p>��Ǳ�ڻ�����������Ȩ�ƣ�����ϸ�£�һ���޷���ʰ���������ı�ų��켺���ڸ��Լ��Ĺ�ʧ�������߲����������������⡣</p>
      </div>
      <div class="ge_advice">
        <h5><i class="cyc"></i>�ܵĽ���<i class="cyc"></i></h5>
        <p>���������÷ǳ������ɹ��뾪ϲ��������һ������ǧ��ע�ⲻҪʧȥ�Ͻ��ġ�</p>
      </div>
      <div class="rsfull_btn">
        <input id="birth_input_submit3" class="btn" type="button" value="���¿�ʼ" onclick="javascript:history.go(-1);">
        <h6 class="ps">��������ϵͳ��Դ���й�����ѧ��һЩ���㷽�������ǿ�ѧ�о��ɹ��������������֣��������ţ����˲���һ�к���Ը�����</h6>
      </div>
    </div>
<div><a href="https://zxcs.linghit.com/mllyuncheng/index.html?channel=swhmz" target="_blank"><img src="/static/images/mll_banner.jpg" width="100%" /></a></div>
<div  class="tj_xing">
      <h3>�Ƽ�����<a href="/qmdqjg/%B3%C2/">����</a><a href="http://qm.hmz.com/" class="qm_icon2"></a></h3>
      <ul>
<li><a href="/xmcs/%B3%C2_%C4%C1%C6%E6_%C4%D0/" target="_blank">������</a></li><li><a href="/xmcs/%B3%C2_%B8%EA_%C4%D0/" target="_blank">�¸�</a></li><li><a href="/xmcs/%B3%C2_%C9%DC%C1%AC_%C4%D0/" target="_blank">������</a></li><li><a href="/xmcs/%B3%C2_%C0%F6%B7%BD_%C4%D0/" target="_blank">������</a></li><li><a href="/xmcs/%B3%C2_%BA%C6%C3%FA_%C4%D0/" target="_blank">�º���</a></li><li><a href="/xmcs/%B3%C2_%D6%BE%C3%F4_%C4%D0/" target="_blank">��־��</a></li><li><a href="/xmcs/%B3%C2_%D5%FE%C1%E9_%C4%D0/" target="_blank">������</a></li><li><a href="/xmcs/%B3%C2_%CE%B0%C3%F1_%C4%D0/" target="_blank">��ΰ��</a></li><li><a href="/xmcs/%B3%C2_%C1%E8%EC%D3_%C4%D0/" target="_blank">������</a></li><li><a href="/xmcs/%B3%C2_%C7%EC%C1%C1_%C4%D0/" target="_blank">������</a></li><li><a href="/xmcs/%B3%C2_%CA%B1_%C4%D0/" target="_blank">��ʱ</a></li><li><a href="/xmcs/%B3%C2_%CB%B8%B8%D6_%C4%D0/" target="_blank">��˸��</a></li><li><a href="/xmcs/%B3%C2_%D3%BE%C6%EB_%C4%D0/" target="_blank">��Ӿ��</a></li><li><a href="/xmcs/%B3%C2_%C8%D5%B6%B0_%C4%D0/" target="_blank">���ն�</a></li><li><a href="/xmcs/%B3%C2_%CD%A8%CF%E9_%C4%D0/" target="_blank">��ͨ��</a></li><li><a href="/xmcs/%B3%C2_%CD%A2%C1%E8_%C4%D0/" target="_blank">��͢��</a></li><li><a href="/xmcs/%B3%C2_%D4%C4_%C4%D0/" target="_blank">����</a></li><li><a href="/xmcs/%B3%C2_%D3%C0%C2%A1_%C4%D0/" target="_blank">����¡</a></li><li><a href="/xmcs/%B3%C2_%C5%EF_%C4%D0/" target="_blank">����</a></li><li><a href="/xmcs/%B3%C2_%E3%E5%C7%E0_%C4%D0/" target="_blank">������</a></li><li><a href="/xmcs/%B3%C2_%D0%A5_%C4%D0/" target="_blank">��Х</a></li><li><a href="/xmcs/%B3%C2_%CC%EC%CC%EC_%C4%D0/" target="_blank">������</a></li><li><a href="/xmcs/%B3%C2_%BF%A1%E7%E5_%C4%D0/" target="_blank">�¿���</a></li><li><a href="/xmcs/%B3%C2_%B7%C9_%C4%D0/" target="_blank">�·�</a></li><li><a href="/xmcs/%B3%C2_%C1%AC%D6%D0_%C4%D0/" target="_blank">������</a></li><li><a href="/xmcs/%B3%C2_%D1%E3%BF%A4_%C4%D0/" target="_blank">���㿤</a></li><li><a href="/xmcs/%B3%C2_%BA%E3%C6%E6_%C4%D0/" target="_blank">�º���</a></li><li><a href="/xmcs/%B3%C2_%D7%DA%B9%F3_%C4%D0/" target="_blank">���ڹ�</a></li><li><a href="/xmcs/%B3%C2_%B6%AB%C0%DA_%C4%D0/" target="_blank">�¶���</a></li><li><a href="/xmcs/%B3%C2_%F6%AD%D2%AB_%C4%D0/" target="_blank">����ҫ</a></li><li><a href="/xmcs/%B3%C2_%BE%BC%E9%AA_%C4%D0/" target="_blank">�¾��</a></li><li><a href="/xmcs/%B3%C2_%C2%B6%CC%EF_%C4%D0/" target="_blank">��¶��</a></li><li><a href="/xmcs/%B3%C2_%BC%BE%B7%AB_%C4%D0/" target="_blank">�¼���</a></li><li><a href="/xmcs/%B3%C2_%E3%FC%C3%FA_%C4%D0/" target="_blank">������</a></li><li><a href="/xmcs/%B3%C2_%D2%AB%BA%CA_%C4%D0/" target="_blank">��ҫ��</a></li><li><a href="/xmcs/%B3%C2_%CF%FE%BF%A5_%C4%D0/" target="_blank">������</a></li><li><a href="/xmcs/%B3%C2_%C9%D0%D0%F9_%C4%D0/" target="_blank">������</a></li><li><a href="/xmcs/%B3%C2_%C7%EF%CA%B5_%C4%D0/" target="_blank">����ʵ</a></li><li><a href="/xmcs/%B3%C2_%C7%E5%C7%E0_%C4%D0/" target="_blank">������</a></li>      </ul>
    </div>
<div class="myads ad_5"><script type="text/javascript">setp_ad(5);</script></div>
    <div  class="tj_xing bjx">
      <h3>�ټ�������<a href="/qmdq/">����</a><a href="http://qm.hmz.com/" class="qm_icon2"></a></h3>
      <ul>
<li><a href="/qmdqjg/%C0%EE/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%CD%F5/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%D5%C5/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%C1%F5/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%B3%C2/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%D1%EE/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%D5%D4/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%BB%C6/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%D6%DC/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%CE%E2/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%D0%EC/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%CB%EF/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%BA%FA/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%D6%EC/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%B8%DF/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%C1%D6/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%BA%CE/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%B9%F9/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%C2%ED/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%C2%DE/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%C1%BA/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%CB%CE/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%D6%A3/" title="֣���к����ִ�ȫ">֣</a></li><li><a href="/qmdqjg/%D0%BB/" title="л���к����ִ�ȫ">л</a></li><li><a href="/qmdqjg/%BA%AB/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%CC%C6/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%B7%EB/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%D3%DA/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%B6%AD/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%CF%F4/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%B3%CC/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%B2%F1/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%D4%AC/" title="Ԭ���к����ִ�ȫ">Ԭ</a></li><li><a href="/qmdqjg/%B5%CB/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%D0%ED/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%B8%B5/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%C9%F2/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%D4%F8/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%C5%ED/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%C2%C0/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%CB%D5/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%C2%AC/" title="¬���к����ִ�ȫ">¬</a></li><li><a href="/qmdqjg/%BD%AF/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%B2%CC/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%BC%D6/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%B6%A1/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%CE%BA/" title="κ���к����ִ�ȫ">κ</a></li><li><a href="/qmdqjg/%D1%A6/" title="Ѧ���к����ִ�ȫ">Ѧ</a></li><li><a href="/qmdqjg/%D2%B6/" title="Ҷ���к����ִ�ȫ">Ҷ</a></li><li><a href="/qmdqjg/%D1%D6/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%D3%E0/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%C5%CB/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%B6%C5/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%B4%F7/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%CF%C4/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%D6%D3/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%CD%F4/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%CC%EF/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%C8%CE/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%BD%AA/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%B7%B6/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%B7%BD/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%CA%AF/" title="ʯ���к����ִ�ȫ">ʯ</a></li><li><a href="/qmdqjg/%D2%A6/" title="Ҧ���к����ִ�ȫ">Ҧ</a></li><li><a href="/qmdqjg/%CC%B7/" title="̷���к����ִ�ȫ">̷</a></li><li><a href="/qmdqjg/%C1%CE/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%D7%DE/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%D0%DC/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%BD%F0/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%C2%BD/" title="½���к����ִ�ȫ">½</a></li><li><a href="/qmdqjg/%BA%C2/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%BF%D7/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%B0%D7/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%B4%DE/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%BF%B5/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%C3%AB/" title="ë���к����ִ�ȫ">ë</a></li><li><a href="/qmdqjg/%C7%F1/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%C7%D8/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%BD%AD/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%CA%B7/" title="ʷ���к����ִ�ȫ">ʷ</a></li><li><a href="/qmdqjg/%B9%CB/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%BA%EE/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%C9%DB/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%C3%CF/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%C1%FA/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%CD%F2/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%B6%CE/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%B2%DC/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%C7%AE/" title="Ǯ���к����ִ�ȫ">Ǯ</a></li><li><a href="/qmdqjg/%CC%C0/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%D2%FC/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%C0%E8/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%D2%D7/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%B3%A3/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%CE%E4/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%C7%C7/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%BA%D8/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%C0%B5/" title="�����к����ִ�ȫ">��</a></li><li><a href="/qmdqjg/%B9%A8/" title="�����к����ִ�ȫ">��</a></li>      </ul>
    </div>


<div class="myads ad_9"></div>
<div class="footer">
  <div><strong><a href="http://m.hmz.com">�ֻ���</a></strong><a href="http://www.hmz.com/redirect/">���԰�</a></div>
  <p>&copy; �������� www.hmz.com ��ICP��12050957��-5 <div style="display:none;"><script type="text/javascript" src="/static/js/count.js"></script>
  </div></p>
</div>
<div id="goto_top" class="goto_top">
<a href="javascript:void(0)"></a>
</div></div>

<div class="brother_right">
<ul>
<li class="home"><i class="hd_left_top"></i><i class="hd_right_top"></i><i class="hd_left_bottom"></i><i class="hd_right_bottom"></i><a href="/">��ҳ</a></li>
<li><i class="hd_left_top"></i><i class="hd_right_top"></i><i class="hd_left_bottom"></i><i class="hd_right_bottom"></i>
<a href="/xmcs/">��������</a></li>
<li><i class="hd_left_top"></i><i class="hd_right_top"></i><i class="hd_left_bottom"></i><i class="hd_right_bottom"></i><a href="/bbqm/">��������</a></li>
<li><i class="hd_left_top"></i><i class="hd_right_top"></i><i class="hd_left_bottom"></i><i class="hd_right_bottom"></i><a href="/gsqm/">��˾����</a></li>
<li><i class="hd_left_top"></i><i class="hd_right_top"></i><i class="hd_left_bottom"></i><i class="hd_right_bottom"></i><a href="/gscm/">��˾����</a></li>
<li><i class="hd_left_top"></i><i class="hd_right_top"></i><i class="hd_left_bottom"></i><i class="hd_right_bottom"></i><a href="/bzsm/">��������</a></li>
<li><i class="hd_left_top"></i><i class="hd_right_top"></i><i class="hd_left_bottom"></i><i class="hd_right_bottom"></i><a href="/bzhh/">���ֺϻ�</a></li>
<li><i class="hd_left_top"></i><i class="hd_right_top"></i><i class="hd_left_bottom"></i><i class="hd_right_bottom"></i><a href="/bzpp/">��������</a></li>
<li><i class="hd_left_top"></i><i class="hd_right_top"></i><i class="hd_left_bottom"></i><i class="hd_right_bottom"></i><a href="/huangli/">��������</a></li>
</ul>
<script type="text/javascript">menu_ad();</script></div>
</div>
<script type="text/javascript">
$(function () {
    $('#birthday').mobiscroll().datePicker({
        theme: "ios",
        mode: "scroller",
        display: "bottom",
        lang: "zh",
        isSolar: 1,
        enableSolarLunar: 1,
        showSolarLunar: 0,
        enableIgnore: 0,
        onSelect: function (r, t) { }
    });
	$('#birthday').mobiscroll("setArrayVal", [2018, 1, 8, 1], !1, !1, !1, 0);
});
</script>
</body>
</html>
'''
