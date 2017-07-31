import re
import numpy

import global_parameters as gp
from pdb import set_trace as bp


class DecResult:
    def __init__(self, uid):
        self.uid_ = uid
        self.map_ = dict.fromkeys(gp.data_type, 0)
        self.data_ = dict.fromkeys(gp.data_type, -1)
        self.time_ = 0

    def add_one_dec_result(self, data):
        tmp = data.split('\n')[0].split('\t')
        if tmp[1] != '':
            assert self.map_[tmp[0]] == 0
            self.map_[tmp[0]] = 1
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
        self.data_ = dict.fromkeys(gp.data_type, 0)
        self.time_ = 0

    def add_one_enc_result(self, data):
        tmp = data.split('\n')[0].split('\t')
        assert self.map_[tmp[0]] == 0
        self.map_[tmp[0]] = 1
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
        return self.configure_

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
