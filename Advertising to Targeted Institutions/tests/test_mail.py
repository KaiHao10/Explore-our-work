from src.auto_send_mail.Mail import MailConfig, Mail, LoginFailedError
import pytest

SENDER_1 = "3480359228@qq.com"
PASS_1 = "Yourqqpassword"
TO = ["jingfeng050106@gmail.com"]
QQ_CONFIG = MailConfig(
    host="smtp.qq.com", port=465, user="3480359228@qq.com", password="yourqqpassword"
)

SENDER_2 = "jingfeng050106@gmail.com"
PASS_2 = "xxx"
TO_2 = ["3480359228@qq.com"]
GMAIL_CONFIG = MailConfig(
    host="smtp.gmail.com", port=587, user=SENDER_2, password=PASS_2, encrypt="tls"
)


def test_mail_success():
    mail = Mail(config=QQ_CONFIG)
    login_success = mail.login()
    assert login_success == True, "Login failed for QQ mail"
    mail.close_connection()


def test_mail_fail():
    mail = Mail(config=GMAIL_CONFIG)
    with pytest.raises(LoginFailedError):
        mail.login(max_retry=3, retry_interval=1, timeout=2)
