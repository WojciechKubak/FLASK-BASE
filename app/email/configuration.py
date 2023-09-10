from flask_mail import Mail, Message
from flask import Flask
from dataclasses import dataclass, field
from jinja2 import Environment
from datetime import datetime
from typing import Self
import os


@dataclass
class MailConfig:
    """
    Configuration class for sending emails using Flask-Mail.

    Attributes:
        mail (Mail): Flask-Mail instance for sending emails.
        template_env (Environment): Jinja2 template environment for rendering email templates.

    """
    mail: Mail = field(default=None, init=False)
    template_env: Environment = field(default=None, init=False)

    @classmethod
    def prepare_mail(cls: Self, app: Flask, template_env: Environment) -> None:
        """
        Initialize the Flask-Mail instance and template environment.

        Args:
            app (Flask): The Flask application instance.
            template_env (Environment): Jinja2 template environment for rendering email templates.

        Returns:
            None
        """
        cls.mail = Mail(app)
        cls.template_env = template_env

    @classmethod
    def send_activation_mail(cls: Self, username: str, email: str) -> None:
        """
        Send an activation email to the specified user.

        Args:
            username (str): The username of the recipient.
            email (str): The recipient's email address.

        Returns:
            None
        """
        timestamp = datetime.utcnow().timestamp() * 1000 + int(os.getenv('REGISTER_TOKEN_LIFESPAN'))
        activation_url = f'http://localhost/users/activate?username={username}&timestamp={timestamp}'
        template = cls.template_env.get_template('activation_email.html')
        html_body = template.render(username=username, activation_url=activation_url)

        message = Message(
            subject='Activate your account',
            sender=os.environ.get('MAIL_USERNAME'),
            recipients=[email],
            html=html_body
        )
        MailConfig.mail.send(message)
