from .tasks import send_mail_to

def otp_sender(user):
    """ Function used to send otp code to user on registration """
# generating the otp code based on random_base32() and setting the expiration time [interval=300 for 5 minutes]
    totp = pyotp.TOTP(pyotp.random_base32(), interval=300)
# getting the otp code
    otp = totp.now()
# generating the token bound to the current totp secret so as to deal with user provided code validation
    token = jwt.encode(
                {
                    'uid': user.id,
                    'tid': totp.secret,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
                    'iat': datetime.datetime.utcnow(),
                }, 
                settings.SECRET_KEY, 
                algorithm='HS256'
            )
# sending the email to user
    send_mail_to.delay(user.name, user.email, otp)

def otp_checker(user, userCode, userToken):
    """ Function used to check otp code provided by user """
# decoding the userToken and processing the incoming
    try:
        payload = jwt.decode(userToken, settings.SECRET_KEY, algorithms=['HS256'])
        if payload['uid'] == user.id:
        # generating the otp code based on secret stored on payload
            totp = pyotp.TOTP(payload['tid'], interval=300)
        # checking the correctness with userCode
            if totp.verify(userCode):
                # TODO : settings user account_status to on
                return{'success': 'Account activated successfully.'}
            else:
                return {'error': 'Wrong code provided. Please, recheck your mails seeking for the correct code received.'}
    except:
        return {'error': 'Code has expired. Please, renew another one and send it back.'}
