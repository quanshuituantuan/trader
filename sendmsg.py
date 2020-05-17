#!python3
#接口类型：互亿无线触发短信接口，支持发送验证码短信、订单通知短信等。
#账户注册：请通过该地址开通账户http://user.ihuyi.com/register.html
#注意事项：
#（1）调试期间，请使用用系统默认的短信内容：您的验证码是：【变量】。请不要把验证码泄露给其他人。
#（2）请使用 APIID 及 APIKEY来调用接口，可在会员中心获取；
#（3）该代码仅供接入互亿无线短信接口参考使用，客户可根据实际需要自行编写；
   
#!python3
#-*- coding:utf-8 -*-
# import httplib2
import urllib
import urllib.parse
import urllib.request
 
host  = "106.ihuyi.com"
sms_send_uri = "https://106.ihuyi.com/webservice/sms.php?method=Submit"
 
#查看用户名 登录用户中心->验证码通知短信>产品总览->API接口信息->APIID
account  = "C21817786"
#查看密码 登录用户中心->验证码通知短信>产品总览->API接口信息->APIKEY
password = "894961724278071c022cd9cd0718b554"
 
def send_sms(text="您的验证码是：12。请不要把验证码泄露给其他人。", mobile="13968116385"):
    params = urllib.parse.urlencode({'account': account, 'password' : password, 'content': text, 'mobile':mobile,'format':'json' }).encode(encoding='UTF8')
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    #conn = httplib2.HTTPConnection(host, port=80, timeout=30)
    #conn.request("POST", sms_send_uri, params, headers)
    request = urllib.request.Request(sms_send_uri, params, headers)
    response = urllib.request.urlopen(request)
    response_str = response.read()
 
    return response_str
 
if __name__ == '__main__':
 
    mobile = "13968116385"
    text = "您的验证码是：12。请不要把验证码泄露给其他人。"
    
    response = "none"
    response = send_sms(text, mobile)
    print(response)