"""
Configuration for sending emails
"""
import os
from fastapi_mail import ConnectionConfig


# conf = ConnectionConfig(
#    MAIL_USERNAME=os.environ.get("MAIL_USERNAME"),
#    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD"),
#    MAIL_FROM=os.environ.get("MAIL_FROM"),
#    MAIL_PORT=os.environ.get("MAIL_PORT"),
#    MAIL_SERVER=os.environ.get("MAIL_SERVER"),
#    MAIL_TLS=True,
#    MAIL_SSL=False
# )
