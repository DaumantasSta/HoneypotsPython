import logging
import logging.handlers
import json
import asyncio
import aiocoap
import datetime
from aiocoap import *
from aiocoap import resource

LOG_FILE = 'coap_requests.json'

class CoapRequestHandler(resource.Resource):
    def __init__(self):
        super().__init__()

    async def render_get(self, request):
        # Log the incoming GET
        log_request(request.remote.hostinfo, 'GET', request.opt.uri_path, request.payload, request.opt)
        return aiocoap.Message(payload=b"SmartHome Security System.")

    async def render_post(self, request):
        # Log the incoming POST
        log_request(request.remote.hostinfo, 'POST', request.opt.uri_path, request.payload, request.opt)
        return aiocoap.Message(payload=b"SmartHome Security System.")

    async def render_put(self, request):
        # Log the incoming PUT
        log_request(request.remote.hostinfo, 'PUT', request.opt.uri_path, request.payload, request.opt)
        return aiocoap.Message(payload=b"SmartHome Security System.")

    async def render_delete(self, request):
        # Log the incoming DELETE
        log_request(request.remote.hostinfo, 'DELETE', request.opt.uri_path, request.payload, request.opt)
        return aiocoap.Message(payload=b"SmartHome Security System.")

def log_request(ip_address, method, uri, payload, options):

    timestamp = int(datetime.datetime.now().timestamp())

    request_data = {
        'timestamp' : timestamp,
        'ip_address': ip_address,
        'method': method,
        'uri': uri,
        'payload': payload.decode('utf-8')
    }

    log_entry = json.dumps(request_data)
    logger.info(log_entry)

def options_to_dict(options):
    # Convert CoAP options to a dictionary
    options_dict = {}
    for option in options:
        options_dict[option.number] = option.value.decode('utf-8')
    return options_dict

async def main():

    protocol = await Context.create_server_context(CoapRequestHandler())

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        await protocol.shutdown()

if __name__ == '__main__':
    logger = logging.getLogger('coap_logger')
    logger.setLevel(logging.INFO)

    file_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=100 * 1024 * 1024, backupCount=0)
    formatter = logging.Formatter('%(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    # Start CoAP server
    asyncio.run(main())
