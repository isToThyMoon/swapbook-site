from threading import Thread

from flask import current_app, render_template

from app import mail
from flask_mail import Message


# 启动了一个新的线程 线程id号不同 这里是取不到current_app的  代理对象受到线程id的影响 它本身作的事情就是线程隔离
def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


def send_mail(to, subject, template, **kwargs):
    # msg = Message('测试邮件标题', sender='935348518@qq.com', body='Test 正文',
    # recipients=['2916709093@qq.com'])

    msg = Message('[鱼书]'+ '' + subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)

    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app, msg])  # 不能直接传递current_app 在下一个线程里会显示它未绑定
    thr.start()
    # mail.send(msg)    # 同步的mail.send()