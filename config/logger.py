import logging
from fastapi import Request 
from fastapi import status
from pythonjsonlogger import jsonlogger
from logtail import LogtailHandler


LEVEL_TO_NAME = {
    logging.CRITICAL: 'Critical',
    logging.ERROR: 'Error',
    logging.WARNING: 'Warning',
    logging.INFO: 'Information',
    logging.DEBUG: 'Debug',
    logging.NOTSET: 'Trace',
}

logger = logging.getLogger(__name__)
handler = logging.FileHandler(filename='app.log')
handler.setFormatter(jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(message)s %(ip_address)s %(method)s %(status_code)s"))
logger.handlers = []
logger.addHandler(handler)
logger.setLevel(logging.INFO)

betterstrack_handler = LogtailHandler(source_token="dzFwv5kKh8mJ1QQNKj5QybMk")
logger.addHandler(betterstrack_handler)

data = {
    'ip_address': '0,0,0,0',
    'method': 'N/A',
    'status_code': status.HTTP_200_OK
}

def genericLoadRequest(r: Request):
 data['ip_address'] = r.client.host
 data['method'] = r.method
 data['status_code'] = status.HTTP_200_OK

