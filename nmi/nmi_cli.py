#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import asyncio
import logging
import struct
from nmi import NmiClient

log = logging.getLogger(__name__)

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, on_connected, callback, loop):
        self.my_buffer = []
        self.on_connected = on_connected
        self.callback = callback
        self.loop = loop

    def connection_made(self, transport):
        # transport.write()
        if self.on_connected:
            self.on_connected(transport)

    def data_received(self, data):
        log.info('Data received: {!r}'.format(data))
        self.my_buffer.append(data)
        if self.callback:
            self.callback(data)

    def connection_lost(self, exc):
        log.info('The server closed the connection')
        log.info('Stop the event loop')
        self.loop.stop()


class Starnet:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.loop = asyncio.get_event_loop()

        self.client = NmiClient()

        self.device_types = 0xFFFF
        self.transport = None
        self.connected = None
        self.is_received = False
        self.address = None
        self.type_points = {}
        self.num = 0

        self.loop.create_task(self._do_connect())

    def on_connected(self, transport):
        log.info('I was called!')
        self.transport = transport
        x = self.client.request(self.client.NM_MT_DEVC_TYPE, self.device_types)
        self.transport.write(x)

    async def _do_connect(self):
        while True:
            await asyncio.sleep(1)
            if self.connected:
                continue
            try:
                xt, _ = await self.loop.create_connection(
                    lambda: EchoClientProtocol(
                        self.on_connected,
                        self.deal_data,
                        self.loop),
                    self.host,
                    self.port)
                log.info('Connection create on {}'.format(xt))
                self.connected = True
            except OSError:
                log.error('Server not up retrying in 5 seconds...')
            except Exception as e:
                log.error('Error when connect to server: {}'.format(e))

    def deal_data(self, data):
        log.info('I had messages')
        cmd, args = self.client.parse(data)
        log.info(f'--------{cmd},++++++++++{args}')
        if cmd == self.client.NM_MT_DEVC_TYPE:
            if args.DevcType == self.client.NM_XF_430:
                self.address = args.Address
        elif cmd == self.client.NM_MT_DESC:
            log.info(f'=============={args}')
        elif cmd in (
                self.client.NM_MT_SENSOR_ALARMS,
                self.client.NM_MT_CONTROLS,
                self.client.NM_MT_FILTER_ALARMS,
                self.client.NM_MT_SHUNTS,
                self.client.NM_MT_PRE_ALARMS,
                self.client.NM_MT_SENSOR_TRBL
        ):
            points = args.Points
            states = args.States
            self.deal_point(points, states)
        else:
            pass

    def deal_point(self, points, states):
        log.info(f'------{points}, ++++++++{states}')
        if not points or not states:
            return
        bytes_len = len(states)
        lists_num = bytes_len*8//points
        alarm_list = [0 for i in range(points)]
        tamper_list = None
        if lists_num == 2:
            tamper_list = [0 for i in range(points)]
            points = points * 2
        x_list = []
        for i in range(bytes_len):
            for j in range(8):
                x = '{}'.format((states[i] >> j) & 0x01)
                x_list.append(x)
        for i in range(points):
            if tamper_list:
                if i%2 == 0 and x_list[i] == '1':
                    alarm_list[int(i/2)] = 1
                elif i%2 == 1 and x_list[i] == '1':
                    tamper_list[i//2] = 1
                else:
                    pass
            else:
                if x_list[i] == '1':
                    alarm_list[i] = 1
        log.info(f'alarm_list----{alarm_list}\ntamper_list++++{tamper_list}')


    def start(self):
        self._auto_loop()

    def _auto_loop(self):
        self.num += 1
        x = None
        if self.address:
            if self.num == 5:
                x = self.client.request(self.client.NM_MT_SENSOR_ALARMS, self.address)
            elif self.num == 10:
                x = self.client.request(self.client.NM_MT_CONTROLS, self.address)
            elif self.num == 15:
                x = self.client.request(self.client.NM_MT_FILTER_ALARMS, self.address)
            elif self.num == 20:
                x = self.client.request(self.client.NM_MT_SHUNTS, self.address)
            elif self.num == 25:
                x = self.client.request(self.client.NM_MT_PRE_ALARMS, self.address)
            elif self.num == 30:
                x = self.client.request(self.client.NM_MT_SENSOR_TRBL, self.address)
            elif self.num > 30:
                self.num = 0
        if self.transport and x:
            self.transport.write(x)
        self.loop.call_later(1, self._auto_loop)


if __name__ == "__main__":
    log = logging.getLogger("")
    formatter = logging.Formatter("%(asctime)s %(levelname)s " +
                                  "[%(module)s:%(lineno)d] %(message)s")
    # log the things
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(formatter)
    log.addHandler(ch)

    loop = asyncio.get_event_loop()
    star = Starnet('0.0.0.0', 850)
    star.start()
    loop.run_forever()
    loop.close()
