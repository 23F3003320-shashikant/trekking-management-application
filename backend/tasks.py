from celery_worker import celery_app

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from flask import render_template
from models.models import Users, Treks, Booking

SERVER_SMTP_HOST = 'localhost'
SERVER_SMTP_PORT = 1025                        
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


@celery_app.task
def send_daily_reminder():
    
    confirmed_bookings = Booking.query.filter_by(status='Confirmed').all()

    for booking in confirmed_bookings:
        user = Users.query.get(booking.user_id)
        trek = Treks.query.get(booking.trek_id)

        if user and trek:
            send_email(
                to_address = user.email_id,
                subject    = f'🏔️ Reminder: Your trek "{trek.trek_name}" is coming up!',
                message    = (
                    f'Hello {user.name},\n\n'
                    f'This is your daily reminder for your upcoming trek:\n\n'
                    f'  Trek     : {trek.trek_name}\n'
                    f'  Location : {trek.trek_Location}\n'
                    f'  Dates    : {trek.start_date.strftime("%d %b %Y") if trek.start_date else "—"}'
                    f' → {trek.end_date.strftime("%d %b %Y") if trek.end_date else "—"}\n'
                    f'  Duration : {trek.duration} days\n\n'
                    f'Please make sure you are prepared with all necessary gear.\n\n'
                    f'Happy Trekking!\n'
                    f'Trekking Management App'
                ),
                content = 'text'
            )

    return f'Daily reminder sent to {len(confirmed_bookings)} trekkers with confirmed bookings.'


@celery_app.task
def send_monthly_report():
    
    admin = Users.query.filter_by(role='admin').first()
    if not admin:
        return 'No admin user found.'

    all_bookings = Booking.query.all()
    booking_data = []
    for b in all_bookings:
        user = Users.query.get(b.user_id)
        trek = Treks.query.get(b.trek_id)
        booking_data.append({
            'booking_id'    : b.booking_id,
            'user_name'     : user.name     if user else b.user_id,
            'trek_name'     : trek.trek_name     if trek else '—',
            'trek_location' : trek.trek_Location if trek else '—',
            'booking_date'  : b.booking_date.strftime('%d %b %Y') if b.booking_date else '—',
            'status'        : b.status,
            'payment_status': b.payment_status,
        })

    html = render_template(
        'monthly_report.html',
        admin_name    = admin.name,
        bookings      = booking_data,
        total         = len(booking_data),
        total_treks   = Treks.query.count(),
        total_users   = Users.query.filter_by(role='trekker').count(),
        total_staff   = Users.query.filter_by(role='staff').count(),
    )

    send_email(
        to_address = admin.email_id,
        subject    = '📊 Monthly Trekking Report',
        message    = html,
        content    = 'html'
    )

    return f'Monthly report sent to admin ({admin.email_id}).'


@celery_app.task
def export_trekker_bookings(user_email):
    """
    Triggered manually from the Trekker dashboard.
    Sends an HTML email to the trekker with their full booking history.
    """
    user = Users.query.get(user_email)
    if not user:
        return 'User not found.'

    bookings = Booking.query.filter_by(user_id=user_email).all()
    if not bookings:
        return 'No bookings found for this user.'

    booking_data = []
    for b in bookings:
        trek = Treks.query.get(b.trek_id)
        booking_data.append({
            'booking_id'    : b.booking_id,
            'trek_name'     : trek.trek_name     if trek else '—',
            'trek_location' : trek.trek_Location if trek else '—',
            'start_date'    : trek.start_date.strftime('%d %b %Y') if trek and trek.start_date else '—',
            'end_date'      : trek.end_date.strftime('%d %b %Y')   if trek and trek.end_date   else '—',
            'booking_date'  : b.booking_date.strftime('%d %b %Y') if b.booking_date else '—',
            'status'        : b.status,
            'payment_status': b.payment_status,
        })

    html = render_template(
        'export_bookings.html',
        user_name         = user.name,
        bookings          = booking_data,
        total_bookings    = len(booking_data),
    )

    send_email(
        to_address = user.email_id,
        subject    = '📋 Your Trekking Bookings Export',
        message    = html,
        content    = 'html'
    )

    return f'Booking export sent to {user.email_id}.'
