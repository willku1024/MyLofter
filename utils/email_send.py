# _*_ coding: utf-8 _*_
__author__ = 'willxin'
__date__ = '2017/8/15  13:32'

import hashlib
import random
from time import time
from Users.models import EmailVerifyRecord
from django.core.mail import send_mail,EmailMessage
from MyLofter.settings import EMAIL_FROM
from celery import task

@task
def send_register_email(email, send_type="register",website="jd.coderr.cn"):
    email_record = EmailVerifyRecord()
    code = generate_random_str()
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()



    if send_type == "register":
        email_title = "网站注册激活"
        url = "http://{0}/user/active/{1}".format(website,code)
        email_body = '''
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;background-color: #ebedf0;font-family:&#39;Alright Sans LP&#39;, &#39;Avenir Next&#39;, &#39;Helvetica Neue&#39;, Helvetica, Arial, &#39;PingFang SC&#39;, &#39;Source Han Sans SC&#39;, &#39;Hiragino Sans GB&#39;, &#39;Microsoft YaHei&#39;, &#39;WenQuanYi MicroHei&#39;, sans-serif;">
          <tr>
            <td>
              <table cellpadding="0" cellspacing="0" align="center" width="640">
                <tr>
                  <td style="height:20px;"></td>
                </tr>
                <tr>
                  <td height="10"></td>
                </tr>
                <tr>
                  <td>
                    <table cellpadding="0" cellspacing="0" width="640">
                      <tr style="line-height: 40px;">
                        <td width='80' style="padding-left: 290px;">
                          <a href="http://jd.coderr.cn">
                          </a>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
                <tr>
                  <td height="40"></td>
                </tr>
                <tr>
                  <td style="background-color: #fff;border-radius:6px;padding:40px 40px 0;">
                    <table>
                      <tr height="40">
                        <td style="padding-left:25px;padding-right:25px;font-size:18px;font-family:&#39;微软雅黑&#39;,&#39;黑体&#39;,arial;">
                          尊敬的{0}，您好,
                        </td>
                      </tr>
                      <tr height="15">
                        <td></td>
                      </tr>
                      <tr height="30">
                        <td style="padding-left:55px;padding-right:55px;font-family:&#39;微软雅黑&#39;,&#39;黑体&#39;,arial;font-size:14px;">
                          感谢您的注册。
                        </td>
                      </tr>
                      <tr height="30">
                        <td style="padding-left:55px;padding-right:55px;font-family:&#39;微软雅黑&#39;,&#39;黑体&#39;,arial;font-size:14px;">
                          请点击以下链接进行邮箱验证，以便开始使用您的账户：
                        </td>
                      </tr>
                      <tr height="60">
                        <td style="padding-left:55px;padding-right:55px;font-family:&#39;微软雅黑&#39;,&#39;黑体&#39;,arial;font-size:14px;">
                          <a href="{1}">
                            马上验证邮箱
                          </a>
                        </td>
                      </tr>
                      <tr height="10">
                        <td></td>
                      </tr>
                      <tr height="20">
                        <td style="padding-left:55px;padding-right:55px;font-family:&#39;微软雅黑&#39;,&#39;黑体&#39;,arial;font-size:12px;">
                          如果您无法点击以上链接，请复制以下网址到浏览器里直接打开：
                          <p>{1}</p>
                        </td>
                      </tr>
                      <tr height="30">
                        <td style="padding-left:55px;padding-right:65px;font-family:&#39;微软雅黑&#39;,&#39;黑体&#39;,arial;line-height:18px;">
                        </td>
                      </tr>
                      <tr height="20">
                        <td style="padding-left:55px;padding-right:55px;font-family:&#39;微软雅黑&#39;,&#39;黑体&#39;,arial;font-size:12px;">
                          如果您并未申请该服务账户，可能是其他用户误输入了您的邮箱地址。请忽略此邮件。
                        </td>
                      </tr>
                      <tr height="20">
                        <td></td>
                      </tr>
                    </table>
                  </td>
                </tr>
                <tr>
                  <td style="height:40px;"></td>
                </tr>
                <tr>
                  <td style="height:50px;"></td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
            '''
        email_body = email_body.format(email, url, url)

        # send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.content_subtype = "html"
        msg.send()


    if send_type == "forget":
        email_title = "网站密码重置"
        # email_body = "请点击下面的链接重置你的账号：http://{0}/user/reset/{1}".format(website,code)
        url = "http://{0}/user/reset/{1}".format(website,code)
        email_body = '''
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;background-color: #ebedf0;font-family:&#39;Alright Sans LP&#39;, &#39;Avenir Next&#39;, &#39;Helvetica Neue&#39;, Helvetica, Arial, &#39;PingFang SC&#39;, &#39;Source Han Sans SC&#39;, &#39;Hiragino Sans GB&#39;, &#39;Microsoft YaHei&#39;, &#39;WenQuanYi MicroHei&#39;, sans-serif;">
                  <tr>
                    <td>
                      <table cellpadding="0" cellspacing="0" align="center" width="640">
                        <tr>
                          <td style="height:20px;"></td>
                        </tr>
                        <tr>
                          <td height="10"></td>
                        </tr>
                        <tr>
                          <td>
                            <table cellpadding="0" cellspacing="0" width="640">
                              <tr style="line-height: 40px;">
                                <td width='80' style="padding-left: 290px;">
                                  <a href="http://jd.coderr.cn">
                                  </a>
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                        <tr>
                          <td height="40"></td>
                        </tr>
                        <tr>
                          <td style="background-color: #fff;border-radius:6px;padding:40px 40px 0;">
                            <table>
                              <tr height="40">
                                <td style="padding-left:25px;padding-right:25px;font-size:18px;font-family:&#39;微软雅黑&#39;,&#39;黑体&#39;,arial;">
                                  尊敬的{0}，您好,
                                </td>
                              </tr>
                              <tr height="15">
                                <td></td>
                              </tr>
                              <tr height="30">
                                <td style="padding-left:55px;padding-right:55px;font-family:&#39;微软雅黑&#39;,&#39;黑体&#39;,arial;font-size:14px;">
                                  您正在使用重置密码服务。
                                </td>
                              </tr>
                              <tr height="30">
                                <td style="padding-left:55px;padding-right:55px;font-family:&#39;微软雅黑&#39;,&#39;黑体&#39;,arial;font-size:14px;">
                                  请点击以下链接进行邮箱重置密码，以便重新开始使用您的账户：
                                </td>
                              </tr>
                              <tr height="60">
                                <td style="padding-left:55px;padding-right:55px;font-family:&#39;微软雅黑&#39;,&#39;黑体&#39;,arial;font-size:14px;">
                                  <a href="{1}">
                                    重置邮箱密码
                                  </a>
                                </td>
                              </tr>
                              <tr height="10">
                                <td></td>
                              </tr>
                              <tr height="20">
                                <td style="padding-left:55px;padding-right:55px;font-family:&#39;微软雅黑&#39;,&#39;黑体&#39;,arial;font-size:12px;">
                                  如果您无法点击以上链接，请复制以下网址到浏览器里直接打开：
                                  <p>{1}</p>
                                </td>
                              </tr>
                              <tr height="30">
                                <td style="padding-left:55px;padding-right:65px;font-family:&#39;微软雅黑&#39;,&#39;黑体&#39;,arial;line-height:18px;">
                                </td>
                              </tr>
                              <tr height="20">
                                <td style="padding-left:55px;padding-right:55px;font-family:&#39;微软雅黑&#39;,&#39;黑体&#39;,arial;font-size:12px;">
                                  如果您并未申请重置密码服务，可能是其他用户误输入了您的邮箱地址。请忽略此邮件。
                                </td>
                              </tr>
                              <tr height="20">
                                <td></td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                        <tr>
                          <td style="height:40px;"></td>
                        </tr>
                        <tr>
                          <td style="height:50px;"></td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
                    '''
        email_body = email_body.format(email,url,url)

        # send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

        msg = EmailMessage(email_title, email_body, EMAIL_FROM,  [email])
        msg.content_subtype = "html"
        msg.send()


def generate_random_str(random_len=10):
    def md5_code():
        timestamp = str(int(time()))
        m = hashlib.md5()
        m.update(timestamp)
        return m.hexdigest()

    hash_code = []
    hash_code += [random.choice(md5_code()) for i in range(0, random_len)]
    return ''.join(hash_code).upper()


