# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import flask
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound

from apps import mail
from apps.home import blueprint
from apps.config import Config

from flask_mail import Message
default_sender = Config.MAIL_DEFAULT_SENDER

def send_email(to, subject, message):
    
    try:

        msg = Message(
            subject,
            body=message,
            recipients=[to],
            sender=default_sender
            )
        
        mail.send(msg)

        return True, None
    
    except Exception as e:

        print('Error sending email: ' + str( e))
        return False, str( e )

@blueprint.route('/contact/', methods=['GET', 'POST'])
@login_required
def contact():

    msg = None

    if flask.request.method == 'POST':

        contact_name  = request.form.get('full_name')
        contact_email = request.form.get('email')
        contact_msg   = request.form.get('message') 

        status, error = send_email(contact_email, 'Mail from: ' + contact_name, contact_msg)

        if status:
            msg = 'Message sent.'
        else:
            msg = 'Error: ' + error 

    return render_template('contact/send-message.html', msg=msg)

@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
