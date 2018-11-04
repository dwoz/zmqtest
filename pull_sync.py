import zmq
import time
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
log = logging.getLogger()

class msg_count:
    n = 0

def main():
    log.info('Starting client (PULL)')
    ctx = zmq.Context.instance()
    s = ctx.socket(zmq.PULL)
    s.setsockopt(
        zmq.TCP_KEEPALIVE, True
    )
    s.setsockopt(
        zmq.TCP_KEEPALIVE_IDLE, 300
    )
    s.setsockopt(
        zmq.TCP_KEEPALIVE_CNT, -1
    )
    s.setsockopt(
        zmq.TCP_KEEPALIVE_INTVL, -1
    )
    s.setsockopt(zmq.SNDHWM, 1000)
    s.setsockopt(zmq.RCVHWM, 1000)
    s.setsockopt(zmq.BACKLOG, 1000)
    s.bind('tcp://127.0.0.1:11223')
    log.info("Receiving messages...")
    while True:
        raw = s.recv()
        if raw == '0':
            break
        msg_count.n += 1
        msg = json.loads(raw)
        time.sleep(.01)
    s.close()
    log.info('Number received %s' % msg_count.n)

main()

