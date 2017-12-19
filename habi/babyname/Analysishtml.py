# coding=gbk
from bs4 import BeautifulSoup
from urllib.parse import urlencode, quote_plus, quote
import os
import urllib.request
import sys
import time, threading
import pygame

'''
遍历的字典
'''
print(os.path.abspath('.'))

dict_zi = {}
set_zi = []


def dict2list(dic:dict):
    '''
    将字典转化为列表
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
    分析网页
    '''
    soup = BeautifulSoup(html, 'lxml')

    # print(soup)

    row_data = {}

    print('============== all html ==============')
    # 姓名
    younam = soup.find_all(id='youname')[0]['value']
    print(younam)
    row_data['姓名'] = younam
    print('============== youname ==============')

    # 五格数理评分、配合八字评分
    tag_data = soup.find_all("div", attrs={'class': 'data'})
    print(tag_data[0].ul.find_all("li")[0].span.text)
    print(tag_data[0].ul.find_all("li")[1].span.text)

    row_data['五格数理评分'] = int(tag_data[0].ul.find_all("li")[0].span.text)
    row_data['八字评分'] = int(tag_data[0].ul.find_all("li")[1].span.text)
    print('============== 五格数理评分、配合八字评分 ==============')

    '''
    组织单行数据，以,号分割：
    名字,五格数理评分,八字评分,天格,人格,地格,外格,总格,三才配置,基础运,成功运,人际关系
    '''

    # <div class="ge_detail"><em ><span class="ji">吉</span>三才配置</em>
    #         <p><strong class="red">金 土 土</strong>可获得意外成功发展，有名利双收的运气，基础稳固，平静安康，免于种种灾祸，可得幸福长寿。</p>
    #       </div>
    tagb = soup.find_all("div", attrs={'class': 'ge_detail'})
    # print(tagb)

    for child_cont in tagb:
        text = str(child_cont.em.text)
        print(text)
        if (text.startswith('天格')):
            print(child_cont.em.span.text)
            row_data['天格'] = child_cont.em.span.text
        if (text.startswith('人格')):
            print(child_cont.em.span.text)
            row_data['人格'] = child_cont.em.span.text
        if (text.startswith('地格')):
            print(child_cont.em.span.text)
            row_data['地格'] = child_cont.em.span.text
        if (text.startswith('外格')):
            print(child_cont.em.span.text)
            row_data['外格'] = child_cont.em.span.text
        if (text.startswith('总格')):
            print(child_cont.em.span.text)
            row_data['总格'] = child_cont.em.span.text
        if (text.endswith('三才配置')):
            print(child_cont.em.span.text)
            row_data['三才配置'] = child_cont.em.span.text
        if (text.endswith('基础运的影响')):
            print(child_cont.em.span.text)
            row_data['基础运'] = child_cont.em.span.text
        if (text.endswith('成功运的影响')):
            print(child_cont.em.span.text)
            row_data['成功运'] = child_cont.em.span.text
        if (text.endswith('人际关系的影响')):
            print(child_cont.em.span.text)
            row_data['人际关系'] = child_cont.em.span.text
            print('============================================')

    print(row_data)
    return row_data


def gethtml(url):
    '''
    获取远程html
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
目标url确定
陈_思伽_公历 2018年1月8日1时_男 urlencode
%B3%C2_%CB%BC%D9%A4_%B9%AB%C0%FA%202018%C4%EA1%D4%C28%C8%D51%CA%B1_%C4%D0
'''
i = 0

# start time
start_time = time.gmtime(time.time())


def wirte_csv(all_data, word):
    with open(os.path.abspath('.') + '\\result_' + word + '.csv', 'w+', encoding='gbk') as f:
        f.write('名字,五格数理评分,八字评分,天格,人格,地格,外格,总格,三才配置,基础运,成功运,人际关系\n')
        for row in all_data:
            print(row)
            f.write(row['姓名'])
            f.write(',' + str(row['五格数理评分']))
            f.write(',' + str(row['八字评分']))
            f.write(',' + row['天格'])
            f.write(',' + row['人格'])
            f.write(',' + row['地格'])
            f.write(',' + row['外格'])
            f.write(',' + row['总格'])
            f.write(',' + row['三才配置'])
            f.write(',' + row['基础运'])
            f.write(',' + row['成功运'])
            f.write(',' + row['成功运'] + '\n')




for in_word in set_zi:
    i += 1
    all_data = []
    # # TODO 测试期间，只算前n条
    if i % 100 == 0:
        print('=========== ' + str(i))

    write_flg = False
    for out_word in set_zi:
        # 条件
        str_from = '陈_' + out_word + in_word + '_公历 2018年1月8日1时_男'
        print(str_from)
        str_encode = quote(str_from.encode('gbk'))
        # print(str_encode)
        '''
        http://m.hmz.com/xmcs/%B3%C2_%CB%BC%D9%A4_%B9%AB%C0%FA%202018%C4%EA1%D4%C28%C8%D51%CA%B1_%C4%D0/?from=singlemessage&isappinstalled=0
        http://m.hmz.com/xmcs/陈_思伽_公历 2018年1月8日1时_男/?from=singlemessage&isappinstalled=0
        '''
        url_to = 'http://m.hmz.com/xmcs/' + str_encode + '/?from=singlemessage&isappinstalled=0'
        print(url_to)
        try:
            html = gethtml(url_to)

            row_data = analysishtml(html)
            all_data.append(row_data)

            if not write_flg:
                if row_data['三才配置'] == '吉':
                    write_flg = True
        except Exception as e:
            print(e)
            continue

    # 如果三才有吉，该文件输出
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
<title>陈思伽姓名测试打分,陈思伽姓名测试-好名字网</title>
<meta name="keywords" content="姓名测试打分,起名字测试打分,测名字打分算命" />
<meta name="description" content="好名字网根据传统周易数理和三才五格起名法为你提供精准的姓名测试打分，测名字打分，宝宝名字测试打分服务，让你从姓名学角度知道你一生荣辱兴衰.富贵祸福.爱情，事业，婚姻，财运，子女等情况，一个高分的好名字将伴你一生。" />
<meta charset="gbk" />
<meta name="format-detection" content="telephone=no">
<meta name="viewport" content="initial-scale=1.0, user-scalable=0, minimum-scale=1.0, maximum-scale=1.0">
<meta name="apple-mobile-web-app-status-bar-style" content="black" />
<meta name="apple-mobile-web-app-title" content="好名字">
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
    <li><a href="/">首页</a><span></span></li>
    <li><a href="/qiming/">起名</a><span></span></li>
    <li><a href="/suanming/">算命</a><span></span></li>
    <li><a href="/fengshui/">风水</a><span></span></li>
    <li><a href="/xiangxue/">相学</a></li>
    <li><a href="/shiershengxiao/">生肖</a><span></span></li>
    <li><a href="/zhouyi/">周易</a><span></span></li>
    <li><a href="/huangli/">黄历</a><span></span></li>
    <li><a href="/jiemeng/">解梦</a><span></span></li>
    <li><a href="/app/" class="nav_app"><i class="app_icon"></i>应用</a></li>
    <div class="z"></div>
  </ul>
</div><a class="qm_banner" href="http://qm.hmz.com/"><img src="/static/images/qm_banner.gif" /></a>


    <div class="center">
    
    <div class="xmcs">
	<form id="login" name="login" method="post" action="/xmcs/xmjg/">
      <div class="xmcs_top">
        <div class="x_right"><span class="sex1 sexbtn on" onclick="selbtn('.sexbtn',this,'on','男','sex');">男</span><span class="sex2 sexbtn" onclick="selbtn('.sexbtn',this,'on','女','sex');">女</span><input type="hidden" id="sex" name="sex" value="男" /></div>
        <div class="x_left">姓名:</div>
        <div class="x_mid">
          <input class="xmcs_txt" type="text" id="youname" name="youname" value="陈思伽" onfocus="if(value==defaultValue){value='';}" onblur="if(!value){value=defaultValue;}" onkeydown="keydown(event, 'xmcs')">
        </div>
      </div>
      <div class="xmcs_bom">
        <div class="x_right">
          <input class="xmcs_btn" type="button" value="测名" onclick="return xmcsCheck();">
        </div>
        <div class="x_left">生日:</div>
        <div class="x_mid">
          <input class="xmcs_txt" type="text" id="birthday" name="birthday" value="公历 2018年1月8日1时"  readonly="readonly">
        </div>
      </div>
	</form>
    </div>
    
    
    
      <div class="name">
        <ul>
			<li><span>陈</span><i class="huo">火</i></li>
									<li><span>思</span><i class="jin">金</i></li>
									<li><span>伽</span><i class="mu">木</i></li>
			        </ul>
      </div>
      <div class="data">
        <ul>
          <li><strong>姓名五格数理评分：</strong><span class="redred">93</span><a href="http://qm.hmz.com/" class="qm_icon2"></a></li>
          <li><strong>姓名配合八字评分：</strong><span class="redred">93</span></li>
          <li class="ption"><span>您生于公元<strong>2018</strong>年 <strong>1</strong>月<strong>8</strong>日<strong> 1 </strong>点 (农历2017年冬 月 廿二丑 时)，年干支为丁酉 ，此命五行<span class="red">火</span>旺缺<span>木</span>；日主天干为<strong>庚金</strong>，生于<strong>丑</strong>月；喜用神为：<strong>水</strong>，<strong>木</strong>。</span></li>
          <li><strong>八字：</strong><span>丁酉	癸丑	庚子	丁丑</span></li>
          <li><strong>五行：</strong><span>火金	水土	金水	火土</span></li>
          <li><strong>繁体：</strong><span>陳    思  伽</span></li>
          <li><strong>拼音：</strong><span>chen  si ga</span></li>
          <li><strong>五行：</strong><span>火    金  木</span></li>
          <li><strong>吉凶：</strong><span class="red">吉    吉  吉</span></li>
          <li><strong>笔划：</strong><span>16    9  7</span></li>
        </ul>
      </div>
    </div>
    <div class="z"></div>
    <div class="name_list">
      <div class="ge">
        <div class="tg">
          <dl>
            <dt>天格-> 17(金)</dt>
            <dd><span style="width:17%;"></span></dd>
          </dl>
        </div>
        <div class="rg">
          <dl>
            <dt>人格-> 25(土)</dt>
            <dd><span style="width:25%;"></span></dd>
          </dl>
        </div>
        <div class="dg">
          <dl>
            <dt>地格-> 16(土)</dt>
            <dd><span style="width:16%;"></span></dd>
          </dl>
        </div>
        <div class="wg">
          <dl>
            <dt>外格-> 8(金)</dt>
            <dd><span style="width:8%;"></span></dd>
          </dl>
        </div>
        <div class="zg">
          <dl>
            <dt>总格-> 32(火)</dt>
            <dd><span style="width:32%;"></span></dd>
          </dl>
        </div>
      </div>
      <div class="ge_detail"><em>天格17的解析<span class="ping">平</span></em>
        <p>平[刚强]权威刚强，突破万难，如能容忍，必获成功。天格数是先祖留传下来的，其数理对人影响不。</p>
      </div>
      <div class="ge_detail"><em>人格25的解析<span class="ping">平</span></em>
        <p>平[荣俊]资性英敏，才能奇特，克服傲慢，尚可成功。人格数又称主运，是整个姓名的中心点，影响人的一生命运。</p>
      </div>
      <div class="ge_detail"><em>地格16的解析<span class="ji">吉</span></em>
        <p>吉[厚重]厚重载德，安富尊荣，财官双美，功成名就。地格数又称前运，影响人中年以前的活动力。</p>
      </div>
      <div class="ge_detail"><em>外格8的解析<span class="ping">平</span></em>
        <p>平[八卦之数]八卦之数，乾坎艮震，巽离坤兑，无穷无尽。外格数影响命运之灵活力。</p>
      </div>
      <div class="ge_detail"><em>总格32的解析<span class="ji">吉</span></em>
        <p>吉[宝马金鞍]侥幸多望，贵人得助，财帛如裕，繁荣至上。总格又称后运，影响人中年至晚年的命运。</p>
      </div>
      <div class="ge_detail"><em ><span class="ji">吉</span>三才配置</em>
        <p><strong class="red">金 土 土</strong>可获得意外成功发展，有名利双收的运气，基础稳固，平静安康，免于种种灾祸，可得幸福长寿。</p>
      </div>
      <div class="ge_detail"><em ><span class="ji">吉</span>对基础运的影响</em>
        <p>性格稍有迟钝，稳重，易亲近也易离开，成功虽然较迟，但总体上是幸福的。</p>
      </div>
      <div class="ge_detail"><em ><span class="ji">吉</span>对成功运的影响</em>
        <p>成功顺利，能平安顺利地达到目的。</p>
      </div>
      <div class="ge_detail"><em ><span class="ji">吉</span>对人际关系的影响</em>
        <p>有潜在活力，不屈于权势；讨厌细事，一见无法收拾，会想出阴谋排除异己，掩盖自己的过失。数吉者步步高升，事事如意。</p>
      </div>
      <div class="ge_advice">
        <h5><i class="cyc"></i>总的建议<i class="cyc"></i></h5>
        <p>你的名字起得非常棒，成功与惊喜会伴随你的一生。但千万注意不要失去上进心。</p>
      </div>
      <div class="rsfull_btn">
        <input id="birth_input_submit3" class="btn" type="button" value="重新开始" onclick="javascript:history.go(-1);">
        <h6 class="ps">（本算命系统来源于中国民俗学的一些测算方法，并非科学研究成果，仅供休闲娱乐，请勿迷信，按此操作一切后果自负！）</h6>
      </div>
    </div>
<div><a href="https://zxcs.linghit.com/mllyuncheng/index.html?channel=swhmz" target="_blank"><img src="/static/images/mll_banner.jpg" width="100%" /></a></div>
<div  class="tj_xing">
      <h3>推荐名字<a href="/qmdqjg/%B3%C2/">更多</a><a href="http://qm.hmz.com/" class="qm_icon2"></a></h3>
      <ul>
<li><a href="/xmcs/%B3%C2_%C4%C1%C6%E6_%C4%D0/" target="_blank">陈牧奇</a></li><li><a href="/xmcs/%B3%C2_%B8%EA_%C4%D0/" target="_blank">陈戈</a></li><li><a href="/xmcs/%B3%C2_%C9%DC%C1%AC_%C4%D0/" target="_blank">陈绍连</a></li><li><a href="/xmcs/%B3%C2_%C0%F6%B7%BD_%C4%D0/" target="_blank">陈丽方</a></li><li><a href="/xmcs/%B3%C2_%BA%C6%C3%FA_%C4%D0/" target="_blank">陈浩铭</a></li><li><a href="/xmcs/%B3%C2_%D6%BE%C3%F4_%C4%D0/" target="_blank">陈志敏</a></li><li><a href="/xmcs/%B3%C2_%D5%FE%C1%E9_%C4%D0/" target="_blank">陈政灵</a></li><li><a href="/xmcs/%B3%C2_%CE%B0%C3%F1_%C4%D0/" target="_blank">陈伟民</a></li><li><a href="/xmcs/%B3%C2_%C1%E8%EC%D3_%C4%D0/" target="_blank">陈凌煊</a></li><li><a href="/xmcs/%B3%C2_%C7%EC%C1%C1_%C4%D0/" target="_blank">陈庆亮</a></li><li><a href="/xmcs/%B3%C2_%CA%B1_%C4%D0/" target="_blank">陈时</a></li><li><a href="/xmcs/%B3%C2_%CB%B8%B8%D6_%C4%D0/" target="_blank">陈烁钢</a></li><li><a href="/xmcs/%B3%C2_%D3%BE%C6%EB_%C4%D0/" target="_blank">陈泳齐</a></li><li><a href="/xmcs/%B3%C2_%C8%D5%B6%B0_%C4%D0/" target="_blank">陈日栋</a></li><li><a href="/xmcs/%B3%C2_%CD%A8%CF%E9_%C4%D0/" target="_blank">陈通祥</a></li><li><a href="/xmcs/%B3%C2_%CD%A2%C1%E8_%C4%D0/" target="_blank">陈廷凌</a></li><li><a href="/xmcs/%B3%C2_%D4%C4_%C4%D0/" target="_blank">陈阅</a></li><li><a href="/xmcs/%B3%C2_%D3%C0%C2%A1_%C4%D0/" target="_blank">陈永隆</a></li><li><a href="/xmcs/%B3%C2_%C5%EF_%C4%D0/" target="_blank">陈棚</a></li><li><a href="/xmcs/%B3%C2_%E3%E5%C7%E0_%C4%D0/" target="_blank">陈沐青</a></li><li><a href="/xmcs/%B3%C2_%D0%A5_%C4%D0/" target="_blank">陈啸</a></li><li><a href="/xmcs/%B3%C2_%CC%EC%CC%EC_%C4%D0/" target="_blank">陈天天</a></li><li><a href="/xmcs/%B3%C2_%BF%A1%E7%E5_%C4%D0/" target="_blank">陈俊珏</a></li><li><a href="/xmcs/%B3%C2_%B7%C9_%C4%D0/" target="_blank">陈飞</a></li><li><a href="/xmcs/%B3%C2_%C1%AC%D6%D0_%C4%D0/" target="_blank">陈连中</a></li><li><a href="/xmcs/%B3%C2_%D1%E3%BF%A4_%C4%D0/" target="_blank">陈雁郡</a></li><li><a href="/xmcs/%B3%C2_%BA%E3%C6%E6_%C4%D0/" target="_blank">陈恒奇</a></li><li><a href="/xmcs/%B3%C2_%D7%DA%B9%F3_%C4%D0/" target="_blank">陈宗贵</a></li><li><a href="/xmcs/%B3%C2_%B6%AB%C0%DA_%C4%D0/" target="_blank">陈东磊</a></li><li><a href="/xmcs/%B3%C2_%F6%AD%D2%AB_%C4%D0/" target="_blank">陈霏耀</a></li><li><a href="/xmcs/%B3%C2_%BE%BC%E9%AA_%C4%D0/" target="_blank">陈炯楠</a></li><li><a href="/xmcs/%B3%C2_%C2%B6%CC%EF_%C4%D0/" target="_blank">陈露田</a></li><li><a href="/xmcs/%B3%C2_%BC%BE%B7%AB_%C4%D0/" target="_blank">陈季帆</a></li><li><a href="/xmcs/%B3%C2_%E3%FC%C3%FA_%C4%D0/" target="_blank">陈泓铭</a></li><li><a href="/xmcs/%B3%C2_%D2%AB%BA%CA_%C4%D0/" target="_blank">陈耀菏</a></li><li><a href="/xmcs/%B3%C2_%CF%FE%BF%A5_%C4%D0/" target="_blank">陈晓骏</a></li><li><a href="/xmcs/%B3%C2_%C9%D0%D0%F9_%C4%D0/" target="_blank">陈尚轩</a></li><li><a href="/xmcs/%B3%C2_%C7%EF%CA%B5_%C4%D0/" target="_blank">陈秋实</a></li><li><a href="/xmcs/%B3%C2_%C7%E5%C7%E0_%C4%D0/" target="_blank">陈清青</a></li>      </ul>
    </div>
<div class="myads ad_5"><script type="text/javascript">setp_ad(5);</script></div>
    <div  class="tj_xing bjx">
      <h3>百家姓起名<a href="/qmdq/">更多</a><a href="http://qm.hmz.com/" class="qm_icon2"></a></h3>
      <ul>
<li><a href="/qmdqjg/%C0%EE/" title="李姓男孩名字大全">李</a></li><li><a href="/qmdqjg/%CD%F5/" title="王姓男孩名字大全">王</a></li><li><a href="/qmdqjg/%D5%C5/" title="张姓男孩名字大全">张</a></li><li><a href="/qmdqjg/%C1%F5/" title="刘姓男孩名字大全">刘</a></li><li><a href="/qmdqjg/%B3%C2/" title="陈姓男孩名字大全">陈</a></li><li><a href="/qmdqjg/%D1%EE/" title="杨姓男孩名字大全">杨</a></li><li><a href="/qmdqjg/%D5%D4/" title="赵姓男孩名字大全">赵</a></li><li><a href="/qmdqjg/%BB%C6/" title="黄姓男孩名字大全">黄</a></li><li><a href="/qmdqjg/%D6%DC/" title="周姓男孩名字大全">周</a></li><li><a href="/qmdqjg/%CE%E2/" title="吴姓男孩名字大全">吴</a></li><li><a href="/qmdqjg/%D0%EC/" title="徐姓男孩名字大全">徐</a></li><li><a href="/qmdqjg/%CB%EF/" title="孙姓男孩名字大全">孙</a></li><li><a href="/qmdqjg/%BA%FA/" title="胡姓男孩名字大全">胡</a></li><li><a href="/qmdqjg/%D6%EC/" title="朱姓男孩名字大全">朱</a></li><li><a href="/qmdqjg/%B8%DF/" title="高姓男孩名字大全">高</a></li><li><a href="/qmdqjg/%C1%D6/" title="林姓男孩名字大全">林</a></li><li><a href="/qmdqjg/%BA%CE/" title="何姓男孩名字大全">何</a></li><li><a href="/qmdqjg/%B9%F9/" title="郭姓男孩名字大全">郭</a></li><li><a href="/qmdqjg/%C2%ED/" title="马姓男孩名字大全">马</a></li><li><a href="/qmdqjg/%C2%DE/" title="罗姓男孩名字大全">罗</a></li><li><a href="/qmdqjg/%C1%BA/" title="梁姓男孩名字大全">梁</a></li><li><a href="/qmdqjg/%CB%CE/" title="宋姓男孩名字大全">宋</a></li><li><a href="/qmdqjg/%D6%A3/" title="郑姓男孩名字大全">郑</a></li><li><a href="/qmdqjg/%D0%BB/" title="谢姓男孩名字大全">谢</a></li><li><a href="/qmdqjg/%BA%AB/" title="韩姓男孩名字大全">韩</a></li><li><a href="/qmdqjg/%CC%C6/" title="唐姓男孩名字大全">唐</a></li><li><a href="/qmdqjg/%B7%EB/" title="冯姓男孩名字大全">冯</a></li><li><a href="/qmdqjg/%D3%DA/" title="于姓男孩名字大全">于</a></li><li><a href="/qmdqjg/%B6%AD/" title="董姓男孩名字大全">董</a></li><li><a href="/qmdqjg/%CF%F4/" title="萧姓男孩名字大全">萧</a></li><li><a href="/qmdqjg/%B3%CC/" title="程姓男孩名字大全">程</a></li><li><a href="/qmdqjg/%B2%F1/" title="柴姓男孩名字大全">柴</a></li><li><a href="/qmdqjg/%D4%AC/" title="袁姓男孩名字大全">袁</a></li><li><a href="/qmdqjg/%B5%CB/" title="邓姓男孩名字大全">邓</a></li><li><a href="/qmdqjg/%D0%ED/" title="许姓男孩名字大全">许</a></li><li><a href="/qmdqjg/%B8%B5/" title="傅姓男孩名字大全">傅</a></li><li><a href="/qmdqjg/%C9%F2/" title="沈姓男孩名字大全">沈</a></li><li><a href="/qmdqjg/%D4%F8/" title="曾姓男孩名字大全">曾</a></li><li><a href="/qmdqjg/%C5%ED/" title="彭姓男孩名字大全">彭</a></li><li><a href="/qmdqjg/%C2%C0/" title="吕姓男孩名字大全">吕</a></li><li><a href="/qmdqjg/%CB%D5/" title="苏姓男孩名字大全">苏</a></li><li><a href="/qmdqjg/%C2%AC/" title="卢姓男孩名字大全">卢</a></li><li><a href="/qmdqjg/%BD%AF/" title="蒋姓男孩名字大全">蒋</a></li><li><a href="/qmdqjg/%B2%CC/" title="蔡姓男孩名字大全">蔡</a></li><li><a href="/qmdqjg/%BC%D6/" title="贾姓男孩名字大全">贾</a></li><li><a href="/qmdqjg/%B6%A1/" title="丁姓男孩名字大全">丁</a></li><li><a href="/qmdqjg/%CE%BA/" title="魏姓男孩名字大全">魏</a></li><li><a href="/qmdqjg/%D1%A6/" title="薛姓男孩名字大全">薛</a></li><li><a href="/qmdqjg/%D2%B6/" title="叶姓男孩名字大全">叶</a></li><li><a href="/qmdqjg/%D1%D6/" title="阎姓男孩名字大全">阎</a></li><li><a href="/qmdqjg/%D3%E0/" title="余姓男孩名字大全">余</a></li><li><a href="/qmdqjg/%C5%CB/" title="潘姓男孩名字大全">潘</a></li><li><a href="/qmdqjg/%B6%C5/" title="杜姓男孩名字大全">杜</a></li><li><a href="/qmdqjg/%B4%F7/" title="戴姓男孩名字大全">戴</a></li><li><a href="/qmdqjg/%CF%C4/" title="夏姓男孩名字大全">夏</a></li><li><a href="/qmdqjg/%D6%D3/" title="钟姓男孩名字大全">钟</a></li><li><a href="/qmdqjg/%CD%F4/" title="汪姓男孩名字大全">汪</a></li><li><a href="/qmdqjg/%CC%EF/" title="田姓男孩名字大全">田</a></li><li><a href="/qmdqjg/%C8%CE/" title="任姓男孩名字大全">任</a></li><li><a href="/qmdqjg/%BD%AA/" title="姜姓男孩名字大全">姜</a></li><li><a href="/qmdqjg/%B7%B6/" title="范姓男孩名字大全">范</a></li><li><a href="/qmdqjg/%B7%BD/" title="方姓男孩名字大全">方</a></li><li><a href="/qmdqjg/%CA%AF/" title="石姓男孩名字大全">石</a></li><li><a href="/qmdqjg/%D2%A6/" title="姚姓男孩名字大全">姚</a></li><li><a href="/qmdqjg/%CC%B7/" title="谭姓男孩名字大全">谭</a></li><li><a href="/qmdqjg/%C1%CE/" title="廖姓男孩名字大全">廖</a></li><li><a href="/qmdqjg/%D7%DE/" title="邹姓男孩名字大全">邹</a></li><li><a href="/qmdqjg/%D0%DC/" title="熊姓男孩名字大全">熊</a></li><li><a href="/qmdqjg/%BD%F0/" title="金姓男孩名字大全">金</a></li><li><a href="/qmdqjg/%C2%BD/" title="陆姓男孩名字大全">陆</a></li><li><a href="/qmdqjg/%BA%C2/" title="郝姓男孩名字大全">郝</a></li><li><a href="/qmdqjg/%BF%D7/" title="孔姓男孩名字大全">孔</a></li><li><a href="/qmdqjg/%B0%D7/" title="白姓男孩名字大全">白</a></li><li><a href="/qmdqjg/%B4%DE/" title="崔姓男孩名字大全">崔</a></li><li><a href="/qmdqjg/%BF%B5/" title="康姓男孩名字大全">康</a></li><li><a href="/qmdqjg/%C3%AB/" title="毛姓男孩名字大全">毛</a></li><li><a href="/qmdqjg/%C7%F1/" title="邱姓男孩名字大全">邱</a></li><li><a href="/qmdqjg/%C7%D8/" title="秦姓男孩名字大全">秦</a></li><li><a href="/qmdqjg/%BD%AD/" title="江姓男孩名字大全">江</a></li><li><a href="/qmdqjg/%CA%B7/" title="史姓男孩名字大全">史</a></li><li><a href="/qmdqjg/%B9%CB/" title="顾姓男孩名字大全">顾</a></li><li><a href="/qmdqjg/%BA%EE/" title="侯姓男孩名字大全">侯</a></li><li><a href="/qmdqjg/%C9%DB/" title="邵姓男孩名字大全">邵</a></li><li><a href="/qmdqjg/%C3%CF/" title="孟姓男孩名字大全">孟</a></li><li><a href="/qmdqjg/%C1%FA/" title="龙姓男孩名字大全">龙</a></li><li><a href="/qmdqjg/%CD%F2/" title="万姓男孩名字大全">万</a></li><li><a href="/qmdqjg/%B6%CE/" title="段姓男孩名字大全">段</a></li><li><a href="/qmdqjg/%B2%DC/" title="曹姓男孩名字大全">曹</a></li><li><a href="/qmdqjg/%C7%AE/" title="钱姓男孩名字大全">钱</a></li><li><a href="/qmdqjg/%CC%C0/" title="汤姓男孩名字大全">汤</a></li><li><a href="/qmdqjg/%D2%FC/" title="尹姓男孩名字大全">尹</a></li><li><a href="/qmdqjg/%C0%E8/" title="黎姓男孩名字大全">黎</a></li><li><a href="/qmdqjg/%D2%D7/" title="易姓男孩名字大全">易</a></li><li><a href="/qmdqjg/%B3%A3/" title="常姓男孩名字大全">常</a></li><li><a href="/qmdqjg/%CE%E4/" title="武姓男孩名字大全">武</a></li><li><a href="/qmdqjg/%C7%C7/" title="乔姓男孩名字大全">乔</a></li><li><a href="/qmdqjg/%BA%D8/" title="贺姓男孩名字大全">贺</a></li><li><a href="/qmdqjg/%C0%B5/" title="赖姓男孩名字大全">赖</a></li><li><a href="/qmdqjg/%B9%A8/" title="龚姓男孩名字大全">龚</a></li>      </ul>
    </div>


<div class="myads ad_9"></div>
<div class="footer">
  <div><strong><a href="http://m.hmz.com">手机版</a></strong><a href="http://www.hmz.com/redirect/">电脑版</a></div>
  <p>&copy; 好名字网 www.hmz.com 粤ICP备12050957号-5 <div style="display:none;"><script type="text/javascript" src="/static/js/count.js"></script>
  </div></p>
</div>
<div id="goto_top" class="goto_top">
<a href="javascript:void(0)"></a>
</div></div>

<div class="brother_right">
<ul>
<li class="home"><i class="hd_left_top"></i><i class="hd_right_top"></i><i class="hd_left_bottom"></i><i class="hd_right_bottom"></i><a href="/">首页</a></li>
<li><i class="hd_left_top"></i><i class="hd_right_top"></i><i class="hd_left_bottom"></i><i class="hd_right_bottom"></i>
<a href="/xmcs/">姓名测算</a></li>
<li><i class="hd_left_top"></i><i class="hd_right_top"></i><i class="hd_left_bottom"></i><i class="hd_right_bottom"></i><a href="/bbqm/">宝宝起名</a></li>
<li><i class="hd_left_top"></i><i class="hd_right_top"></i><i class="hd_left_bottom"></i><i class="hd_right_bottom"></i><a href="/gsqm/">公司起名</a></li>
<li><i class="hd_left_top"></i><i class="hd_right_top"></i><i class="hd_left_bottom"></i><i class="hd_right_bottom"></i><a href="/gscm/">公司测名</a></li>
<li><i class="hd_left_top"></i><i class="hd_right_top"></i><i class="hd_left_bottom"></i><i class="hd_right_bottom"></i><a href="/bzsm/">八字算命</a></li>
<li><i class="hd_left_top"></i><i class="hd_right_top"></i><i class="hd_left_bottom"></i><i class="hd_right_bottom"></i><a href="/bzhh/">八字合婚</a></li>
<li><i class="hd_left_top"></i><i class="hd_right_top"></i><i class="hd_left_bottom"></i><i class="hd_right_bottom"></i><a href="/bzpp/">八字排盘</a></li>
<li><i class="hd_left_top"></i><i class="hd_right_top"></i><i class="hd_left_bottom"></i><i class="hd_right_bottom"></i><a href="/huangli/">黄历民俗</a></li>
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
