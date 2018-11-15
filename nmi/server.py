#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import asyncio
import logging
import struct
import math
import random
from .nmi import NmiServer
from .status import Status

log = logging.getLogger(__name__)


class TcpServerProtocol(asyncio.Protocol):
    def __init__(self, callback, server):
        self.callback = callback
        self.server = server

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        log.info('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        log.info('Data received: {}'.format(data))
        (cmd, arg) = self.server.parse(data)
        log.info(f'cmd: {cmd}, arg: {arg}\n')
        x = self.callback(cmd, arg)
        if x:
            self.transport.write(x)
            log.info('Data send: {}\n'.format(x))

        # print('Send: {!r}'.format(data))
        # self.transport.write(data)

        # print('Close the client socket')
        # if self.closed:
        #     self.transport.close()


class Site:
    def __init__(self, unit_id, device_type, loop):
        self.port = 849 + unit_id
        self.device_type = device_type
        self.loop = loop

        self.server = NmiServer('NM_XF_430')
        self.device_types = [
            {
                "id": 1,
                "name": "PLC_430",
                "diags": 0,
                "alarms": 8,
                "controls": 8
            },
            {
                "id": 2,
                "name": "PLC_410",
                "diags": 0,
                "alarms": 64,
                "controls": 128
            }
        ]
        self.device = "PLC_430"
        self.diags = 0
        self.alarms = 8
        self.controls = 8

        self.sensor_alarm = ['NORMAL' for i in range(8)]
        self.sensor_tamper = ['NORMAL' for i in range(8)]
        self.filter_alarm = ['NORMAL' for i in range(8)]
        self.filter_tamper = ['NORMAL' for i in range(8)]
        self.shunt_alarm = ['NORMAL' for i in range(8)]
        self.shunt_tamper = ['NORMAL' for i in range(8)]
        self.pre_alarm = ['NORMAL' for i in range(8)]
        self.trbl_alarm = ['NORMAL' for i in range(8)]
        self.control_list = ['NORMAL' for i in range(8)]

        self.auto = False

    def start(self):
        for i in self.device_types:
            if self.device_type == i.get("name").lower():
                self.device = i.get("name")
                self.diags = i.get("diags")
                self.alarms = i.get("alarms")
                self.controls = i.get("controls")
                self.sensor_alarm = ['NORMAL' for i in range(self.alarms)]
                self.sensor_tamper = ['NORMAL' for i in range(self.alarms)]
                self.filter_alarm = ['NORMAL' for i in range(self.alarms)]
                self.filter_tamper = ['NORMAL' for i in range(self.alarms)]
                self.shunt_alarm = ['NORMAL' for i in range(self.alarms)]
                self.shunt_tamper = ['NORMAL' for i in range(self.alarms)]
                self.pre_alarm = ['NORMAL' for i in range(self.alarms)]
                self.trbl_alarm = ['NORMAL' for i in range(self.alarms)]
                self.control_list = ['NORMAL' for i in range(self.controls)]
        self._set_connection()
        self._auto_loop()

    def _auto_loop(self):
        dev_type = {
            'SENSOR': self.sensor_alarm,
            'TAMPER': self.sensor_tamper,
            'FILTER_ALARM': self.filter_alarm,
            'FILTER_TAMPER': self.filter_tamper,
            'SHUNT_ALARM': self.shunt_alarm,
            'SHUNT_TAMPER': self.shunt_tamper,
            'PRE_ALARM': self.pre_alarm,
            'TRBL_ALARM': self.trbl_alarm
        }
        if self.auto:
            x_list = random.choice([i for i in dev_type.values()])
            for k, v in dev_type.items():
                if x_list == v:
                    key = k
            point = random.randint(1, len(x_list)*10)
            status = random.choice(['NORMAL', 'ALARM'])
            if point in range(len(x_list)):
                x_list[point-1] = status
                log.info(f'Auto change: The {point} point is {status} in {key}')
        self.loop.call_later(1, self._auto_loop)

    def _set_connection(self):
        coro = self.loop.create_server(
            lambda: TcpServerProtocol(callback=self.process, server=self.server),
            '0.0.0.0',
            self.port
        )
        server = self.loop.run_until_complete(coro)
        log.info('Serving on {}'.format(server.sockets[0].getsockname()))

    def process(self, cmd, arg):
        if not cmd:
            return None
        if cmd == self.server.NM_MT_DEVC_TYPE:
            pass
            return self.server.respone(cmd,
                                       1,
                                       self.server.NM_XF_430,
                                       self.server.NM_XF_430_DIAGS,
                                       self.server.NM_XF_430_ALARMS,
                                       self.server.NM_XF_430_CONTROLS)
        elif cmd == self.server.NM_MT_DESC:
            desc = f'{arg.Address}_{arg.Type}_{arg.Point}'.encode()
            desc_len = len(desc)
            return self.server.respone(cmd,
                                       arg.Address,
                                       arg.Point,
                                       arg.Type,
                                       desc,
                                       0,
                                       fmt=f'<HHB{desc_len}sB')
        elif cmd == self.server.NM_MT_MATE_STAT:
            mate_state = 0 # 0 is unconnected, 1 is connected
            return self.server.respone(cmd,
                                       mate_state)
        elif cmd == self.server.NM_MT_STANDBY:
            log.warning('No response!!!')
        elif cmd == self.server.NM_MT_COMM_STAT:
            return self.server.respone(cmd,
                                       arg.Address,
                                       1, # 0 is connected (True 1, False 0).
                                       2 # bit 0: Side A Fault, bit 1: Side B Fault
            )
        elif cmd == self.server.NM_MT_DEVC_SMRY:
            return self.server.respone(cmd,
                                       arg.Address,
                                       5 # • Bit 0: Comm. fail active or mismatch between configured and connected device type • Bit 1: 1 or more comm. side faults active • Bit 2: 1 or more fatal diagnostic alarms active • Bit 3: 1 or more warning diagnostic alarms active• Bit 4: Enclosure tamper alarm active
            )
        elif cmd == self.server.NM_MT_DIAG_ALARMS:
            return self.server.respone(cmd,
                                       arg.Address,
                                       self.server.NM_XF_430_DIAGS,
                                       0
            )
        elif cmd == self.server.NM_MT_SENSOR_ALARM:
            return self.server.respone(cmd,
                                      arg.Address,
                                      arg.Alarm,
                                      0, # 0 is alarm, 1 is tamper
                                      0 # alarm location structres
            )
        elif cmd == self.server.NM_MT_SENSOR_ALARMS:
            x = self.calculate(self.sensor_alarm, self.sensor_tamper)
            return self.server.respone(cmd,
                                       arg.Address,
                                       len(self.sensor_alarm),
                                       x,
                                       fmt=f'<HH{len(x)}s'
            )
        elif cmd == self.server.NM_MT_FILTER_ALARM:
            return self.server.respone(cmd,
                                       arg.Address,
                                       arg.Alarm,
                                       0, # 0 is alarm, 1 is tamper
                                       0 # alarm location structres
            )
        elif cmd == self.server.NM_MT_FILTER_ALARMS:
            x = self.calculate(self.filter_alarm, self.filter_tamper)
            return self.server.respone(cmd,
                                       arg.Address,
                                       len(self.filter_alarm),
                                       x,
                                       fmt=f'<HH{len(x)}s'
            )
        elif cmd == self.server.NM_MT_PRE_ALARMS:
            x = self.calculate(self.pre_alarm)
            return self.server.respone(cmd,
                                       arg.Address,
                                       len(self.pre_alarm),
                                       x,
                                       fmt=f'<HH{len(x)}s'
            )
        elif cmd == self.server.NM_MT_SENSOR_TRBL:
            x = self.calculate(self.trbl_alarm)
            return self.server.respone(cmd,
                                       arg.Address,
                                       len(self.trbl_alarm),
                                       x,
                                       fmt=f'<HH{len(x)}s'
            )
        elif cmd == self.server.NM_MT_SHUNTS:
            x = self.calculate(self.shunt_alarm, self.shunt_tamper)
            return self.server.respone(cmd,
                                       arg.Address,
                                       len(self.shunt_alarm),
                                       x,
                                       fmt=f'<HH{len(x)}s'
            )
        elif cmd == self.server.NM_MT_CONTROLS:
            x = self.calculate(self.control_list)
            return self.server.respone(cmd,
                                       arg.Address,
                                       len(self.control_list),
                                       x,
                                       fmt=f'<HH{len(x)}s'
            )
        else:
            pass
        return None

    def calculate(self, alarm_list, tamper_list=None):
        point_nums = len(alarm_list)
        bytes_len = math.ceil(point_nums/8)
        if tamper_list:
            bytes_len = math.ceil(point_nums*2/8)
        x_list = [0 for i in range(bytes_len)]
        for i in range(point_nums):
            byte_position = i//4
            bit_position = i%4*2
            if not tamper_list:
                byte_position = i//8
                bit_position = i%8
            if alarm_list[i] != Status.NORMAL:
                x_list[byte_position] |= 1 << (bit_position + 0)
            if tamper_list:
                if tamper_list[i] != Status.NORMAL:
                    x_list[byte_position] |= 1 << (bit_position + 1)
        data_fmt = b''
        for i in x_list:
            data_fmt += struct.pack('B', i)
        return data_fmt


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # coro = loop.create_server(TcpServerProtocol, '0.0.0.0', 850)
    # server = loop.run_until_complete(coro)

    # print('Serving on {}'.format(server.sockets[0].getsockname()))
    site = Site('0.0.0.0', 850, loop)
    site.start()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    # loop.run_until_complete()
    loop.close()
