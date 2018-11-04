import zmq
import time
import json
import random
import zmq
import zmq.eventloop
import zmq.eventloop.zmqstream
import tornado.gen
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
log = logging.getLogger()

zmq.eventloop.ioloop.install()
io_loop = tornado.ioloop.IOLoop.current()
random.seed()
port = 11223

class msg_count:
    n = 0


@tornado.gen.coroutine
def sleeper():
    time.sleep(1)
    raise tornado.gen.Return()

def send():
    log.info('Starting server (PUSH)')
    start = time.time()
    log.info("Sending messages...")
    while True:
        context = zmq.Context(1)
        socket = context.socket(zmq.PUSH)
        socket.setsockopt(
            zmq.TCP_KEEPALIVE, True
        )
        socket.setsockopt(
            zmq.TCP_KEEPALIVE_IDLE, 300
        )
        socket.setsockopt(
            zmq.TCP_KEEPALIVE_CNT, -1
        )
        socket.setsockopt(
            zmq.TCP_KEEPALIVE_INTVL, -1
        )
        socket.setsockopt(zmq.SNDHWM, 1000)
        socket.setsockopt(zmq.RCVHWM, 1000)
        socket.setsockopt(zmq.BACKLOG, 1000)
        socket.connect("tcp://127.0.0.1:11223")
        #stream = zmq.eventloop.zmqstream.ZMQStream(socket)
        msg_count.n += 1
        #socket.send('meh {}'.format(foo.n))
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
    io_loop.stop()

io_loop.call_at(time.time() + 1, send)
io_loop.call_at(time.time() + 2, sleeper)
io_loop.start()

