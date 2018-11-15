# -*- coding: utf-8 -*-

"""Main module."""

from collections import namedtuple
import struct
import logging

log = logging.getLogger(__name__)


class Nmi(object):
    """ Network Manager Interface """
    VERSION = '00DA0209-001, Rev S'
    NM_MT_NULL = 0
    NM_MT_LOOPBACK = 1
    NM_MT_DEVC_TYPE = 2
    NM_MT_COMM_STAT = 3
    NM_MT_DIAG_ALARM = 4
    NM_MT_DIAG_ALARMS = 5
    NM_MT_SENSOR_ALARM = 6
    NM_MT_SENSOR_ALARMS = 7
    NM_MT_CONTROL = 8
    NM_MT_CONTROLS = 9
    NM_MT_STANDBY = 10
    NM_MT_MATE_STAT = 11
    NM_MT_AUDIO_FOLDER = 12
    NM_MT_AUDIO_EVENT = 13
    NM_MT_SHUNT = 14
    NM_MT_SHUNTS = 15
    NM_MT_FILTER_ALARM = 16
    NM_MT_FILTER_ALARMS = 17
    NM_MT_DESC = 18
    NM_MT_DEVC_SMRY = 19
    NM_MT_SENSOR_TRBL = 20
    NM_MT_PRE_ALARMS = 21
    NM_MT_LINK_STAT = 50
    NM_MT_PASSTHRU = 51
    NM_D_LOOPBACK = namedtuple('NM_D_LOOPBACK',
                               'Input')
    NM_D_DEVC_TYPE = namedtuple('NM_D_DEVC_TYPE',
                                'Address DevcType MaxDiag MaxAlarm MaxCtrl')
    NM_NO_DEVC = -1
    NM_D_COMM_STAT = namedtuple('NM_D_COMM_STAT',
                                'Address Connected SideFault')
    NM_D_DIAG_ALARM = namedtuple('NM_D_DIAG_ALARM',
                                 'Address Point Active')
    NM_D_DIAG_ALARMS = namedtuple('NM_D_DIAG_ALARMS',
                                  'Address Points States') #
    NM_D_SENSOR_ALARM = namedtuple('NM_D_SENSOR_ALARM',
                                   'Address Point Status Location')
    NM_D_SENSOR_ALARMS = namedtuple('NM_D_SENSOR_ALARMS',
                                    'Address Points States') #
    NM_D_CONTROL = namedtuple('NM_D_CONTROL',
                              'Address Point Active')
    NM_D_CONTROLS = namedtuple('NM_D_CONTROLS',
                               'Address Points States') #
    NM_D_AUDIO_EVENT = namedtuple('NM_AUDIO_EVENT',
                                  'Channel Pathname Desc')
    NM_D_SHUNT = namedtuple('NM_D_SHUNT',
                            'Address Point Mask State')
    NM_D_SHUNTS = namedtuple('NM_D_SHUNTS',
                             'Address Points States') #
    NM_D_MATE_STAT = namedtuple('NM_D_MATE_STAT',
                                'Status')
    NM_D_FILTER_ALARM = NM_D_SENSOR_ALARM
    NM_D_FILTER_ALARMS = NM_D_SENSOR_ALARMS #
    NM_DEVC_DESC = 0x0
    NM_COMM_DESC = 0x1
    NM_DIAG_DESC = 0x2
    NM_SENS_DESC = 0x3
    NM_CTRL_DESC = 0x4
    NM_SMRY_DESC = 0x5
    NM_USER_DESC = 0x10
    NM_D_DESC = namedtuple('NM_D_DESC',
                           'Address Point Type Desc') #
    NM_D_R_DESC = namedtuple('NM_D_R_DESC', 'Address Point Type')

    NM_MAX_SMRY_PNT = 5
    NM_D_DEVC_SMRY = namedtuple('NM_D_DEVC_SMRY',
                                'Address Summary')
    NM_D_SENSOR_TRBL = namedtuple('NM_D_SENSOR_TRBL',
                                  'Address Points States') #
    NM_D_PRE_ALARMS = namedtuple('NM_D_PRE_ALARMS',
                                 'Address Points States') #
    NM_XF_MIN_ADDR = 0
    NM_XF_MAX_ADDR = 127
    NM_XF_410 = 0x001
    NM_XF_420 = 0x002
    NM_XF_430 = 0x003
    NM_XF_4100 = 0x004
    NM_XF_IFLX = 0x005
    NM_XF_IFLD = 0x006
    NM_XF_410_DIAGS = 0
    NM_XF_410_ALARMS = 64
    NM_XF_410_CONTROLS = 128
    NM_XF_420_DIAGS = 0
    NM_XF_420_ALARMS = 64
    NM_XF_420_CONTROLS = 64
    NM_XF_430_DIAGS = 0
    NM_XF_430_ALARMS = 8
    NM_XF_430_CONTROLS = 8
    NM_XF_4100_DIAGS = 0
    NM_XF_4100_ALARMS = 2
    NM_XF_4100_CONTROLS = 3
    NM_XF_IFLX_DIAGS = 2
    NM_XF_IFLX_ALARMS = 4
    NM_XF_IFLX_CONTROLS = 6
    NM_XF_IFLD_DIAGS = 1
    NM_XF_IFLD_ALARMS = 4
    NM_XF_IFLD_CONTROLS = 8
    NM_SN_MIN_ADDR = 0
    NM_SN_MAX_ADDR = 62
    NM_SN_TU = 0x100
    NM_SN_LTU = 0x101
    NM_SN_SM = 0x103
    NM_SN_IF = 0x105
    NM_SN_NC = 0x106
    NM_SN_TU_DIAGS = 4
    NM_SN_TU_ALARMS = 16
    NM_SN_TU_CONTROLS = 8
    NM_SN_LTU_DIAGS = 3
    NM_SN_LTU_ALARMS = 256
    NM_SN_LTU_CONTROLS = 256
    NM_SN_SM_DIAGS = 9
    NM_SN_SM_ALARMS = 10
    NM_SN_SM_CONTROLS = 6
    NM_SN_IF_DIAGS = 3
    NM_SN_IF_ALARMS = 4
    NM_SN_IF_CONTROLS = 6
    NM_SN_NC_DIAGS = 4
    NM_SN_NC_ALARMS = 0
    NM_SN_NC_CONTROLS = 0
    NM_AG_MIN_ADDR = 1
    NM_AG_MAX_ADDR = 60
    NM_AG_NIU = 0x200
    NM_AG_OTRX = 0x201
    NM_AG_OTRX_LT = 0x202
    NM_AG_XFLD = 0x203
    NM_AG_IO16 = 0x204
    NM_AG_TFDIDS = 0x205
    NM_AG_4100 = 0x206
    NM_AG_FLXPS = 0x207
    NM_AG_UWAVE = 0x208
    NM_AG_ULIO = 0x209
    NM_AG_XFLD_LT = 0x20A
    NM_AG_FLXZ20 = 0x20B
    NM_AG_FLXPS_SC = 0x20C
    NM_AG_FLXZ4 = 0x20D
    NM_AG_AMUX = 0x20E
    NM_AG_FLXZN = 0x20F
    NM_AG_RBX510 = 0x210
    NM_AG_ALE = 0x211
    NM_AG_IO16_DIAGS = 8
    NM_AG_IO16_ALARMS = 16
    NM_AG_IO16_CONTROLS = 16
    NM_AG_ALE_DIAGS = 0
    NM_AG_ALE_ALARMS = 400
    NM_AG_ALE_CONTROLS = 400
    NM_AG_AMUX_DIAGS = 0
    NM_AG_AMUX_ALARMS = 0
    NM_AG_AMUX_CONTROLS = 100
    NM_AG_FLXPS_DIAGS = 7
    NM_AG_FLXPS_ALARMS = 4
    NM_AG_FLXPS_CONTROLS = 8
    NM_AG_FLXZ4_DIAGS = 42
    NM_AG_FLXZ4_ALARMS = 14
    NM_AG_FLXZ4_CONTROLS = 4
    NM_AG_FLXZ20_DIAGS = 42
    NM_AG_FLXZ20_ALARMS = 30
    NM_AG_FLXZ20_CONTROLS = 4
    NM_AG_FLXZN_DIAGS = 42
    NM_AG_FLXZN_ALARMS = 70
    NM_AG_FLXZN_CONTROLS = 4
    NM_AG_FLXZN_LOCN = namedtuple('NM_AG_FLXZN_LOCN',
                                  'Meter Side Active')

    NM_AG_4100_DIAGS = 0
    NM_AG_4100_ALARMS = 2
    NM_AG_4100_CONTROLS = 3
    NM_AG_NIU_DIAGS = 12
    NM_AG_NIU_ALARMS = 0
    NM_AG_NIU_CONTROLS = 0
    NM_AG_OTRX_DIAGS = 15
    NM_AG_OTRX_ALARMS = 60
    NM_AG_OTRX_CONTROLS = 12
    NM_AG_OTRX_LOCN = namedtuple('NM_AG_OTRX_LOCN',
                                 'Meter Side Active')
    NM_AG_OTRX_LT_DIAGS = 15
    NM_AG_OTRX_LT_ALARMS = 15
    NM_AG_OTRX_LT_CONTROLS = 12
    NM_AG_OTRX_LT_LOCN = NM_AG_OTRX_LOCN
    NM_AG_RBX510_DIAGS = 0
    NM_AG_RBX510_ALARMS = 8
    NM_AG_RBX510_CONTROLS = 8
    NM_AG_ULIO_DIAGS = 44
    NM_AG_ULIO_ALARMS = 264
    NM_AG_ULIO_CONTROLS = 264
    NM_AG_UWAVE_DIAGS = 16
    NM_AG_UWAVE_ALARMS = 2
    NM_AG_UWAVE_CONTROLS = 3
    NM_AG_XFLD_DIAGS = 18
    NM_AG_XFLD_ALARMS = 12
    NM_AG_XFLD_CONTROLS = 14
    NM_MX_MIN_ADDR = 0
    NM_MX_MAX_ADDR = 120
    NM_MX_5000 = 0x300
    NM_MX_ZN = 0x301
    NM_MX_5000_DIAGS = 3
    NM_MX_5000_ALARMS = 0
    NM_MX_5000_CONTROLS = 1
    NM_MX_ZN_DIAGS = 1
    NM_MX_ZN_ALARMS = 1
    NM_MX_ZN_CONTROLS = 3
    NM_VO_MIN_ADDR = 1
    NM_VO_MAX_ADDR = 200
    NM_VO_IPCC = 0x400
    NM_VO_IPCC_G1 = 0x400
    NM_VO_IPCC_G2 = 0x401
    NM_VO_IPCC_PA = 0x402
    NM_VO_IPCC_DIAGS = 4
    NM_VO_IPCC_ALARMS = 4
    NM_VO_IPCC_CONTROLS = 18
    NM_SX_MIN_ADDR = 0
    NM_SX_MAX_ADDR = 16
    NM_SX_CM = 0x500
    NM_SX_TM = 0x501
    NM_SX_CM_DIAGS = 11
    NM_SX_CM_ALARMS = 0
    NM_SX_CM_CONTROLS = 33
    NM_SX_TM_DIAGS = 1
    NM_SX_TM_ALARMS = 6
    NM_SX_TM_CONTROLS = 4
    NM_C3_MIN_ADDR = 0
    NM_C3_MAX_ADDR = 127
    NM_C3_FOST = 0x600
    NM_C3_GPRU = 0x601
    NM_C3_SPRU = 0x602
    NM_C3_VPRU = 0x603
    NM_C3_YAEL = 0x604
    NM_C3_FOST_DIAGS = 1
    NM_C3_FOST_ALARMS = 4
    NM_C3_FOST_CONTROLS = 1
    NM_C3_GPRU_DIAGS = 0
    NM_C3_GPRU_ALARMS = 8
    NM_C3_GPRU_CONTROLS = 10
    NM_C3_SPRU_DIAGS = 1
    NM_C3_SPRU_ALARMS = 6
    NM_C3_SPRU_CONTROLS = 1
    NM_C3_VPRU_DIAGS = 2
    NM_C3_VPRU_ALARMS = 4
    NM_C3_VPRU_CONTROLS = 3
    NM_C3_YAEL_DIAGS = 4
    NM_C3_YAEL_ALARMS = 1
    NM_C3_YAEL_CONTROLS = 4
    NM_FP_MIN_ADDR = 1
    NM_FP_MAX_ADDR = 10
    NM_FP_SU = 0x700
    NM_FP_SU_DIAGS = 10
    NM_FP_SU_ALARMS = 480
    NM_FP_SU_CONTROLS = 0
    NM_FP_SU_LOCN = namedtuple('NM_FU_SU_LOCN',
                               'Active Posn Lat Long Alt')

    NM_FLR_MIN_ADDR = NM_FP_MIN_ADDR
    NM_FLR_MAX_ADDR = NM_FP_MAX_ADDR
    NM_FLR_SU = NM_FP_SU
    NM_FLR_SU_DIAGS = NM_FP_SU_DIAGS
    NM_FLR_SU_ALARMS = NM_FP_SU_ALARMS
    NM_FLR_SU_CONTROLS = NM_FP_SU_CONTROLS
    NM_FLR_SU_LOCN = NM_FP_SU_LOCN
    NM_KR_MIN_ADDR = 1
    NM_KR_MAX_ADDR = 200
    NM_KR_SU = 0x800
    NM_KR_SU_DIAGS = 10
    NM_KR_SU_ALARMS = 1
    NM_KR_SU_CONTROLS = 2
    PPD_Event = namedtuple('PPD_Event',
                           'Event Id Type Altitude Temp RSSI1 RSSI2')
    NM_SC_MIN_ADDR = 0
    NM_SC_MAX_ADDR = 0
    NM_SC_DEV = 0x900
    NM_SC_DEV_DIAGS = 5
    NM_SC_DEV_ALARMS = 1024
    NM_SC_DEV_CONTROLS = 1024

    # NM_HEAD = b'\xE0\x31'
    NM_HEAD = 0x31E0
    MIN_PACK_LENGTH = 5

    NM_D_ADDRESS = namedtuple('NM_D_ADDRESS',
                              'Address')
    NM_D_LOOPBACK = namedtuple('NM_D_LOOPBACK',
                               'Values')
    NM_D_ADDRESS_ALARM = namedtuple('NM_D_ADDRESS_ALARM', 'Address Alarm')
    dispatch = {
        NM_MT_NULL: {
            'query': ('', None),
            'respone': ('', None)
        },
        NM_MT_LOOPBACK: {
            'query': ('<H', NM_D_ADDRESS),
            'respone': ('<H', NM_D_LOOPBACK)
        },
        NM_MT_DEVC_TYPE: {
            'query': ('<H', NM_D_ADDRESS),
            'respone': ('<HHHHH', NM_D_DEVC_TYPE)
        },
        NM_MT_COMM_STAT: {
            'query': ('<H', NM_D_ADDRESS),
            'respone': ('<HBB', NM_D_COMM_STAT)
        },
        NM_MT_DIAG_ALARM: {
            'query': ('', None),
            'respone': ('<HH', NM_D_DIAG_ALARM)
        },
        NM_MT_DIAG_ALARMS: {
            'query': ('<H', NM_D_ADDRESS),
            'respone': ('<HHB', NM_D_DIAG_ALARMS)
        },
        NM_MT_SENSOR_ALARM: {
            'query': ('<HH', NM_D_ADDRESS_ALARM),
            'respone': ('<HHBH', NM_D_SENSOR_ALARM)
        },
        NM_MT_SENSOR_ALARMS: {
            'query': ('<H', NM_D_ADDRESS),
            'respone': ('<HH', NM_D_SENSOR_ALARMS)
        },
        NM_MT_CONTROL: {
            'query': ('<HHB', NM_D_CONTROL),
            'respone': ('<HH', NM_D_CONTROL)
        },
        NM_MT_CONTROLS: {
            'query': ('<H', NM_D_ADDRESS),
            'respone': ('<HH', NM_D_CONTROLS)
        },
        NM_MT_STANDBY: {
            'query': ('', None),
            'respone': ('', None)
        },
        NM_MT_MATE_STAT: {
            'query': ('', None),
            'respone': ('<B', NM_D_MATE_STAT)
        },
        NM_MT_AUDIO_FOLDER: {
            'query': ('<H', NM_D_ADDRESS),
            'respone': ('', None)
        },
        NM_MT_AUDIO_EVENT: {
            'query': ('', None),
            'respone': ('<HHH', NM_D_AUDIO_EVENT)
        },
        NM_MT_SHUNT: {
            'query': ('', None),
            'respone': ('<HHBB', NM_D_SHUNT)
        },
        NM_MT_SHUNTS: {
            'query': ('<H', NM_D_ADDRESS),
            'respone': ('<HH', NM_D_SHUNTS)
        },
        NM_MT_FILTER_ALARM: {
            'query': ('<HH', NM_D_ADDRESS_ALARM),
            'respone': ('<HHBH', NM_D_FILTER_ALARM)
        },
        NM_MT_FILTER_ALARMS: {
            'query': ('<H', NM_D_ADDRESS),
            'respone': ('<HH', NM_D_FILTER_ALARMS)
        },
        NM_MT_DESC: {
            'query': ('<HHB', NM_D_R_DESC),
            'respone': ('<HHB', NM_D_DESC)
        },
        NM_MT_DEVC_SMRY: {
            'query': ('<H', NM_D_ADDRESS),
            'respone': ('<HB', NM_D_DEVC_SMRY)
        },
        NM_MT_SENSOR_TRBL: {
            'query': ('<H', NM_D_ADDRESS),
            'respone': ('<HH', NM_D_SENSOR_TRBL)
        },
        NM_MT_PRE_ALARMS: {
            'query': ('<H', NM_D_ADDRESS),
            'respone': ('<HH', NM_D_PRE_ALARMS)
        },
        NM_MT_LINK_STAT: {
            'query': ('', None),
            'respone': ('', None)
        },
        NM_MT_PASSTHRU: {
            'query': ('', None),
            'respone': ('', None)
        },
    }

    def __init__(self):
        pass

    def __str__(self):
        return "Network Manager Interface {self.VERSION}"

    def _build(self, cmd, payload=b''):
        cmd_str = struct.pack('<HHB',
                              self.NM_HEAD,
                              len(payload) + 1,
                              cmd)
        return cmd_str + payload

    def get_cmd(self, message):
        s = struct.Struct('<HHB')
        (h, l, cmd) = s.unpack(message[:5])
        return (cmd, message[5:4+l])

    def is_invalid(self, message):
        if len(message) < self.MIN_PACK_LENGTH:
            return True
        s = struct.Struct('<HH')
        (h, l) = s.unpack(message[:4])
        if h != self.NM_HEAD or len(message[4:]) < l:
            return True
        return False


class NmiClient(Nmi):
    """ Client for Network Manager Interface """

    def __init__(self):
        super().__init__()

    def request(self, cmd, *args, **kwargs):
        if cmd in self.dispatch:
            fmt = kwargs.get('fmt')
            if not fmt:
                (fmt, _) = self.dispatch.get(cmd).get('query')
            try:
                payload = fmt and struct.pack(fmt, *args) or b''
            except struct.error as e:
                log.error(f'{e}')
                return None
            return self._build(cmd, payload)
        else:
            return False

    def parse(self, message):
        if self.is_invalid(message):
            return None
        (cmd, payload) = self.get_cmd(message)
        if cmd in self.dispatch:
            (fmt, data_struct) = self.dispatch.get(cmd).get('respone')
            try:
                missing = len(payload) - struct.calcsize(fmt)
                if missing > 0:
                    fmt += '{}s'.format(missing)
                d = struct.unpack(fmt, payload)
            except struct.error as e:
                log.error(f'{e}')
                return None
            arg = data_struct and data_struct._make(d) or None
            return (cmd, arg)


class NmiServer(Nmi):
    """ Server for Network Manager Interface """

    def __init__(self, dev_type):
        super().__init__()
        self.dev_type = dev_type

    def choose(self):
        if self.dev_type == 'NM_XF_430':
            device = self.NM_XF_430
            diags = self.NM_XF_430_DIAGS
            alarms = self.NM_XF_430_ALARMS
            controls = self.NM_XF_430_CONTROLS
        return (device, diags, alarms, controls)

    def respone(self, cmd, *args, **kwargs):
        if cmd in self.dispatch:
            fmt = kwargs.get('fmt')
            if not fmt:
                (fmt, _) = self.dispatch.get(cmd).get('respone')
            try:
                payload = fmt and struct.pack(fmt, *args) or b''
            except struct.error as e:
                log.error(f'{e}')
                return None
            return self._build(cmd, payload)
        else:
            return False

    def parse(self, message):
        if self.is_invalid(message):
            return None
        (cmd, payload) = self.get_cmd(message)
        if cmd in self.dispatch:
            (fmt, data_struct) = self.dispatch.get(cmd).get('query')
            try:
                d = fmt and struct.unpack(fmt, payload) or None
            except struct.error as e:
                log.error(f'{e}')
                return None
            arg = data_struct and data_struct._make(d) or None
            return (cmd, arg)


if __name__ == '__main__':
    client = NmiClient()
    server = NmiServer('NM_XF_430')
    server.choose()
    x = client.request(client.NM_MT_NULL)
    print(x)
    y = server.parse(x)
    print(y)
    x = client.request(client.NM_MT_LOOPBACK, 0xFF)
    print(" ".join('{0:X}'.format(i) for i in x))
    x = client.request(client.NM_MT_DEVC_TYPE, 1)
    print('--------------', x)
    y = server.parse(x)
    x = server.respone(server.NM_MT_LOOPBACK, 1)
    print(x)
    n = server.NM_D_DEVC_TYPE(1, 2, 3, 4, 5)
    x = server.respone(server.NM_MT_DEVC_TYPE, *n)
    print(x)
    y = client.parse(x)
    print(y)
    y = client.parse(b'\xE0\x31\x07\x00\x07\x03\x00\x06\x00\x55\x02\x09')
    print('Pack data: {}'.format(y))
    n = server.NM_D_SENSOR_ALARMS(1, 2, 3)
    x = server.respone(server.NM_MT_DIAG_ALARMS, 1, 6, 597, fmt='<HHH')
    print('Server send is: {}'.format(x))
    x = server.respone(server.NM_MT_SENSOR_ALARMS, 1, 2)
    print(x)
