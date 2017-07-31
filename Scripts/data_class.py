import numpy

import global_parameters as gp
from pdb import set_trace as bp


class ResultRecorder:
    def __init__(self, title):
        tmp = title.split('\n')[0].split('\t')
        self.map_ = dict.fromkeys(gp.data_type, -1)
        for enc_data in gp.data_type:
            if enc_data in tmp:
                self.map_[enc_data] = tmp.index(enc_data)
        self.result_for_one_second_ = dict.fromkeys(gp.data_type, 0)
        self.result_for_one_second_['bitrate_diff'] = []
        self.result_per_second_ = dict.fromkeys(gp.data_type)
        for data_type in gp.data_type:
            self.result_per_second_[data_type] = []
        self.frames_ = 0
        self.start_time = 0
        self.time = 0

    def add_one_fame_result(self, result):
        if result == '':
            return 1
        tmp = result.split('\n')[0].split('\t')
        if self.frames_ == 0:
            self.start_time = int(tmp[self.map_['timestamp']])
            self.result_per_second_['timestamp'].append(self.start_time)
            self.time = 1

        target_bitrate = self.result_for_one_second_['target_bitrate']
        real_bitrate = self.result_for_one_second_['real_bitrate']
        if target_bitrate == 0:
            target_bitrate = real_bitrate
        if int(tmp[self.map_['timestamp']]) - self.start_time > self.time * 1000:
            for data_type in gp.data_type:
                if data_type == 'bitrate_diff':
                    self.result_per_second_[data_type].append(abs(target_bitrate - real_bitrate) * 100 / target_bitrate)
                    self.result_for_one_second_[data_type] = []
                elif self.is_per_frame_data_type(data_type):
                    self.result_per_second_[data_type].append(int(tmp[self.map_[data_type]]))
                    self.result_for_one_second_[data_type] = 0
                elif self.is_accumulate_data_type(data_type):
                    if data_type == 'is_decodable':
                        self.result_per_second_[data_type].append(self.result_for_one_second_[data_type])
                    else:
                        self.result_per_second_[data_type].append(self.result_for_one_second_[data_type]*1.0/1000)
                    self.result_for_one_second_[data_type] = 0
                elif self.is_average_data_type(data_type):
                    self.result_per_second_[data_type].append(self.result_for_one_second_[data_type]/self.frames_)
                    self.result_for_one_second_[data_type] = 0

            self.result_per_second_['real_fps'].append(self.frames_)
            self.frames_ = 0
            self.time += 1

        self.frames_ += 1
        target = 0
        for data_type in gp.data_type:
            if self.map_[data_type] != -1:
                if self.is_stream_data_type(data_type):
                    self.result_for_one_second_[data_type] = tmp[self.map_[data_type]]
                elif self.is_per_frame_data_type(data_type):
                    self.result_for_one_second_[data_type] = int(tmp[self.map_[data_type]])
                else:
                    if data_type == 'target_bitrate':
                        target = float(tmp[self.map_[data_type]])
                    elif data_type == 'real_bitrate':
                        real = float(tmp[self.map_[data_type]])
                        
                    if data_type == 'is_decodable':
                        self.result_for_one_second_[data_type] += abs(int(tmp[self.map_[data_type]]))
                    else:
                        self.result_for_one_second_[data_type] += float(tmp[self.map_[data_type]])

        if target == 0:
            target = real
        # self.result_for_one_second_['bitrate_diff'].append((target - real) * 100.0 / target)
        return 0

    def is_recorded_data_type(self, data_type, ref_type):
        if data_type not in gp.data_type:
            gp.print_log(gp.LogLevel.Normal, 'data_type ' + data_type + ' is not in data_type_!')
        return data_type in gp.data_type and self.map_[data_type] != -1 and data_type == ref_type

    def is_accumulate_data_type(self, data_type):
        return self.is_recorded_data_type(data_type, 'target_bitrate') \
               or self.is_recorded_data_type(data_type, 'real_bitrate') \
               or self.is_recorded_data_type(data_type, 'is_decodable')

    def is_average_data_type(self, data_type):
        return self.is_recorded_data_type(data_type, 'PSNR') \
               or self.is_recorded_data_type(data_type, 'SSIM') \
               or self.is_recorded_data_type(data_type, 'encoding_time') \
               or self.is_recorded_data_type(data_type, 'target_fps')

    def is_stream_data_type(self, data_type):
        return self.is_recorded_data_type(data_type, 'MD5') \
               or self.is_recorded_data_type(data_type, 'orig_MD5')

    def is_per_frame_data_type(self, data_type):
        return self.is_recorded_data_type(data_type, 'frame_idx') \
               or self.is_recorded_data_type(data_type, 'timestamp') \
               or self.is_recorded_data_type(data_type, 'uid')

    def get_current_md5(self):
        return self.result_for_one_second_['MD5']

    def get_current_uid(self):
        return self.result_for_one_second_['uid']

    def get_data_per_second(self, data_type):
        return self.result_per_second_[data_type]

    def get_data_per_second_str(self, data_type):
        if data_type == 'SSIM':
            return data_type + '\t' + '\t'.join('%.4f' % data for data in self.result_per_second_[data_type]) + '\n'
        elif data_type == 'is_decodable':
            return data_type + '\t' + '\t'.join('%d' % data for data in self.result_per_second_[data_type]) + '\n'
        else:
            return data_type + '\t' + '\t'.join('%.2f' % data for data in self.result_per_second_[data_type]) + '\n'

    def get_data_total_str(self):
        result = ''
        for data_type in gp.data_type:
            if self.is_accumulate_data_type(data_type) \
                    or self.is_average_data_type(data_type) \
                    or data_type == 'real_fps':
                result += self.get_data_per_second_str(data_type)
            # here is to prevent decoder print this line
            if data_type == 'bitrate_diff' and numpy.sum(self.result_per_second_[data_type]) > 0:
                result += self.get_data_per_second_str(data_type)
        return result
