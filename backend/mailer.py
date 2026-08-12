from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from flask import render_template

SERVER_SMTP_HOST = 'localhost'
SERVER_SMTP_PORT = 1025              
SENDER_ADDRESS   = 'noreply@trekapp.com'
SENDER_PASSWORD  = ''               

def send_email(to_address, subject, message, content='text', attachment=None):
   
    msg = MIMEMultipart()
    msg['To']      = to_address
    msg['From']    = SENDER_ADDRESS
    msg['Subject'] = subject

    if content == 'html':
        msg.attach(MIMEText(message, 'html'))
    else:
        msg.attach(MIMEText(message, 'plain'))

    if attachment:
        with open(attachment, 'rb') as a:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(a.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={attachment}')
        msg.attach(part)

    try:
        s = smtplib.SMTP(host=SERVER_SMTP_HOST, port=SERVER_SMTP_PORT)
        s.login(SENDER_ADDRESS, SENDER_PASSWORD)
        s.send_message(msg)
        s.quit()
        print(f'[MAIL] Sent "{subject}" → {to_address}')
        return True
    except Exception as e:
        print(f'[MAIL WARNING] Could not send to {to_address}: {e}')
        print('[MAIL WARNING] Is MailHog running? → docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog')
        return False



def send_welcome_user(user_email, user_name):
    html = render_template('welcome_user.html', name=user_name, email=user_email)
    return send_email(user_email, '🏔️ Welcome to Trekking Management App!', html, content='html')


def send_welcome_staff(staff_email, staff_name, password):
    html = render_template('welcome_staff.html',
                           name=staff_name, email=staff_email, password=password)
    return send_email(staff_email, '🧭 Your Trek Staff Account is Ready!', html, content='html')


def send_booking_confirmed(user_email, user_name, booking_id, trek):
    html = render_template(
        'booking_confirmed.html',
        user_name       = user_name,
        booking_id      = booking_id,
        trek_name       = trek.trek_name,
        trek_location   = trek.trek_Location,
        trek_difficulty = trek.trek_difficulty,
        start_date      = trek.start_date.strftime('%d %b %Y') if trek.start_date else '—',
        end_date        = trek.end_date.strftime('%d %b %Y')   if trek.end_date   else '—',
        duration        = trek.duration,
    )
    return send_email(user_email, f'✅ Booking Confirmed — {trek.trek_name}', html, content='html')


def send_booking_cancelled(user_email, user_name, booking_id, trek):
    html = render_template(
        'booking_cancelled.html',
        user_name     = user_name,
        booking_id    = booking_id,
        trek_name     = trek.trek_name,
        trek_location = trek.trek_Location,
        start_date    = trek.start_date.strftime('%d %b %Y') if trek.start_date else '—',
        end_date      = trek.end_date.strftime('%d %b %Y')   if trek.end_date   else '—',
    )
    return send_email(user_email, f'❌ Booking Cancelled — {trek.trek_name}', html, content='html')
