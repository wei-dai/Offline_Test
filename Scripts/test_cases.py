#!/usr/bin/python

import global_parameters as gp

suit = {
    'CommDefault': ['Communication', 'None', 'None'],
    'CommScreenShare': ['Communication', '{\"che.video.video_content\":2}', 'None'],
    'LiveDefault': ['Live', 'None', 'None'],
    'LiveScreenShare': ['Live', '{\"che.video.video_content\":2}', 'None'],
    'LiveWebInterOp': ['Live', '{\"che.video.web_h264_interop_enable\":true}', 'None']
}


def generate_case_name(scenario, mode, number):
    return scenario + gp.folder_join + mode + gp.folder_join + number

if gp.cur_platform == 'Linux':
    if gp.on_server == 0:
        cases = [
            [generate_case_name('CommDefault', 'Regression', '0000'), 2, 6, ['640x360']*2, [200,  400], [15]*2, [0]*2, ['AzureLow']*2],
            [generate_case_name('CommDefault', 'Overnight', '0000'), 2, 15, ['640x360']*2, [200,  400], [15]*2, [0]*2, ['AzureLow']*2],

            [generate_case_name('LiveDefault', 'Regression', '0000'), 2, 6, ['640x360']*2, [800, 1200], [15]*2, [0]*2, ['AzureLow']*2],
            [generate_case_name('LiveDefault', 'Overnight', '0000'), 2, 15, ['640x360']*2, [800, 1200], [15]*2, [0]*2, ['AzureLow']*2],

            [generate_case_name('CommScreenShare', 'Regression', '0000'), 2, 6, ['576x360']*2, [ 1000]*2, [ 5]*2, [0]*2, ['WikiText']*2],
            [generate_case_name('CommScreenShare', 'Overnight', '0000'),  2, 15, ['576x360']*2, [ 1000]*2, [ 5]*2, [0]*2, ['WikiText']*2],

            [generate_case_name('LiveScreenShare', 'Regression', '0000'), 2, 6, ['576x360']*2, [ 1000]*2, [ 5]*2, [0]*2, ['WikiText']*2],
            [generate_case_name('LiveScreenShare', 'Overnight', '0000'),  2, 15, ['576x360']*2, [ 1000]*2, [ 5]*2, [0]*2, ['WikiText']*2],

            [generate_case_name('LiveWebInterOp', 'Regression', '0000'), 2, 6, ['640x360']*2, [800, 1200], [15]*2, [0]*2, ['AzureLow']*2],
            [generate_case_name('LiveWebInterOp', 'Overnight', '0000'), 2, 15, ['640x360']*2, [800, 1200], [15]*2, [0]*2, ['AzureLow']*2],
        ]
    else:
        cases = [
            [generate_case_name('CommDefault', 'Regression', '0000'), 2, 30, [  '120x120']*2, [  12,   25], [ 5]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0001'), 2, 30, [  '120x120']*2, [  12,   25], [ 5]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0002'), 2, 30, [  '120x120']*2, [  25,   50], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0003'), 2, 30, [  '120x120']*2, [  25,   50], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0004'), 1, 30, [  '120x120']  , [  12]      , [ 5]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Regression', '0005'), 1, 30, [  '120x120']  , [  50]      , [15]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Regression', '0100'), 2, 30, [  '160x120']*2, [  15,   30], [ 5]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0101'), 2, 30, [  '160x120']*2, [  15,   30], [ 5]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0102'), 2, 30, [  '160x120']*2, [  30,   60], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0103'), 2, 30, [  '160x120']*2, [  30,   60], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0104'), 1, 30, [  '160x120']  , [  15]      , [ 5]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Regression', '0105'), 1, 30, [  '160x120']  , [  60]      , [15]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Regression', '0200'), 2, 30, [  '180x180']*2, [  25,   50], [ 5]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0201'), 2, 30, [  '180x180']*2, [  25,   50], [ 5]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0202'), 2, 30, [  '180x180']*2, [  50,  100], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0203'), 2, 30, [  '180x180']*2, [  50,  100], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0204'), 1, 30, [  '180x180']  , [  25]      , [ 5]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Regression', '0205'), 1, 30, [  '180x180']  , [ 100]      , [15]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Regression', '0300'), 2, 30, [  '240x180']*2, [  30,   60],  [5]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0301'), 2, 30, [  '240x180']*2, [  30,   60],  [5]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0302'), 2, 30, [  '240x180']*2, [  60,  120], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0303'), 2, 30, [  '240x180']*2, [  60,  120], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0304'), 1, 30, [  '240x180']  , [  30]      , [ 5]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Regression', '0305'), 1, 30, [  '240x180']  , [ 120]      , [15]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Regression', '0400'), 2, 30, [  '320x180']*2, [  35,   70],  [5]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0401'), 2, 30, [  '320x180']*2, [  35,   70],  [5]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0402'), 2, 30, [  '320x180']*2, [  70,  140], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0403'), 2, 30, [  '320x180']*2, [  70,  140], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0404'), 1, 30, [  '320x180']  , [  35]      , [ 5]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Regression', '0405'), 1, 30, [  '320x180']  , [ 140]      , [15]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Regression', '0500'), 2, 30, [  '240x240']*2, [  35,   70],  [5]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0501'), 2, 30, [  '240x240']*2, [  35,   70],  [5]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0502'), 2, 30, [  '240x240']*2, [  70,  140], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0503'), 2, 30, [  '240x240']*2, [  70,  140], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0504'), 1, 30, [  '240x240']  , [  35]      , [ 5]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Regression', '0505'), 1, 30, [  '240x240']  , [ 140]      , [15]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Regression', '0600'), 2, 30, [  '320x240']*2, [  45,   90],  [5]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0601'), 2, 30, [  '320x240']*2, [  45,   90],  [5]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0602'), 2, 30, [  '320x240']*2, [  90,  180], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0603'), 2, 30, [  '320x240']*2, [  90,  180], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0604'), 1, 30, [  '320x240']  , [  45]      , [ 5]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Regression', '0605'), 1, 30, [  '320x240']  , [ 180]      , [15]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Regression', '0700'), 2, 30, [  '424x240']*2, [  55,  110],  [5]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0701'), 2, 30, [  '424x240']*2, [  55,  110],  [5]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0702'), 2, 30, [  '424x240']*2, [ 110,  220], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0703'), 2, 30, [  '424x240']*2, [ 110,  220], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0704'), 1, 30, [  '424x240']  , [  55]      , [ 5]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Regression', '0705'), 1, 30, [  '424x240']  , [ 220]      , [15]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Regression', '0800'), 2, 30, [  '360x360']*2, [  65,  130],  [5]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0801'), 2, 30, [  '360x360']*2, [  65,  130],  [5]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0802'), 2, 30, [  '360x360']*2, [ 130,  260], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0803'), 2, 30, [  '360x360']*2, [ 130,  260], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0804'), 1, 30, [  '360x360']  , [  65]      , [ 5]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Regression', '0805'), 1, 30, [  '360x360']  , [ 260]      , [15]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Regression', '0900'), 2, 30, [  '640x360']*2, [ 200,  400], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0901'), 2, 30, [  '640x360']*2, [ 200,  400], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0902'), 2, 30, [  '640x360']*2, [ 300,  600], [30]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0903'), 2, 30, [  '640x360']*2, [ 300,  600], [30]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0904'), 1, 30, [  '640x360']  , [ 200]      , [15]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Regression', '0905'), 1, 30, [  '640x360']  , [ 600]      , [30]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Regression', '0A00'), 2, 30, [  '480x480']*2, [ 200,  400], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0A01'), 2, 30, [  '480x480']*2, [ 200,  400], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0A02'), 2, 30, [  '480x480']*2, [ 300,  600], [30]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0A03'), 2, 30, [  '480x480']*2, [ 300,  600], [30]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0A04'), 1, 30, [  '480x480']  , [ 200]      , [15]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Regression', '0A05'), 1, 30, [  '480x480']  , [ 600]      , [30]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Regression', '0B00'), 2, 30, [  '640x480']*2, [ 250,  500], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0B01'), 2, 30, [  '640x480']*2, [ 250,  500], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0B02'), 2, 30, [  '640x480']*2, [ 375,  750], [30]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0B03'), 2, 30, [  '640x480']*2, [ 375,  750], [30]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0B04'), 1, 30, [  '640x480']  , [ 250]      , [15]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Regression', '0B05'), 1, 30, [  '640x480']  , [ 750]      , [30]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Regression', '0C00'), 2, 30, [  '848x480']*2, [ 300,  600], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0C01'), 2, 30, [  '848x480']*2, [ 300,  600], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0C02'), 2, 30, [  '848x480']*2, [ 450,  900], [30]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0C03'), 2, 30, [  '848x480']*2, [ 450,  900], [30]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Regression', '0C04'), 1, 30, [  '848x480']  , [ 300]      , [15]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Regression', '0C05'), 1, 30, [  '848x480']  , [ 900]      , [30]  , [0]  , ['AzureMedium']             ],

            # [generate_case_name('CommDefault', 'Regression', '0D00'), 2, 30, [  '960x720']*2, [ 480,  960], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            # [generate_case_name('CommDefault', 'Regression', '0D01'), 2, 30, [  '960x720']*2, [ 480,  960], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            # [generate_case_name('CommDefault', 'Regression', '0D02'), 2, 30, [  '960x720']*2, [ 720, 1440], [30]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            # [generate_case_name('CommDefault', 'Regression', '0D03'), 2, 30, [  '960x720']*2, [ 720, 1440], [30]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            # [generate_case_name('CommDefault', 'Regression', '0D04'), 1, 30, [  '960x720']  , [ 480]      , [15]  , [0]  , ['AzureLow']                ],
            # [generate_case_name('CommDefault', 'Regression', '0D05'), 1, 30, [  '960x720']  , [1440]      , [30]  , [0]  , ['AzureMedium']             ],

            # [generate_case_name('CommDefault', 'Regression', '0E00'), 2, 30, [ '1280x720']*2, [ 600, 1200], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            # [generate_case_name('CommDefault', 'Regression', '0E01'), 2, 30, [ '1280x720']*2, [ 600, 1200], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            # [generate_case_name('CommDefault', 'Regression', '0E02'), 2, 30, [ '1280x720']*2, [ 900, 1800], [30]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            # [generate_case_name('CommDefault', 'Regression', '0E03'), 2, 30, [ '1280x720']*2, [ 900, 1800], [30]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            # [generate_case_name('CommDefault', 'Regression', '0E04'), 1, 30, [ '1280x720']  , [ 600]      , [15]  , [0]  , ['AzureLow']                ],
            # [generate_case_name('CommDefault', 'Regression', '0E05'), 1, 30, [ '1280x720']  , [1800]      , [30]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Regression', '1200'), 2, 30, [  '640x360']*2, [ 400]*2, [15]*2, [0, 4]           , ['AzureMedium']*2],
            [generate_case_name('CommDefault', 'Regression', '1201'), 4, 30, [  '640x360']*4, [ 400]*4, [15]*4, [0]*2+[4]*2      , ['AzureMedium']*4],
            [generate_case_name('CommDefault', 'Regression', '1202'), 6, 30, [  '640x360']*6, [ 400]*6, [15]*6, [0]*2+[3]*2+[6]*2, ['AzureMedium']*6],

            [generate_case_name('CommDefault', 'Regression', '1300'), 2, 60, [  '640x360']*2, [ 400]*2, [15]*2, [0, 7]           , ['AzureMedium']*2],
            [generate_case_name('CommDefault', 'Regression', '1301'), 4, 60, [  '640x360']*4, [ 400]*4, [15]*4, [0]*2+[7]*2      , ['AzureMedium']*4],

            [generate_case_name('LiveDefault', 'Regression', '0000'), 4, 30, [  '120x120']*4, [   37,    50,    62,    75],  [5]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Regression', '0001'), 4, 30, [  '120x120']*4, [   75,   100,   125,   150], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveDefault', 'Regression', '0100'), 4, 30, [  '160x120']*4, [   45,    60,    75,    90],  [5]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Regression', '0101'), 4, 30, [  '160x120']*4, [   90,   120,   150,   180], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveDefault', 'Regression', '0200'), 4, 30, [  '180x180']*4, [   75,   100,   125,   150],  [5]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Regression', '0201'), 4, 30, [  '180x180']*4, [  150,   200,   250,   300], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveDefault', 'Regression', '0300'), 4, 30, [  '240x180']*4, [   90,   120,   150,   180],  [5]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Regression', '0301'), 4, 30, [  '240x180']*4, [  180,   240,   300,   360], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveDefault', 'Regression', '0400'), 4, 30, [  '320x180']*4, [  105,   140,   175,   210],  [5]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Regression', '0401'), 4, 30, [  '320x180']*4, [  210,   280,   350,   420], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveDefault', 'Regression', '0500'), 4, 30, [  '240x240']*4, [  105,   140,   175,   210],  [5]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Regression', '0501'), 4, 30, [  '240x240']*4, [  210,   280,   350,   420], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveDefault', 'Regression', '0600'), 4, 30, [  '320x240']*4, [  135,   180,   225,   270],  [5]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Regression', '0601'), 4, 30, [  '320x240']*4, [  270,   360,   450,   540], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveDefault', 'Regression', '0700'), 4, 30, [  '424x240']*4, [  165,   220,   275,   330],  [5]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Regression', '0701'), 4, 30, [  '424x240']*4, [  330,   440,   550,   660], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveDefault', 'Regression', '0800'), 4, 30, [  '360x360']*4, [  195,   260,   325,   390],  [5]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Regression', '0801'), 4, 30, [  '360x360']*4, [  390,   520,   650,   780], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveDefault', 'Regression', '0900'), 4, 30, [  '640x360']*4, [  600,   800,  1000,  1200], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Regression', '0901'), 4, 30, [  '640x360']*4, [  900,  1200,  1500,  1800], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveDefault', 'Regression', '0A00'), 4, 30, [  '480x480']*4, [  600,   800,  1000,  1200], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Regression', '0A01'), 4, 30, [  '480x480']*4, [  900,  1200,  1500,  1800], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveDefault', 'Regression', '0B00'), 4, 30, [  '640x480']*4, [  750,  1000,  1250,  1500], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Regression', '0B01'), 4, 30, [  '640x480']*4, [ 1125,  1500,  1875,  2250], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveDefault', 'Regression', '0C00'), 4, 30, [  '848x480']*4, [  900,  1200,  1500,  1800], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Regression', '0C01'), 4, 30, [  '848x480']*4, [ 1350,  1800,  2250,  2700], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            # [generate_case_name('LiveDefault', 'Regression', '0D00'), 4, 30, [  '960x720']*4, [ 1440,  1920,  2400,  2880], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            # [generate_case_name('LiveDefault', 'Regression', '0D01'), 4, 30, [  '960x720']*4, [ 2160,  2880,  3600,  4320], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            # [generate_case_name('LiveDefault', 'Regression', '0E00'), 4, 30, [ '1280x720']*4, [ 1800,  2400,  3000,  3600], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            # [generate_case_name('LiveDefault', 'Regression', '0E01'), 4, 30, [ '1280x720']*4, [ 2700,  3600,  4500,  5400], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            # Regression currently does not support resolution higher than 720P
            # [generate_case_name('LiveDefault', 'Regression', '0F00'), 4, 30, ['1920x1080']*4, [ 3000,  4000,  5000,  6000], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            # [generate_case_name('LiveDefault', 'Regression', '0F01'), 4, 30, ['1920x1080']*4, [ 4500,  6000,  7500,  9000], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            # [generate_case_name('LiveDefault', 'Regression', '1000'), 4, 30, ['2560x1440']*4, [ 4800,  6400,  8000,  9600], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            # [generate_case_name('LiveDefault', 'Regression', '1001'), 4, 30, ['2560x1440']*4, [ 7200,  9600, 12000, 14400], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            # [generate_case_name('LiveDefault', 'Regression', '1100'), 4, 30, ['3840x2160']*4, [ 9000, 12000, 15000, 18000], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            # [generate_case_name('LiveDefault', 'Regression', '1101'), 4, 30, ['3840x2160']*4, [13500, 18000, 22500, 27000], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('CommScreenShare', 'Regression', '0000'), 2, 30, ['960x600']*2, [ 1000]*2, [ 5]*2, [0]*2, ['WikiText']*2],
            [generate_case_name('CommScreenShare', 'Regression', '0001'), 2, 30, ['960x600']*2, [ 1000]*2, [ 5]*2, [4]*2, ['WikiText']*2],
            [generate_case_name('CommScreenShare', 'Regression', '0002'), 2, 30, ['960x600']*2, [ 1000]*2, [10]*2, [0]*2, ['WikiText']*2],
            [generate_case_name('CommScreenShare', 'Regression', '0003'), 2, 30, ['960x600']*2, [ 1000]*2, [10]*2, [4]*2, ['WikiText']*2],

            [generate_case_name('LiveScreenShare', 'Regression', '0000'), 2, 30, ['960x600']*2, [ 1000]*2, [ 5]*2, [0]*2, ['WikiText']*2],
            [generate_case_name('LiveScreenShare', 'Regression', '0001'), 2, 30, ['960x600']*2, [ 1000]*2, [ 5]*2, [4]*2, ['WikiText']*2],
            [generate_case_name('LiveScreenShare', 'Regression', '0002'), 2, 30, ['960x600']*2, [ 1000]*2, [10]*2, [0]*2, ['WikiText']*2],
            [generate_case_name('LiveScreenShare', 'Regression', '0003'), 2, 30, ['960x600']*2, [ 1000]*2, [10]*2, [4]*2, ['WikiText']*2],

            [generate_case_name('LiveWebInterOp', 'Regression', '0000'), 4, 30, [  '640x360']*4, [  600,   800,  1000,  1200], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveWebInterOp', 'Regression', '0001'), 4, 30, [  '640x360']*4, [  900,  1200,  1500,  1800], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveWebInterOp', 'Regression', '0100'), 4, 30, [  '480x480']*4, [  600,   800,  1000,  1200], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveWebInterOp', 'Regression', '0101'), 4, 30, [  '480x480']*4, [  900,  1200,  1500,  1800], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveWebInterOp', 'Regression', '0200'), 4, 30, [  '640x480']*4, [  750,  1000,  1250,  1500], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveWebInterOp', 'Regression', '0201'), 4, 30, [  '640x480']*4, [ 1125,  1500,  1875,  2250], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveWebInterOp', 'Regression', '0300'), 4, 30, [  '848x480']*4, [  900,  1200,  1500,  1800], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveWebInterOp', 'Regression', '0301'), 4, 30, [  '848x480']*4, [ 1350,  1800,  2250,  2700], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('CommDefault', 'Overnight', '0000'), 2, 120, [  '120x120']*2, [  12,   25], [ 5]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0001'), 2, 120, [  '120x120']*2, [  12,   25], [ 5]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0002'), 2, 120, [  '120x120']*2, [  25,   50], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0003'), 2, 120, [  '120x120']*2, [  25,   50], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0004'), 1, 120, [  '120x120']  , [  12]      , [ 5]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Overnight', '0005'), 1, 120, [  '120x120']  , [  50]      , [15]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Overnight', '0100'), 2, 120, [  '160x120']*2, [  15,   30], [ 5]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0101'), 2, 120, [  '160x120']*2, [  15,   30], [ 5]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0102'), 2, 120, [  '160x120']*2, [  30,   60], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0103'), 2, 120, [  '160x120']*2, [  30,   60], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0104'), 1, 120, [  '160x120']  , [  15]      , [ 5]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Overnight', '0105'), 1, 120, [  '160x120']  , [  60]      , [15]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Overnight', '0200'), 2, 120, [  '180x180']*2, [  25,   50], [ 5]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0201'), 2, 120, [  '180x180']*2, [  25,   50], [ 5]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0202'), 2, 120, [  '180x180']*2, [  50,  100], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0203'), 2, 120, [  '180x180']*2, [  50,  100], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0204'), 1, 120, [  '180x180']  , [  25]      , [ 5]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Overnight', '0205'), 1, 120, [  '180x180']  , [ 100]      , [15]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Overnight', '0300'), 2, 120, [  '240x180']*2, [  30,   60],  [5]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0301'), 2, 120, [  '240x180']*2, [  30,   60],  [5]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0302'), 2, 120, [  '240x180']*2, [  60,  120], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0303'), 2, 120, [  '240x180']*2, [  60,  120], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0304'), 1, 120, [  '240x180']  , [  30]      , [ 5]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Overnight', '0305'), 1, 120, [  '240x180']  , [ 120]      , [15]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Overnight', '0400'), 2, 120, [  '320x180']*2, [  35,   70],  [5]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0401'), 2, 120, [  '320x180']*2, [  35,   70],  [5]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0402'), 2, 120, [  '320x180']*2, [  70,  140], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0403'), 2, 120, [  '320x180']*2, [  70,  140], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0404'), 1, 120, [  '320x180']  , [  35]      , [ 5]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Overnight', '0405'), 1, 120, [  '320x180']  , [ 140]      , [15]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Overnight', '0500'), 2, 120, [  '240x240']*2, [  35,   70],  [5]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0501'), 2, 120, [  '240x240']*2, [  35,   70],  [5]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0502'), 2, 120, [  '240x240']*2, [  70,  140], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0503'), 2, 120, [  '240x240']*2, [  70,  140], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0504'), 1, 120, [  '240x240']  , [  35]      , [ 5]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Overnight', '0505'), 1, 120, [  '240x240']  , [ 140]      , [15]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Overnight', '0600'), 2, 120, [  '320x240']*2, [  45,   90],  [5]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0601'), 2, 120, [  '320x240']*2, [  45,   90],  [5]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0602'), 2, 120, [  '320x240']*2, [  90,  180], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0603'), 2, 120, [  '320x240']*2, [  90,  180], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0604'), 1, 120, [  '320x240']  , [  45]      , [ 5]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Overnight', '0605'), 1, 120, [  '320x240']  , [ 180]      , [15]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Overnight', '0700'), 2, 120, [  '424x240']*2, [  55,  110],  [5]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0701'), 2, 120, [  '424x240']*2, [  55,  110],  [5]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0702'), 2, 120, [  '424x240']*2, [ 110,  220], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0703'), 2, 120, [  '424x240']*2, [ 110,  220], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0704'), 1, 120, [  '424x240']  , [  55]      , [ 5]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Overnight', '0705'), 1, 120, [  '424x240']  , [ 220]      , [15]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Overnight', '0800'), 2, 120, [  '360x360']*2, [  65,  130],  [5]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0801'), 2, 120, [  '360x360']*2, [  65,  130],  [5]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0802'), 2, 120, [  '360x360']*2, [ 130,  260], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0803'), 2, 120, [  '360x360']*2, [ 130,  260], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0804'), 1, 120, [  '360x360']  , [  65]      , [ 5]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Overnight', '0805'), 1, 120, [  '360x360']  , [ 260]      , [15]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Overnight', '0900'), 2, 120, [  '640x360']*2, [ 200,  400], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0901'), 2, 120, [  '640x360']*2, [ 200,  400], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0902'), 2, 120, [  '640x360']*2, [ 300,  600], [30]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0903'), 2, 120, [  '640x360']*2, [ 300,  600], [30]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0904'), 1, 120, [  '640x360']  , [ 200]      , [15]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Overnight', '0905'), 1, 120, [  '640x360']  , [ 600]      , [30]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Overnight', '0A00'), 2, 120, [  '480x480']*2, [ 200,  400], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0A01'), 2, 120, [  '480x480']*2, [ 200,  400], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0A02'), 2, 120, [  '480x480']*2, [ 300,  600], [30]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0A03'), 2, 120, [  '480x480']*2, [ 300,  600], [30]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0A04'), 1, 120, [  '480x480']  , [ 200]      , [15]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Overnight', '0A05'), 1, 120, [  '480x480']  , [ 600]      , [30]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Overnight', '0B00'), 2, 120, [  '640x480']*2, [ 250,  500], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0B01'), 2, 120, [  '640x480']*2, [ 250,  500], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0B02'), 2, 120, [  '640x480']*2, [ 375,  750], [30]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0B03'), 2, 120, [  '640x480']*2, [ 375,  750], [30]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0B04'), 1, 120, [  '640x480']  , [ 250]      , [15]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Overnight', '0B05'), 1, 120, [  '640x480']  , [ 750]      , [30]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Overnight', '0C00'), 2, 120, [  '848x480']*2, [ 300,  600], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0C01'), 2, 120, [  '848x480']*2, [ 300,  600], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0C02'), 2, 120, [  '848x480']*2, [ 450,  900], [30]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0C03'), 2, 120, [  '848x480']*2, [ 450,  900], [30]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0C04'), 1, 120, [  '848x480']  , [ 300]      , [15]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Overnight', '0C05'), 1, 120, [  '848x480']  , [ 900]      , [30]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Overnight', '0D00'), 2, 120, [  '960x720']*2, [ 480,  960], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0D01'), 2, 120, [  '960x720']*2, [ 480,  960], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0D02'), 2, 120, [  '960x720']*2, [ 720, 1440], [30]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0D03'), 2, 120, [  '960x720']*2, [ 720, 1440], [30]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0D04'), 1, 120, [  '960x720']  , [ 480]      , [15]  , [0]  , ['AzureLow']                ],
            [generate_case_name('CommDefault', 'Overnight', '0D05'), 1, 120, [  '960x720']  , [1440]      , [30]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Overnight', '0E00'), 2, 120, [ '1280x720']*2, [ 600, 1200], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0E01'), 2, 120, [ '1280x720']*2, [ 600, 1200], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            # [generate_case_name('CommDefault', 'Overnight', '0E02'), 2, 120, [ '1280x720']*2, [ 900, 1800], [30]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            # [generate_case_name('CommDefault', 'Overnight', '0E03'), 2, 120, [ '1280x720']*2, [ 900, 1800], [30]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0E04'), 1, 120, [ '1280x720']  , [ 600]      , [15]  , [0]  , ['AzureLow']                ],
            # [generate_case_name('CommDefault', 'Overnight', '0E05'), 1, 120, [ '1280x720']  , [1800]      , [30]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Overnight', '0F00'), 2, 120, ['1920x1080']*2, [1000, 2000], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0F01'), 2, 120, ['1920x1080']*2, [1000, 2000], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            # [generate_case_name('CommDefault', 'Overnight', '0F02'), 2, 120, ['1920x1080']*2, [1500, 3000], [30]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            # [generate_case_name('CommDefault', 'Overnight', '0F03'), 2, 120, ['1920x1080']*2, [1500, 3000], [30]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            [generate_case_name('CommDefault', 'Overnight', '0F04'), 1, 120, ['1920x1080']  , [1000]      , [15]  , [0]  , ['AzureLow']                ],
            # [generate_case_name('CommDefault', 'Overnight', '0F05'), 1, 120, ['1920x1080']  , [3000]      , [30]  , [0]  , ['AzureMedium']             ],

            # [generate_case_name('CommDefault', 'Overnight', '1000'), 2, 120, ['2560x1440']*2, [1600, 3200], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            # [generate_case_name('CommDefault', 'Overnight', '1001'), 2, 120, ['2560x1440']*2, [1600, 3200], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            # [generate_case_name('CommDefault', 'Overnight', '1002'), 2, 120, ['2560x1440']*2, [2400, 4800], [30]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            # [generate_case_name('CommDefault', 'Overnight', '1003'), 2, 120, ['2560x1440']*2, [2400, 4800], [30]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            # [generate_case_name('CommDefault', 'Overnight', '1004'), 1, 120, ['2560x1440']  , [1600]      , [15]  , [0]  , ['AzureLow']                ],
            # [generate_case_name('CommDefault', 'Overnight', '1005'), 1, 120, ['2560x1440']  , [4800]      , [30]  , [0]  , ['AzureMedium']             ],

            # [generate_case_name('CommDefault', 'Overnight', '1100'), 2, 120, ['3840x2160']*2, [3000, 6000], [15]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            # [generate_case_name('CommDefault', 'Overnight', '1101'), 2, 120, ['3840x2160']*2, [3000, 6000], [15]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            # [generate_case_name('CommDefault', 'Overnight', '1102'), 2, 120, ['3840x2160']*2, [4500, 9000], [30]*2, [0]*2, ['AzureLow', 'AzureMedium']],
            # [generate_case_name('CommDefault', 'Overnight', '1103'), 2, 120, ['3840x2160']*2, [4500, 9000], [30]*2, [4]*2, ['AzureLow', 'AzureMedium']],
            # [generate_case_name('CommDefault', 'Overnight', '1104'), 1, 120, ['3840x2160'],   [3000],       [15]  , [0]  , ['AzureLow']                ],
            # [generate_case_name('CommDefault', 'Overnight', '1105'), 1, 120, ['3840x2160'],   [9000],       [30]  , [0]  , ['AzureMedium']             ],

            [generate_case_name('CommDefault', 'Overnight', '1200'), 2, 120, [  '640x360']*2, [ 400]*2, [15]*2, [0, 4]           , ['AzureMedium']*2],
            [generate_case_name('CommDefault', 'Overnight', '1201'), 4, 120, [  '640x360']*4, [ 400]*4, [15]*4, [0]*2+[4]*2      , ['AzureMedium']*4],
            [generate_case_name('CommDefault', 'Overnight', '1202'), 6, 120, [  '640x360']*6, [ 400]*6, [15]*6, [0]*2+[3]*2+[6]*2, ['AzureMedium']*6],

            [generate_case_name('LiveDefault', 'Overnight', '0000'), 4, 120, [  '120x120']*4, [   37,    50,    62,    75],  [5]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Overnight', '0001'), 4, 120, [  '120x120']*4, [   75,   100,   125,   150], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveDefault', 'Overnight', '0100'), 4, 120, [  '160x120']*4, [   45,    60,    75,    90],  [5]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Overnight', '0101'), 4, 120, [  '160x120']*4, [   90,   120,   150,   180], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveDefault', 'Overnight', '0200'), 4, 120, [  '180x180']*4, [   75,   100,   125,   150],  [5]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Overnight', '0201'), 4, 120, [  '180x180']*4, [  150,   200,   250,   300], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveDefault', 'Overnight', '0300'), 4, 120, [  '240x180']*4, [   90,   120,   150,   180],  [5]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Overnight', '0301'), 4, 120, [  '240x180']*4, [  180,   240,   300,   360], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveDefault', 'Overnight', '0400'), 4, 120, [  '320x180']*4, [  105,   140,   175,   210],  [5]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Overnight', '0401'), 4, 120, [  '320x180']*4, [  210,   280,   350,   420], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveDefault', 'Overnight', '0500'), 4, 120, [  '240x240']*4, [  105,   140,   175,   210],  [5]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Overnight', '0501'), 4, 120, [  '240x240']*4, [  210,   280,   350,   420], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveDefault', 'Overnight', '0600'), 4, 120, [  '320x240']*4, [  135,   180,   225,   270],  [5]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Overnight', '0601'), 4, 120, [  '320x240']*4, [  270,   360,   450,   540], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveDefault', 'Overnight', '0700'), 4, 120, [  '424x240']*4, [  165,   220,   275,   330],  [5]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Overnight', '0701'), 4, 120, [  '424x240']*4, [  330,   440,   550,   660], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveDefault', 'Overnight', '0800'), 4, 120, [  '360x360']*4, [  195,   260,   325,   390],  [5]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Overnight', '0801'), 4, 120, [  '360x360']*4, [  390,   520,   650,   780], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveDefault', 'Overnight', '0900'), 4, 120, [  '640x360']*4, [  600,   800,  1000,  1200], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Overnight', '0901'), 4, 120, [  '640x360']*4, [  900,  1200,  1500,  1800], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveDefault', 'Overnight', '0A00'), 4, 120, [  '480x480']*4, [  600,   800,  1000,  1200], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Overnight', '0A01'), 4, 120, [  '480x480']*4, [  900,  1200,  1500,  1800], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveDefault', 'Overnight', '0B00'), 4, 120, [  '640x480']*4, [  750,  1000,  1250,  1500], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Overnight', '0B01'), 4, 120, [  '640x480']*4, [ 1125,  1500,  1875,  2250], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveDefault', 'Overnight', '0C00'), 4, 120, [  '848x480']*4, [  900,  1200,  1500,  1800], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveDefault', 'Overnight', '0C01'), 4, 120, [  '848x480']*4, [ 1350,  1800,  2250,  2700], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveDefault', 'Overnight', '0D00'), 4, 120, [  '960x720']*4, [ 1440,  1920,  2400,  2880], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            # [generate_case_name('LiveDefault', 'Overnight', '0D01'), 4, 120, [  '960x720']*4, [ 2160,  2880,  3600,  4320], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            # [generate_case_name('LiveDefault', 'Overnight', '0E00'), 4, 120, [ '1280x720']*4, [ 1800,  2400,  3000,  3600], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            # [generate_case_name('LiveDefault', 'Overnight', '0E01'), 4, 120, [ '1280x720']*4, [ 2700,  3600,  4500,  5400], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            # [generate_case_name('LiveDefault', 'Overnight', '0F00'), 4, 120, ['1920x1080']*4, [ 3000,  4000,  5000,  6000], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            # [generate_case_name('LiveDefault', 'Overnight', '0F01'), 4, 120, ['1920x1080']*4, [ 4500,  6000,  7500,  9000], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            # [generate_case_name('LiveDefault', 'Overnight', '1000'), 4, 120, ['2560x1440']*4, [ 4800,  6400,  8000,  9600], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            # [generate_case_name('LiveDefault', 'Overnight', '1001'), 4, 120, ['2560x1440']*4, [ 7200,  9600, 12000, 14400], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            # [generate_case_name('LiveDefault', 'Overnight', '1100'), 4, 120, ['3840x2160']*4, [ 9000, 12000, 15000, 18000], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            # [generate_case_name('LiveDefault', 'Overnight', '1101'), 4, 120, ['3840x2160']*4, [13500, 18000, 22500, 27000], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('CommScreenShare', 'Overnight', '0000'), 2, 120, ['2880x1800']*2, [ 1000]*2, [ 5]*2, [0]*2, ['WikiText']*2],
            [generate_case_name('CommScreenShare', 'Overnight', '0001'), 2, 120, ['2880x1800']*2, [ 1000]*2, [ 5]*2, [4]*2, ['WikiText']*2],
            # [generate_case_name('CommScreenShare', 'Overnight', '0002'), 2, 120, ['2880x1800']*2, [ 1000]*2, [10]*2, [0]*2, ['WikiText']*2],
            # [generate_case_name('CommScreenShare', 'Overnight', '0003'), 2, 120, ['2880x1800']*2, [ 1000]*2, [10]*2, [4]*2, ['WikiText']*2],

            [generate_case_name('LiveScreenShare', 'Overnight', '0000'), 2, 120, ['2880x1800']*2, [ 1000]*2, [ 5]*2, [0]*2, ['WikiText']*2],
            [generate_case_name('LiveScreenShare', 'Overnight', '0001'), 2, 120, ['2880x1800']*2, [ 1000]*2, [ 5]*2, [4]*2, ['WikiText']*2],
            # [generate_case_name('LiveScreenShare', 'Overnight', '0002'), 2, 120, ['2880x1800']*2, [ 1000]*2, [10]*2, [0]*2, ['WikiText']*2],
            # [generate_case_name('LiveScreenShare', 'Overnight', '0003'), 2, 120, ['2880x1800']*2, [ 1000]*2, [10]*2, [4]*2, ['WikiText']*2],

            [generate_case_name('LiveWebInterOp', 'Overnight', '0000'), 4, 120, [  '640x360']*4, [  600,   800,  1000,  1200], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveWebInterOp', 'Overnight', '0001'), 4, 120, [  '640x360']*4, [  900,  1200,  1500,  1800], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveWebInterOp', 'Overnight', '0100'), 4, 120, [  '480x480']*4, [  600,   800,  1000,  1200], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveWebInterOp', 'Overnight', '0101'), 4, 120, [  '480x480']*4, [  900,  1200,  1500,  1800], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveWebInterOp', 'Overnight', '0200'), 4, 120, [  '640x480']*4, [  750,  1000,  1250,  1500], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveWebInterOp', 'Overnight', '0201'), 4, 120, [  '640x480']*4, [ 1125,  1500,  1875,  2250], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveWebInterOp', 'Overnight', '0300'), 4, 120, [  '848x480']*4, [  900,  1200,  1500,  1800], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
            [generate_case_name('LiveWebInterOp', 'Overnight', '0301'), 4, 120, [  '848x480']*4, [ 1350,  1800,  2250,  2700], [30]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],

            [generate_case_name('LiveWebInterOp', 'Overnight', '0400'), 4, 120, [  '960x720']*4, [ 1440,  1920,  2400,  2880], [15]*4, [0]*4, ['AzureMedium']*2+['AzureHigh']*2],
        ]
else:
    cases = [
        [generate_case_name('CommDefault', 'Regression', '0000'), 2, 6, ['180x180']*2, [ 25,  50],  [5]*2, [0]*2, ['Default']*2],
        [generate_case_name('CommDefault', 'Regression', '0001'), 2, 6, ['320x180']*2, [ 70, 140], [15]*2, [0]*2, ['Default']*2],
        [generate_case_name('CommDefault', 'Regression', '0002'), 2, 6, ['320x240']*2, [ 45,  90],  [5]*2, [2]*2, ['Default']*2],
        [generate_case_name('CommDefault', 'Regression', '0003'), 2, 6, ['180x180']*2, [ 50, 100], [15]*2, [2]*2, ['Default']*2],
        [generate_case_name('CommDefault', 'Regression', '0004'), 2, 6, ['320x180']*2, [ 35,  70],  [5]*2, [4]*2, ['Default']*2],
        [generate_case_name('CommDefault', 'Regression', '0005'), 2, 6, ['320x240']*2, [ 90, 180], [15]*2, [4]*2, ['Default']*2],

        [generate_case_name('CommDefault', 'Regression', '0100'), 2, 6, ['360x360']*2, [130, 260], [15]*2, [0]*2, ['Default']*2],
        [generate_case_name('CommDefault', 'Regression', '0101'), 2, 6, ['640x360']*2, [300, 600], [30]*2, [0]*2, ['Default']*2],
        [generate_case_name('CommDefault', 'Regression', '0102'), 2, 6, ['640x480']*2, [250, 500], [15]*2, [2]*2, ['Default']*2],
        [generate_case_name('CommDefault', 'Regression', '0103'), 2, 6, ['360x360']*2, [195, 390], [30]*2, [2]*2, ['Default']*2],
        [generate_case_name('CommDefault', 'Regression', '0104'), 2, 6, ['640x360']*2, [200, 400], [15]*2, [4]*2, ['Default']*2],
        [generate_case_name('CommDefault', 'Regression', '0105'), 2, 6, ['640x480']*2, [375, 750], [30]*2, [4]*2, ['Default']*2],

        [generate_case_name('LiveDefault', 'Regression', '0000'), 4, 6, ['180x180']*4, [ 105,  140,  175,  210], [ 5]*4, [0]*4, ['Default']*4],
        [generate_case_name('LiveDefault', 'Regression', '0001'), 4, 6, ['320x180']*4, [ 210,  280,  350,  420], [15]*4, [0]*4, ['Default']*4],
        [generate_case_name('LiveDefault', 'Regression', '0002'), 4, 6, ['320x240']*4, [ 210,  280,  350,  420], [30]*4, [0]*4, ['Default']*4],

        [generate_case_name('LiveDefault', 'Regression', '0100'), 4, 6, ['360x360']*4, [ 195,  260,  325,  390], [ 5]*4, [0]*4, ['Default']*4],
        [generate_case_name('LiveDefault', 'Regression', '0101'), 4, 6, ['640x360']*4, [ 600,  800, 1000, 1200], [15]*4, [0]*4, ['Default']*4],
        [generate_case_name('LiveDefault', 'Regression', '0102'), 4, 6, ['640x480']*4, [1125, 1500, 1875, 2250], [30]*4, [0]*4, ['Default']*4],

        [generate_case_name('CommScreenShare', 'Regression', '0000'), 2, 6, ['640x360'] * 2, [300, 600], [30] * 2, [0] * 2, ['Default'] * 2],

        [generate_case_name('LiveScreenShare', 'Regression', '0000'), 2, 6, ['640x360'] * 2, [300, 600], [30] * 2, [0] * 2, ['Default'] * 2],

        [generate_case_name('LiveWebInterOp', 'Regression', '0100'), 4, 6, ['360x360']*4, [ 195,  260,  325,  390], [ 5]*4, [0]*4, ['Default']*4],
        [generate_case_name('LiveWebInterOp', 'Regression', '0101'), 4, 6, ['640x360']*4, [ 600,  800, 1000, 1200], [15]*4, [0]*4, ['Default']*4],
        [generate_case_name('LiveWebInterOp', 'Regression', '0102'), 4, 6, ['640x480']*4, [1125, 1500, 1875, 2250], [30]*4, [0]*4, ['Default']*4],

        [generate_case_name('CommDefault', 'Overnight', '0000'), 2, 15, ['640x360']*2, [300, 600], [15]*2, [0]*2, ['Default']*2],
        [generate_case_name('CommDefault', 'Overnight', '0001'), 2, 15, ['640x360']*2, [300, 600], [30]*2, [0]*2, ['Default']*2],

        [generate_case_name('LiveDefault', 'Overnight', '0000'), 4, 15, ['640x360']*4, [ 600,  800, 1000, 1200], [15]*4, [0]*4, ['Default']*4],
        [generate_case_name('LiveDefault', 'Overnight', '0001'), 4, 15, ['640x360']*4, [ 600,  800, 1000, 1200], [15]*4, [4]*4, ['Default']*4],

        [generate_case_name('CommScreenShare', 'Overnight', '0000'), 2, 15, ['640x360']*2, [300, 600], [30]*2, [0]*2, ['Default']*2],
        [generate_case_name('CommScreenShare', 'Overnight', '0001'), 2, 15, ['640x360']*2, [300, 600], [30]*2, [4]*2, ['Default']*2],

        [generate_case_name('LiveScreenShare', 'Overnight', '0000'), 2, 15, ['640x360']*2, [300, 600], [15]*2, [0]*2, ['Default']*2],
        [generate_case_name('LiveScreenShare', 'Overnight', '0001'), 2, 15, ['640x360']*2, [300, 600], [30]*2, [0]*2, ['Default']*2],

        [generate_case_name('LiveWebInterOp', 'Overnight', '0000'), 4, 15, ['640x360']*4, [ 600,  800, 1000, 1200], [15]*4, [0]*4, ['Default']*4],
        [generate_case_name('LiveWebInterOp', 'Overnight', '0001'), 4, 15, ['640x360']*4, [ 600,  800, 1000, 1200], [15]*4, [4]*4, ['Default']*4],
    ]
