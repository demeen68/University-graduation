from django.core.mail import send_mail
from Mainweb.settings import EMAIL_FORM
from Mainweb.settings import WEB_URL


def send_email(email, send_type, other_details=''):
    """Send email
    :param email: target email(whom will we send the message)
    :param send_type: has not been used in this system
    :return: check if the email has send successfully
    """
    if send_type is None or send_type is "":
        return
    if send_type is "title":
        email_title = u'网络爬虫 \"' + other_details + '\" 已完成'
        email_body = u'点击链接查看:http://' + WEB_URL + '/backms/graph/?title=' + other_details
    else:
        return False
    send_states = send_mail(email_title, email_body, EMAIL_FORM, [email])
    if send_states:
        return True
    else:
        return False
