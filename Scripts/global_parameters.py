#!/usr/bin/python

import os
import platform
import time
import shutil
import re
import multiprocessing
from pdb import set_trace as bp


script_version = '1.0'
encoder_version = '20120202'

data_type = ['timestamp', 'frame_idx', 'target_bitrate', 'real_bitrate', 'target_fps', 'real_fps', 'PSNR', 'SSIM',
             'MD5', 'encoding_time', 'bitrate_diff', 'uid', 'is_decodable', 'orig_MD5', 'vqmg']


class RunningState:
    Success = 0
    Crash = 1
    Unfinished = 2
    Running = 3

    def __init__(self):
        pass


class LogLevel:
    Normal = 0b001
    Debug = 0b010
    Info = 0b100

    def __init__(self):
        pass

print_log_filter = LogLevel.Normal
log_file = ''


def print_log(level, info):
    if level & print_log_filter:
        process_lock.acquire()
        print(info)
        if type(log_file) == file and not log_file.closed:
            log_file.write(info + '\n')
        process_lock.release()


def generate_dir_path(*arg):
    output = ''
    for variable in arg:
        output += variable
        if output[-1] != '/':
            output += '/'
    return output


def zip_to_folder(zip_name, zip_folder, target_folder):
    cur_dir = os.getcwd()
    if zip_folder[-1] != '/':
        zip_folder += '/'
    os.chdir(zip_folder + '../')
    folder_name = zip_folder.split('/')[-2]
    os.system('zip -rq ' + zip_name + ' ' + folder_name)
    os.system('mv ' + zip_name + ' ' + target_folder)
    os.chdir(cur_dir)


def remove_dir(directory):
    if os.path.exists(directory):
        print_log(LogLevel.Info, 'Removing ' + directory)
        shutil.rmtree(directory)


def create_dir(directory):
    remove_dir(directory)
    print_log(LogLevel.Info, 'Creating ' + directory)
    os.makedirs(directory)


def read_commit_log(directory):
    output = ''
    doc_list = os.listdir(directory)
    for doc in doc_list:
        if re.search('commit.log', doc):
            fp = open(directory + doc, 'r')
            line = fp.readline()
            while line != '\n':
                output += '<p>\n' + line + '</p>\n'
                line = fp.readline()
            output += '<p>\n' + fp.readline() + '</p>\n'
            fp.close()
    return output


def convert_date(date):
    return date[0:4] + '-' + date[4:6] + '-' + date[6:8] + ' ' + date[8:10] + ':' + date[10:12] + ':' + date[12:14]


cur_abs_dir = os.getcwd() + '/../'
cur_platform = platform.system()

cur_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

if re.search('data', cur_abs_dir) or cur_platform != 'Linux':
    on_server = 0
else:
    on_server = 1

scenario = [
    'CommDefault',
    'LiveDefault',
    'CommScreenShare',
    'LiveScreenShare',
    'LiveWebInterOp',
]

connection = [
    'WithServer',
    'NoServer',
]
connection_type = 'WithServer'

networks = [
    'network0.txt',
    'network1.txt',
    'network2.txt',
    'network3.txt',
    'network4.txt',
    'network5.txt',
    'network6.txt',
    'network7.txt',
]

if cur_platform == 'Linux':
    data_dir = '/data/'
    sequence_dir = '/data/RawSeq/'
    executable_dir = cur_abs_dir + 'Executable/Linux/'
else:
    data_dir = cur_abs_dir
    sequence_dir = cur_abs_dir + '../../UnitTest_multi_process/Sequences/'
    executable_dir = cur_abs_dir + 'Executable/Darwin/'

result_dir = generate_dir_path(data_dir, 'Results')
network_dir = generate_dir_path(cur_abs_dir, 'Network')
problem_dir = generate_dir_path(data_dir, 'ProblematicCase')
temp_dir = generate_dir_path(data_dir, 'TempResult')
cur_log_dir = ''
ref_log_dir = ''
backup_log_dir = ''
save_to_backup_dir = True
mode = ''
cur_commit_id = ''
ref_commit_id = ''


class Executable:
    def __init__(self, name, directory):
        self.name_ = name
        self.dir_ = directory

    def set_executable_dir(self, directory):
        self.dir_ = directory

    def get_full_path_executable(self):
        return self.dir_ + self.name_

    def get_executable_name(self):
        return self.name_

    def copy_executable_to_dir(self, directory):
        os.system('cp ' + self.get_full_path_executable() + ' ' + directory)


scale = Executable('YUVScale', executable_dir)
client = Executable('ClientAgora', '')
server = Executable('ServerAgora', executable_dir)
vqm_test = Executable('VQMTest2', executable_dir)
decode_stream = Executable('DecodeStream', executable_dir)

process_lock = multiprocessing.Lock()
mgr = multiprocessing.Manager()
running_process = mgr.Value('i', 0)
scenario_crash = mgr.Value('i', 0)
used_capacity = mgr.Value('i', 0)
client_flag = mgr.list([0])

total_crash = 0
total_mismatch = 0

multiprocessing.Pool()
if cur_platform == 'Linux' and on_server == 1:
    active_process = max(len(multiprocessing.active_children()) / 2, 4)
else:
    active_process = max(len(multiprocessing.active_children()) - 1, 2)

capacity = 1920 * 1080 * 30 * 2

seq_candidates = dict()

if cur_platform == 'Linux':
    if on_server == 0:
        sequences = {'AzureLow': '405_AzureLowMotion_20160523_1920x1080p30_614',
                     'WikiText': '501_WikipediaText_20170427_2880x1800p15_301'}
    else:
        sequences = {'AzureLow': '405_AzureLowMotion_20160523_1920x1080p30_614',
                     'AzureMedium': '406_AzureMediumMotion_20160523_1920x1080p30_703',
                     'AzureHigh': '407_AzureHighMotion_20160523_1920x1080p30_658',
                     'WikiText': '501_WikipediaText_20170427_2880x1800p15_301'}
else:
    sequences = {'Default': '401_MediumLightZehuaYurunTalk_20151224_160x90p30_100f'}

clients = []

folder_join = '_'
string_join = '-'
