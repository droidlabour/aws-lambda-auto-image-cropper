import json
import base64
import logging
import traceback

from deps.recognize import recognize

log = logging.getLogger()
log.setLevel('INFO')


def cropter(event, context):
    log.info(event)

    with open('/tmp/1', 'wb') as f:
        f.write(base64.b64decode(event['body']))

    try:
        recognize('/tmp/1', '/tmp/output.txt', 'texts/chom.txt')

        with open('/tmp/deskewed.jpg', 'rb') as image:
            b64Image = base64.b64encode(image.read()).decode()

        response = {
            'statusCode': 200,
            'body': b64Image,
            'isBase64Encoded': True,
            'headers': {
                'Content-Type': 'image/jpeg'
            }
        }
    except Exception:
        log.error(traceback.format_exc())

        response = {
            'statusCode': 500,
            'body': json.dumps('Oops, something went wrong!')
        }

    return response
