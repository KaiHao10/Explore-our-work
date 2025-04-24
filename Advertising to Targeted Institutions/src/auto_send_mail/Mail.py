"""
This is a simple mail sender using SMTP.
It uses the smtplib and email libraries to send emails.
It is designed to be used with a QQ account.
It is a simple and easy to use mail sender.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import sys
from dataclasses import dataclass
import time


class LoginFailedError(Exception):
    """
    Exception raised when login fails.
    """


@dataclass
class MailConfig:
    """
    Configuration for the mail sender.
    :param host: SMTP server host
    :param port: SMTP server port
    :param user: SMTP server user
    :param password: SMTP server password
    :param encrypt: Encryption type (ssl or tls)
    """

    host: str
    user: str
    password: str
    port: int = 465
    encrypt: str = "ssl"


class Mail:
    def __init__(self, config: MailConfig):
        """
        Initialize the mail sender.
        :param host: SMTP server host
        :param port: SMTP server port
        :param user: SMTP server user
        :param password: SMTP server password
        """
        self.__config = config

    @property
    def encrypt(self):
        """
        Get the encryption type.
        :return: Encryption type (ssl or tls)
        """
        return self.__config.encrypt

    @property
    def host(self):
        """
        Get the SMTP server host.
        :return: SMTP server host
        """
        return self.__config.host

    @property
    def user(self):
        """
        Get the SMTP server user.
        :return: SMTP server user
        """
        return self.__config.user

    def login(self, max_retry: int = 3, retry_interval: int = 5, timeout: int = 10):
        """
        Login to the SMTP server.
        :return: True if login is successful, False otherwise
        """

        def try_login(num_try: int):
            print(
                f"Trying to login to {self.__config.host} as {self.__config.user} ({num_try}/{max_retry})"
            )
            try:
                if self.__config.encrypt == "ssl":
                    self.__stmp = smtplib.SMTP_SSL(
                        self.__config.host, self.__config.port, timeout=timeout
                    )
                    self.__stmp.login(self.__config.user, self.__config.password)
                elif self.__config.encrypt == "tls":
                    self.__stmp = smtplib.SMTP(
                        self.__config.host, self.__config.port, timeout=timeout
                    )
                    self.__stmp.starttls()
                    self.__stmp.login(self.__config.user, self.__config.password)
                print(f"Login successful: {self.__config.user}")
                return True
            except Exception as e:
                print(f"Login failed: {e}")
                return False

        for num_try in range(1, max_retry + 1):
            if try_login(num_try):
                return True
            time.sleep(retry_interval)
        raise LoginFailedError(f"Login failed after {max_retry} attempts")

    def close_connection(self):
        """
        Close the connection to the SMTP server.
        """
        if hasattr(self, "__stmp"):
            self.__stmp.quit()
            print(f"Connection to {self.__config.host} closed")
        else:
            print(f"No connection to close")

    def create_message(
        self,
        subject: str,
        body: str,
        sender: str,
        receiver: list,
        is_html: bool = False,
    ) -> MIMEMultipart:
        """
        Create a message object.
        :param subject: Subject of the email
        :param body: Body of the email (can be plain text or HTML)
        :param sender: Sender of the email
        :param receiver: Receiver of the email
        :param is_html: If True, treat the body as HTML content
        :return: Message object
        """
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = ", ".join(receiver)
        msg["Subject"] = subject
        if is_html:
            msg.attach(MIMEText(body, "html"))
        else:
            msg.attach(MIMEText(body, "plain"))
        self.__msg = msg
        self.__receiver = receiver
        return msg

    def send_mail(self):
        """
        Send the email.
        :return: True if email is sent successfully, False otherwise
        """
        try:
            self.__stmp.sendmail(
                self.__config.user, self.__receiver, self.__msg.as_string()
            )
            print(f"Email sent")
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
