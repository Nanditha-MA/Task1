from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from fastapi import BackgroundTasks

conf = ConnectionConfig(
    MAIL_USERNAME="nandithanandu5244@gmail.com",
    MAIL_PASSWORD="nqcc qwvv yquj rknh",
    MAIL_FROM="nandithanandu5244@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

def send_email(background_tasks: BackgroundTasks, subject: str, email: EmailStr, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=body,
        subtype="plain"
    )

    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)
