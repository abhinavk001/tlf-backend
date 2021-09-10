"""
Send email
"""
from fastapi_mail import FastMail, MessageSchema
# from mail.config import conf


async def send_reset_email(user, request):
    """
    Send password request form link through email
    """
    #token = user.get_reset_token()
    template = """
        <html>
        <body>
          
<p>Hi !!!
        <br>Thanks for using fastapi mail, keep using it..!!!</p>
  
        </body>
        </html>
        """

    message = MessageSchema(
        subject = "TLF | Reset Password Request",
        recipients = ["godofwars0017@gmail.com"],
        body = template,
        subtype = "html",
    )
    # fm = FastMail(conf)
    # await fm.send_message(message)
    # print(message)
