from flask_mail import Mail, Message
from flask import Flask
from dataclasses import dataclass, field
from datetime import datetime
from typing import Self
import os


@dataclass
class MailConfig:
    mail: Mail = field(default=None, init=False)

    @classmethod
    def prepare_mail(cls: Self, app: Flask) -> None:
        cls.mail = Mail(app)

    @classmethod
    def send_mail(cls: Self, username: str, email: str) -> None:
        timestamp = datetime.utcnow().timestamp() * 1000 + int(os.getenv('REGISTER_TOKEN_LIFESPAN'))
        html_body = MailConfig._generate_html_body(username, timestamp)
        message = Message(
            subject='Activate your account',
            sender=os.environ.get('MAIL_USERNAME'),
            recipients=[email],
            html=html_body
        )
        MailConfig.mail.send(message)

    @staticmethod
    def _generate_html_body(username: str, timestamp: float) -> str:
        return f'''\
            <html>
            <body>
                <div style="font-family:Consolas;margin:auto 100px;padding:5px;text-size:16px;color:white;background-color:grey">
                    <h1>Hello {username}!</h1>
                    <h2>Hello Click to activate account: http://localhost/users/activate?username={username}&timestamp={timestamp}</h2>
                </div>
            </body>
            </html>
        '''
