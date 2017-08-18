import re
import numpy

import global_parameters as gp
from pdb import set_trace as bp


class DecResult:
    def __init__(self, uid):
        self.uid_ = uid
        self.map_ = dict.fromkeys(gp.data_type, 0)
        #store raw_data for generating pictures
        self.raw_data_ = dict.fromkeys(gp.data_type, [])
        self.data_ = dict.fromkeys(gp.data_type, -1)
        self.time_ = 0

    def add_one_dec_result(self, data):
        tmp = data.split('\n')[0].split('\t')
        if tmp[1] != '':
            assert self.map_[tmp[0]] == 0
            self.map_[tmp[0]] = 1
            #store raw_data
            self.raw_data_[tmp[0]] = map(float, tmp[1:])
            self.data_[tmp[0]] = numpy.mean(map(float, tmp[1:]))
            if self.time_ == 0:
                self.time_ = len(tmp) - 1
            elif len(tmp) != 2:
                assert self.time_ == len(tmp) - 1


class Client:
    def __init__(self, client_title):
        tmp = client_title.split('\n')[0].split(gp.string_join)
        self.uid_ = int(tmp[1])
        self.case_ = tmp[0]
        self.configure_ = tmp[2]
        self.rate_ = int(tmp[2].split(gp.folder_join)[0][4:])
        self.decoded_client_ = []
        self.map_ = dict.fromkeys(gp.data_type, 0)
        self.raw_data_ = dict.fromkeys(gp.data_type, [])
        self.data_ = dict.fromkeys(gp.data_type, 0)
        self.time_ = 0
        self.len_ = 0

    #add some functions:
    #get length of target_bitrate_ and real_bitrate_
    def get_len_(self):
        assert len(self.raw_data_['target_bitrate']) == len(self.raw_data_['real_bitrate'])
        return len(self.raw_data_['target_bitrate'])
    #judge whether the target_bitrate falls in the correct range.
    def is_rate_reasonable(self, lower_range = 0.8, upper_range = 1.2, absolute = 0):
        mean_target_bitrate = numpy.mean(self.raw_data_['target_bitrate'])
        if absolute == 0:
            return mean_target_bitrate >= lower_range * self.rate_ and mean_target_bitrate <= upper_range * self.rate_
        else:
            return mean_target_bitrate >= lower_range and mean_target_bitrate <= upper_range

    #return ratio of target_rate to purposed rate
    def find_rate_ratio(self):
        mean_target_bitrate = numpy.mean(self.raw_data_['target_bitrate'])
        return mean_target_bitrate / float(self.rate_)

    #judge whether target_bitrate always matches well with real_bitrate. In this version, I don't consider how to judge whether the data is fluctuating significantly.
    def compare_target_and_real_plain(self, lower_range = 0.92, upper_range = 1.08):
        assert len(self.raw_data_['target_bitrate']) == len(self.raw_data_['real_bitrate'])
        total_sec = len(self.raw_data_['target_bitrate'])
        err_sec = 0
        for i in range(len(self.raw_data_['target_bitrate'])):
            if self.raw_data_['real_bitrate'][i] < lower_range * self.raw_data_['target_bitrate'][i] or self.raw_data_['real_bitrate'][i] > upper_range * self.raw_data_['target_bitrate'][i]:
                err_sec += 1
        return float(err_sec)/total_sec*100

    #judge whether target_bitrate is stable during the recent 2-second period
    def is_stable(self, cur_second, lower_range = 0.9, upper_range = 1.1):
        self.len_ = self.get_len_()
        #print self.len_
        assert cur_second >= 0 and cur_second <= self.len_-1
        cur_bitrate = self.raw_data_['target_bitrate'][cur_second]
        if cur_second == 0:
            return self.len_ == 0 or (self.raw_data_['target_bitrate'][1] >= lower_range * cur_bitrate and self.raw_data_['target_bitrate'][1] <= upper_range * cur_bitrate)
        elif cur_second == self.len_-1:
            return self.time_ == 0 or (self.raw_data_['target_bitrate'][-2] >= lower_range * cur_bitrate and self.raw_data_['target_bitrate'][-2] <= upper_range * cur_bitrate)
        else:
            return (self.raw_data_['target_bitrate'][cur_second-1] >= lower_range * cur_bitrate and self.raw_data_['target_bitrate'][cur_second-1] <= upper_range * cur_bitrate) and (self.raw_data_['target_bitrate'][cur_second+1] >= lower_range * cur_bitrate and self.raw_data_['target_bitrate'][cur_second+1] <= upper_range * cur_bitrate)
    
    #judge whether target_bitrate always matches well with real_bitrate. In this version, the fluctuation of target_bitrate is considered by monitoring the variance of value in 2 adjacent seconds.
    def compare_target_and_real(self, stable_lower_range = 0.92, stable_upper_range = 1.08, fluc_lower_range = 0.9, fluc_upper_range = 1.1):
        assert len(self.raw_data_['target_bitrate']) == len(self.raw_data_['real_bitrate'])
        total_sec = len(self.raw_data_['target_bitrate'])
        err_sec = 0
        for i in range(len(self.raw_data_['target_bitrate'])):
            if self.is_stable(i):
                if self.raw_data_['real_bitrate'][i] < stable_lower_range * self.raw_data_['target_bitrate'][i] or self.raw_data_['real_bitrate'][i] > stable_upper_range * self.raw_data_['target_bitrate'][i]:
                    err_sec += 1
            else:
                if self.raw_data_['real_bitrate'][i] < fluc_lower_range * self.raw_data_['target_bitrate'][i] or self.raw_data_['real_bitrate'][i] > fluc_upper_range * self.raw_data_['target_bitrate'][i]:
                    err_sec += 1
        return float(err_sec)/total_sec*100

    def add_one_enc_result(self, data):
        tmp = data.split('\n')[0].split('\t')
        assert self.map_[tmp[0]] == 0
        self.map_[tmp[0]] = 1
        self.raw_data_[tmp[0]] = map(float, tmp[1:])
        self.data_[tmp[0]] = numpy.mean(map(float, tmp[1:]))
        if self.time_ == 0:
            self.time_ = len(tmp) - 1
        elif len(tmp) != 2:
            assert self.time_ == len(tmp) - 1

    def get_enc_result(self, data_type):
        return self.data_[data_type]

    def get_dec_result(self, data_type):
        data = []
        for decoded_client in self.decoded_client_:
            if decoded_client.data_[data_type] != -1:
                data.append(decoded_client.data_[data_type])

        return numpy.mean(data)

    def get_uid(self):
        return self.uid_

    def get_case(self):
        return self.case_

    def get_config(self):
        return 'uid' + str(self.uid_) + '_' + self.configure_

    def add_one_decode_client(self, decoded_uid):
        self.decoded_client_.append(DecResult(decoded_uid))

    def add_one_dec_result(self, data):
        self.decoded_client_[-1].add_one_dec_result(data)

    def __lt__(self, other):
        return self.rate_ < other.rate_


class Case:
    def __init__(self, data):
        self.case_ = self.extract_case(data)
        self.client_ = [Client(data)]

    def add_client(self, data):
        self.client_.append(Client(data))

    def sort_client(self):
        self.client_.sort()

    def is_same_case(self, case):
        return self.case_ == case

    @staticmethod
    def extract_case(data):
        return data.split('\n')[0].split(gp.string_join)[0]

    @staticmethod
    def extract_configure(data):
        return data.split('\n')[0].split(gp.string_join)[2]

    def get_case(self):
        return self.case_

    def get_config(self, index):
        return self.client_[index].get_config()

    def get_client_number(self):
        return len(self.client_)

    def get_enc_data(self, data_type, multiplier = 1.0):
        data = []
        for client in self.client_:
            data.append(client.get_enc_result(data_type) * multiplier)
        return data

    def get_avg_enc_data(self, data_type):
        data = self.get_enc_data(data_type)
        return numpy.mean(data)

    def get_dec_data(self, data_type, multiplier = 1.0):
        data = []
        for client in self.client_:
            data.append(client.get_dec_result(data_type) * multiplier)
        return data

    def get_avg_dec_data(self, data_type):
        data = self.get_dec_data(data_type)
        return numpy.mean(data)

    def __lt__(self, other):
        cur = int(self.case_.split(gp.folder_join)[-1], 16)
        tst = int(other.case_.split(gp.folder_join)[-1], 16)

        return cur < tst


class CaseSummary:
    def __init__(self, enc_file_name, dec_file_name):
        self.case_set_ = []

        enc_file = open(enc_file_name, 'r')
        line = enc_file.readline()
        while line != '':
            if re.search('Net', line):
                case_name = line.split('\n')[0].split(gp.string_join)[0]
                case = self.find_case(case_name)
                if case != 0:
                    case.add_client(line)
                else:
                    self.case_set_.append(Case(line))
                    case = self.case_set_[-1]
            else:
                case.client_[-1].add_one_enc_result(line)
            line = enc_file.readline()
        
        enc_file.close()
        # reconstruction: updating the target_purposed_ratio and unqualified_ratio of each client
        for case_idx_ in range(len(self.case_set_)):
            for client_idx_ in range(len(self.case_set_[case_idx_].client_)):
                self.case_set_[case_idx_].client_[client_idx_].data_['target_purposed_ratio'] = \
                self.case_set_[case_idx_].client_[client_idx_].find_rate_ratio()
                self.case_set_[case_idx_].client_[client_idx_].data_['unqualified_ratio'] = \
                self.case_set_[case_idx_].client_[client_idx_].compare_target_and_real()

        
        for case in self.case_set_:
            case.sort_client()

        self.case_set_.sort()

        dec_file = open(dec_file_name, 'r')
        line = dec_file.readline()
        while line != '':
            if re.search('Net', line):
                decoded_uid = int(line.split('\n')[0].split(gp.string_join)[1])
                case_name = line.split('\n')[0].split(gp.string_join)[0]
            elif re.search('For' + gp.string_join + 'UID', line):
                uid = int(line.split('\n')[0].split(gp.string_join)[-1])
                client = self.find_client_by_case_and_uid(case_name, uid)
                if client == 0:
                    gp.print_log(gp.LogLevel.Normal, 'Can not find client by UID ' + str(uid))
                    exit()
                client.add_one_decode_client(decoded_uid)
            else:
                client.add_one_dec_result(line)
            line = dec_file.readline()
        dec_file.close()

    def find_case(self, case):
        for idx in range(0, len(self.case_set_)):
            if self.case_set_[idx].is_same_case(case):
                return self.case_set_[idx]
        return 0

    def find_client_by_case_and_uid(self, case_name, uid):
        for case in self.case_set_:
            if case_name == case.get_case():
                for client in case.client_:
                    if client.get_uid() == uid:
                        return client
        return 0

    def find_client_by_case(self, case):
        for case_idx in range(0, len(self.case_set_)):
            for client_idx in range(0, len(self.case_set_[case_idx].client_)):
                if self.case_set_[case_idx].client_[client_idx].get_case() == case:
                    return self.case_set_[case_idx].client_[client_idx]
        return 0

    def get_total_case_num(self):
        return len(self.case_set_)
