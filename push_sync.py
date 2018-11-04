import zmq
import time
import json
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
log = logging.getLogger()
random.seed()
port = 11223

class msg_count:
    n = 0


def send():
    log.info('Starting server (PUSH)')
    start = time.time()
    log.info("Sending messages...")
    while True:
        context = zmq.Context(1)
        socket = context.socket(zmq.PUSH)
        socket.connect("tcp://127.0.0.1:11223")
        #stream = zmq.eventloop.zmqstream.ZMQStream(socket)
        msg_count.n += 1
        #socket.send('meh {}'.format(msg_count.n))
        msg = json.dumps([msg_count.n, '0']) # * random.randint(25000, 25000 * 3)])
        socket.send(msg)
        socket.close()
        context.term()
        if time.time() - start > 120:
            break
        time.sleep(.011)
    context = zmq.Context(1)
    socket = context.socket(zmq.PUSH)
    socket.connect("tcp://127.0.0.1:11223")
    socket.send('0')
    socket.close()
    context.term()
    log.info('Number sent %s' % msg_count.n)

send()

