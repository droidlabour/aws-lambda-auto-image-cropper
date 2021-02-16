import base64
import logging
import urllib.request

log = logging.getLogger()
log.setLevel('INFO')


def cropter(event, context):
    log.info(event)

    urllib.request.urlretrieve('https://picsum.photos/200/300', '/tmp/1.jpg')
    with open('/tmp/1.jpg', 'rb') as image:
        b64Image = base64.b64encode(image.read()).decode()

    response = {
        'statusCode': 200,
        'body': b64Image,
        'isBase64Encoded': True,
        'headers': {
            'Content-Type': 'image/jpeg'
        }
    }

    return response
