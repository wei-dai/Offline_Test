#!/usr/bin/python

import os
import platform
import time
import shutil
import re
import multiprocessing
from pdb import set_trace as bp
from matplotlib import pyplot as plt

script_version = '1.0'
encoder_version = '20120202'

data_type = ['timestamp', 'frame_idx', 'target_bitrate', 'real_bitrate', 'target_fps', 'real_fps', 'PSNR', 'SSIM',
             'MD5', 'encoding_time', 'bitrate_diff', 'uid', 'is_decodable', 'orig_MD5', 'vqmg', 'target_purposed_ratio', 'unqualified_ratio']


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


def exists_dir(directory):
    return os.path.exists(directory)


def remove_dir(directory):
    if os.path.exists(directory):
        print_log(LogLevel.Info, 'Removing ' + directory)
        shutil.rmtree(directory)


def move_to_dir(old_dir, new_dir):
    os.system('mv ' + old_dir + ' ' + new_dir)


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

#on_server = 0
#need to modify if committed to github!

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
    # data_dir and sequence_dir changed
    data_dir = '/data/'   
    sequence_dir = '/data/RawSeq/'
    executable_dir = cur_abs_dir + '/Executable/Linux/'
else:
    data_dir = cur_abs_dir
    sequence_dir = cur_abs_dir + '../../UnitTest_multi_process/Sequences/'
    executable_dir = cur_abs_dir + 'Executable/Darwin/'

pic_dir = data_dir + 'pic/'
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
        sequences = {
                     'AzureLow': '201_MedianLightAprilHighMotion_20170802_640x360p30_600f',
                     'WikiText': '202_MedianLightAprilLowMotion_20170802_640x360p30_600f',
                     'Default': '401_MediumLightZehuaYurunTalk_20151224_160x90p30_100f'}
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

class Comparison:
    def __init__(self):
        #nested dict.fromkeys will lead to simutaneous update
        self.inc_ = self.generate_dict()
        self.hold_ = self.generate_dict()
        self.dec_ = self.generate_dict()

    def add_one_comparison(self, cur_scenario, type_of_data, ref_val, cur_val):
        if type_of_data == 'target_purposed_ratio':
            ref_val = abs(1 - ref_val)
            cur_val = abs(1 - cur_val)
        if ref_val > cur_val:
            self.dec_[cur_scenario][type_of_data] += 1
        elif ref_val == cur_val:
            self.hold_[cur_scenario][type_of_data] += 1
        else:
            self.inc_[cur_scenario][type_of_data] += 1
    
    def generate_dict(self):
        dic = {}
        for x in scenario:
            dic[x] = dict.fromkeys(data_type, 0)
        return dic
enc_comparison_class = Comparison()
dec_comparison_class = Comparison()

#Draw graphs for problematic clients.
def drawOneEncoderClient(cur_pic_dir, client_name, target_bitrate, real_bitrate, real_fps, PSNR, SSIM):
    plots = []
    for i in range(4):
        plots.append(plt.subplot(2, 2, i+1))
    plots[0].plot(target_bitrate[0], label='taget_bitrate(cur)', color='r')
    plots[0].plot(target_bitrate[1], label='taget_bitrate(ref)', color='b')
    plots[0].plot(real_bitrate[0], label='real_bitrate(cur)', color='r', ls=':')
    plots[0].plot(real_bitrate[1], label='real_bitrate(ref)', color='b', ls=':')
    plots[1].plot(real_fps[0], label='real_fps(cur)', color='r')
    plots[1].plot(real_fps[1], label='real_fps(ref)', color='b')
    plots[2].plot(PSNR[0], label='PSNR(cur)', color='r')
    plots[2].plot(PSNR[1], label='PSNR(ref)', color='b')
    plots[3].plot(SSIM[0], label='SSIM(cur)', color='r')
    plots[3].plot(SSIM[1], label='SSIM(ref)', color='b')
    for i in range(4):
        plots[i].legend(fontsize='x-small')
        plots[i].set_xlim(xmin=0)
    current_plot = plt.gcf()
    current_plot.savefig(cur_pic_dir + 'Enc-' + client_name + '.png', format='png', dpi = 100)
    plt.close()

def drawOneDecoderClient(cur_pic_dir, client_name, decoded_uid, real_fps, real_bitrate, PSNR, SSIM):
    plots = []
    for i in range(4):
        plots.append(plt.subplot(2, 2, i+1))

    plots[0].plot(real_fps[0], label='real_fps(cur)', color='r')
    plots[0].plot(real_fps[1], label='real_fps(ref)', color='b')
    plots[1].plot(real_fps[0], label='real_bitrate(cur)', color='r')
    plots[1].plot(real_fps[1], label='real_bitrate(ref)', color='b')
    plots[2].plot(PSNR[0], label='PSNR(cur)', color='r')
    plots[2].plot(PSNR[1], label='PSNR(ref)', color='b')
    plots[3].plot(SSIM[0], label='SSIM(cur)', color='r')
    plots[3].plot(SSIM[1], label='SSIM(ref)', color='b')

    for i in range(4):
        plots[i].legend(fontsize='x-small')
    plt.xlim(xmin = 0)
    current_plot = plt.gcf()
    current_plot.savefig(cur_pic_dir + 'Dec-' + client_name + '-for_' + decoded_uid + '.png', format='png', dpi = 100)
    plt.close()




