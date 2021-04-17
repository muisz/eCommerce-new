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

def dictfetchall(cursor):
    # "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def getPaginate(request, data, **kwargs):
    page = settings.PAGINATION['PAGE']
    page_size = settings.PAGINATION['PAGE_SIZE']
    params = request.GET

    page_query = kwargs['pageQueryName']
    size_query = kwargs['sizeQueryName']

    if page_query in params and params[page_query] != '':
        page = int(params[page_query])

    if size_query in params and params[size_query] != '':
        page_size = int(params[size_query])

    return paginate(data, page, page_size)

def paginate(data, page, page_size):
    try:
        dataLength = len(data)
        if dataLength > 0:
            maxPage = 0

            if dataLength % page_size == 0:
                maxPage = int(dataLength / page_size)
            else:
                maxPage = int(dataLength / page_size) + 1

            result = []
            current = []
            start = 0
            perPage = page_size
            for i in range(maxPage):
                new_data = data[start:perPage]
                result.append(new_data)
                meta = start + 1
                current.append('{}-{}-{}'.format(meta, len(new_data) + start, dataLength))
                start += page_size
                perPage += page_size

            # return {'data':result[page - 1], 'size':maxPage, 'current':current[page - 1]}
            return {
                'data': result[page - 1],
                'meta': {
                    'total_data': len(data),
                    'total_page': maxPage,
                    'page': page,
                    'page_size': page_size,
                    'current': current[page - 1]
                }
            }
        else:
           raise

    except:
        return {
                'data': [],
                'meta': {
                    'total_data': 0,
                    'total_page': 0,
                    'page': page,
                    'page_size': page_size,
                    'current': '0-0-0'
                }
            }