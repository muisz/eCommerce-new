import uuid
import hashlib
import random
from django.conf import settings
from main.models.product import References

def storeRefCode(initial, id):
    reference = "{}-{}".format(initial, id)
    code = str(uuid.uuid4())
    saved = References.objects.create(code=code, value=reference)
    return saved

def checkIsExists(cls, **kwargs):
    try:
        check = cls.objects.get(**kwargs)
        return check
    except:
        return False

def generateHash(txt):
    key = str(settings.SECRET_KEY)
    result = hashlib.pbkdf2_hmac('sha256', str(txt).encode('utf-8'), key.encode('utf-8'), 100000)
    return result.hex()

def verifyPassword(password, chiper):
    hashed = generateHash(password)
    return hashed == chiper