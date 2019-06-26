from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.models.base import db
from app.models.user import User
from . import web
from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from app.libs.email import send_mail


@web.route('/register', methods=['GET', 'POST'])
def register():
    # print('request: {}'.format(request.form))
    form = RegisterForm(request.form)
    # print('校验：{}'.format(form.data))
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
            # db.session.commit()
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user= User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('账号不存在或密码错误')
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            account_email = form.email.data
            user = User.query.filter_by(email=account_email).first_or_404()
            send_mail(form.email.data, '重置你的密码', 'email/reset_password.html',
                      user=user, token=user.generate_token()
                      )
            flash('一封邮件已发送至你的邮箱' + account_email + '，请查收')
            # return redirect(url_for('web.login'))
    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == "POST" and form.validate():
        success = User.reset_password(token, form.password1.data)
        if success:
            flash('你的密码已更新 请使用新密码登录')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败')
    return render_template('auth/forget_password.html', form=form)


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
