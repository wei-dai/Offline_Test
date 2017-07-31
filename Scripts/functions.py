#!/usr/bin/python

import getpass
import os
import re
import smtplib
import time
from email.header import Header
from email.mime.text import MIMEText

import global_parameters as gp
import test_cases as tc
from pdb import set_trace as bp


def os_system(cmd):
    gp.print_log(gp.LogLevel.Info, cmd)
    # return os.system(cmd+' >>log.txt')
    return os.system(cmd + ' >>/dev/null')
    # return os.system(cmd)


def send_unit_test_email(content):
    header = '<html>\n<head>\n'
    header += '<h1>\nThis email is the regression comparison results\n</h1>'
    # In Regression, the cur_log_dir is the old one and ref is the new one
    header += '<h2>\n Current Commit:\n</h2>' + gp.read_commit_log(gp.ref_log_dir)
    header += '<h2>\n Ref Commit:\n</h2>' + gp.read_commit_log(gp.cur_log_dir)

    if gp.total_crash != 0:
        header += '<h2>\n Total Crash: ' + str(gp.total_crash) + '\n</h2>'
    else:
        header += '<h2>\n No Crash.\n</h2>'
    content = header + content

    if gp.cur_platform == 'Linux':
        subject = 'Server Regression Test Result! Time: ' \
                  + time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        if type(gp.log_file) == file:
            gp.log_file.close()
            utils.send_alert_email2([subject, content, open('Regression.log', 'rb').read()],
                                    ['daiwei@agora.io', 'loujian@agora.io', 'chenqianzong@agora.io', 'lijiali@agora.io'],
                                    'outlook')
        else:
            utils.send_alert_email([(subject, content)],
                                   ['daiwei@agora.io', 'loujian@agora.io', 'chenqianzong@agora.io', 'lijiali@agora.io'],
                                   'outlook')
    else:
        trial_time = 0
        while trial_time < 5:
            mail_user = raw_input('Please enter your email: ')
            if mail_user == 'skip':
                gp.print_log(gp.LogLevel.Normal, 'skip sending the email')
                return
            mail_pass = getpass.getpass('Please enter your password: ')
            try:
                smtp_obj = smtplib.SMTP('smtp.office365.com', 587)
                smtp_obj.starttls()
                smtp_obj.ehlo()
                smtp_obj.login(mail_user, mail_pass)
                break
            except smtplib.SMTPException:
                trial_time += 1
                gp.print_log(gp.LogLevel.Normal, 'Error login data, please enter again!')

        if trial_time == 5:
            gp.print_log(gp.LogLevel.Normal,
                         'Exceed maximum times of trial, please check your email and password again!')
            smtp_obj.close()
            return

        sender = mail_user
        receivers = ['video-team@agora.io']

        body = '<h1>The Offline Test anchor has been updated</h1>\n'
        mail_body = raw_input('Please enter a short description in one line: ')
        body = body + '<p>' + mail_body + '</p>\n' + content
        message = MIMEText(body, 'html', 'utf-8')

        subject = 'Offline Test Anchor Update'
        message['Subject'] = Header(subject, 'utf-8')

        smtp_obj.sendmail(sender, receivers, message.as_string())
        smtp_obj.close()

    gp.print_log(gp.LogLevel.Normal, 'Success send the email!')


def send_server_test_email(content):
    subject = 'Server Overnight Test Result! Time: ' + time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    if gp.cur_platform == 'Linux':
        if type(gp.log_file) == file:
            gp.log_file.close()
            utils.send_alert_email2([subject, content, open('Overnight.log', 'rb').read()],
                                    ['daiwei@agora.io', 'loujian@agora.io', 'chenqianzong@agora.io', 'lijiali@agora.io'],
                                    'outlook')
        else:
            utils.send_alert_email([(subject, content)],
                                   ['daiwei@agora.io', 'loujian@agora.io', 'chenqianzong@agora.io', 'lijiali@agora.io'],
                                   'outlook')
    else:
        trial_time = 0
        while trial_time < 5:
            mail_user = raw_input('Please enter your email: ')
            if mail_user == 'skip':
                gp.print_log(gp.LogLevel.Normal, 'skip sending the email')
                return
            mail_pass = getpass.getpass('Please enter your password: ')
            try:
                smtp_obj = smtplib.SMTP('smtp.office365.com', 587)
                smtp_obj.starttls()
                smtp_obj.ehlo()
                smtp_obj.login(mail_user, mail_pass)
                break
            except smtplib.SMTPException:
                trial_time += 1
                gp.print_log(gp.LogLevel.Normal, 'Error login data, please enter again!')

        if trial_time == 5:
            gp.print_log(gp.LogLevel.Normal,
                         'Exceed maximum times of trial, please check your email and password again!')
            smtp_obj.close()
            return

        sender = mail_user
        receivers = ['video-team@agora.io']

        message = MIMEText(content, 'html', 'utf-8')

        message['Subject'] = Header(subject, 'utf-8')

        smtp_obj.sendmail(sender, receivers, message.as_string())
        smtp_obj.close()

    if gp.cur_platform == 'Linux' and gp.on_server == 0:
        gp.print_log(gp.LogLevel.Normal, 'Skip send email!')
    else:
        gp.print_log(gp.LogLevel.Normal, 'Success send the email!')


def saving_logs(scenario):
    result_dir = gp.generate_dir_path(gp.result_dir, scenario)
    if gp.connection_type == gp.connection[0]:
        dst_dir = gp.generate_dir_path(gp.cur_log_dir, scenario)
        os.system('cp ' + gp.client.dir_ + 'commit.log ' + gp.cur_log_dir)
    else:
        dst_dir = gp.generate_dir_path(gp.ref_log_dir, scenario)
        os.system('cp ' + gp.client.dir_ + 'commit.log ' + gp.ref_log_dir)

    room_list = os.listdir(result_dir)

    for room in room_list:
        if os.path.isdir(result_dir + room):
            uid_list = os.listdir(result_dir + room)
            room_dir = gp.generate_dir_path(result_dir, room)
            for uid in uid_list:
                if os.path.isdir(room_dir + uid):
                    cur_uid_dir = gp.generate_dir_path(room_dir, uid)

                    doc_list = os.listdir(cur_uid_dir)
                    dst_uid_dir = gp.generate_dir_path(dst_dir, room, uid)
                    gp.create_dir(dst_uid_dir)
                    for doc in doc_list:
                        if re.search('enc_offline_test_0', doc) \
                                or re.search('enc_online_parameters', doc) \
                                or re.search('enc_save_sent_stream', doc) \
                                or re.search('enc_save_stream_info_0', doc):
                            os.system('cp ' + cur_uid_dir + doc + ' ' + dst_uid_dir)
                        if gp.mode == 'Overnight':
                            if re.search('dec_offline_test', doc) \
                                    or re.search('dec_save_stream_info', doc) \
                                    or re.search('dec_quality_score', doc) \
                                    or re.search('dec_save_stream_received', doc) \
                                    or re.search('vqmg', doc) \
                                    or re.search('crash', doc) \
                                    or re.search('timestamp', doc):
                                os.system('cp ' + cur_uid_dir + doc + ' ' + dst_uid_dir)


class Client:
    def __init__(self, case, idx, uid, total_client):
        orig_sequence = gp.sequences[case[7][idx]]
        self.case_ = case[0]
        self.duration_ = case[2]
        self.resolution_ = case[3][idx]
        self.rate_ = case[4][idx]
        self.fps_ = case[5][idx]
        self.network_ = case[6][idx]
        self.sequence_dir_ = gp.generate_dir_path(gp.sequence_dir, orig_sequence)
        self.room_ = int(self.case_.split(gp.folder_join)[-1], 16)
        self.uid_ = uid
        self.capacity_ = int(self.resolution_.split('x')[0]) * int(self.resolution_.split('x')[1]) \
                         * self.fps_ * (2 + total_client - 1) / 2
        tmp = orig_sequence.split('_')
        self.anchor_seq_ = tmp[0] + '_' + tmp[1] + '_' + tmp[2] + '_' + self.resolution_ + 'p' + str(self.fps_) \
                           + '_' + tmp[4] + '.yuv'
        self.config_ = 'Rate' + str(self.rate_) + gp.folder_join + 'Net' + str(self.network_) + gp.folder_join \
                       + 'FPS' + str(self.fps_) + gp.folder_join + 'Res' + self.resolution_ + gp.folder_join \
                       + 'Seq' + tmp[1]

        key = case[7][idx]
        if key in gp.seq_candidates:
            if self.anchor_seq_ not in gp.seq_candidates[key]:
                gp.seq_candidates[key].append(self.anchor_seq_)
        else:
            gp.seq_candidates[key] = [self.anchor_seq_]


def config_test_case(scenario):
    gp.seq_candidates.clear()
    room_num = 0
    gp.clients = []
    for case in tc.cases:
        if re.search(scenario, case[0]) and re.search(gp.mode, case[0]):
            uid = 0
            for idx in range(0, case[1]):
                gp.clients.append(Client(case, idx, uid, case[1]))
                uid += 1
            room_num += 1

    gp.print_log(gp.LogLevel.Normal, 'Totally ' + str(room_num) + ' cases!')


def get_next_case():
    all_start = True
    all_finish = True
    start_idx = len(gp.clients)
    end_idx = len(gp.clients)

    for x in range(0, len(gp.clients)):
        if gp.client_flag[x] != gp.RunningState.Success:
            all_finish = False
        if gp.client_flag[x] == gp.RunningState.Unfinished or gp.client_flag[x] == gp.RunningState.Crash:
            all_start = False
    if all_finish is True or all_start is True:
        return all_start, all_finish, start_idx, end_idx

    for x in range(0, len(gp.clients)):
        if gp.client_flag[x] == gp.RunningState.Unfinished or gp.client_flag[x] == gp.RunningState.Crash:
            find = 1
            room = gp.clients[x].room_
            start = x - 1
            while start >= 0:
                if gp.clients[start].room_ == room:
                    if gp.client_flag[start] == gp.RunningState.Running:
                        find = 0
                    start -= 1
                else:
                    break
            start += 1

            end = x + 1
            while end < len(gp.clients):
                if gp.clients[end].room_ == room:
                    if gp.client_flag[end] == gp.RunningState.Running:
                        find = 0
                    end += 1
                else:
                    break

            if find == 1:
                break

    if find == 0:
        return True, False, start_idx, end_idx
    else:
        return False, False, start, end


def gen_dir(scenario):
    gp.print_log(gp.LogLevel.Normal, 'Generating directories...')
    gp.print_log(gp.LogLevel.Normal, 'Creating necessary folders...')
    result_secnario_dir = gp.generate_dir_path(gp.result_dir, scenario)
    gp.create_dir(result_secnario_dir)
    if gp.connection_type == gp.connection[1]:
        ref_log_scenario_dir = gp.generate_dir_path(gp.ref_log_dir, scenario)
        gp.create_dir(ref_log_scenario_dir)
    if gp.mode == 'Overnight' and not os.path.isdir(gp.backup_log_dir):
        gp.create_dir(gp.backup_log_dir)
    if gp.mode == 'Regression':
        if gp.connection_type == gp.connection[0]:
            gp.client.set_executable_dir(gp.generate_dir_path(gp.executable_dir, 'anchor'))
        else:
            gp.client.set_executable_dir(gp.generate_dir_path(gp.executable_dir, 'test'))
    else:
        gp.client.set_executable_dir(gp.generate_dir_path(gp.executable_dir, 'overnight'))


def check_files():
    gp.print_log(gp.LogLevel.Normal, 'Checking files...')
    if not os.path.exists(gp.scale.get_full_path_executable()):
        gp.print_log(gp.LogLevel.Normal, '\tERROR!!! missing ' + gp.scale.get_executable_name())
        gp.print_log(gp.LogLevel.Normal, '\tExit.')
        exit()

    if not os.path.exists(gp.client.get_full_path_executable()):
        gp.print_log(gp.LogLevel.Normal, '\tERROR!!! missing ' + gp.client.get_executable_name())
        gp.print_log(gp.LogLevel.Normal, '\tExit.')
        exit()

    if not os.path.exists(gp.vqm_test.get_full_path_executable()) and gp.mode == 'Overnight':
        gp.print_log(gp.LogLevel.Normal, '\tERROR!!! missing ' + gp.vqm_test.get_executable_name())
        gp.print_log(gp.LogLevel.Normal, '\tExit.')
        exit()

    if not os.path.exists(gp.decode_stream.get_full_path_executable()) and gp.mode == 'Overnight':
        gp.print_log(gp.LogLevel.Normal, '\tERROR!!! missing ' + gp.decode_stream.get_executable_name())
        gp.print_log(gp.LogLevel.Normal, '\tExit.')
        exit()

    for seq_idx in gp.sequences:
        if gp.cur_platform == 'Linux':
            if not os.path.exists(gp.sequence_dir + gp.sequences[seq_idx] + '.yuv'):
                gp.print_log(gp.LogLevel.Normal,
                             '\tERROR!!! missing ' + gp.sequence_dir + gp.sequences[seq_idx] + '.yuv')
                gp.print_log(gp.LogLevel.Normal, '\tExit.')
                exit()
        else:
            if not os.path.exists(gp.sequence_dir + gp.sequences[seq_idx] + '.yuv.zip'):
                gp.print_log(gp.LogLevel.Normal,
                             '\tERROR!!! missing ' + gp.sequence_dir + gp.sequences[seq_idx] + '.yuv.zip')
                gp.print_log(gp.LogLevel.Normal, '\tExit.')
                exit()

    for network_idx in range(0, len(gp.networks)):
        if not os.path.exists(gp.network_dir + gp.networks[network_idx]):
            gp.print_log(gp.LogLevel.Normal,
                         '\tERROR!!! missing ' + gp.network_dir + gp.networks[network_idx])
            gp.print_log(gp.LogLevel.Normal, '\tExit.')
            exit()

    gp.print_log(gp.LogLevel.Normal, '\tAll Found!!!\n')


def scale_yuv(*args):
    seq_idx = args[0]
    gp.print_log(gp.LogLevel.Normal, '\tScaling ' + gp.sequences[seq_idx] + '...')
    ori_sequence = gp.sequences[seq_idx] + '.yuv'
    sequence_dir = gp.generate_dir_path(gp.sequence_dir, gp.sequences[seq_idx])
    if not os.path.exists(sequence_dir):
        gp.create_dir(sequence_dir)
    if not os.path.exists(sequence_dir + ori_sequence):
        if gp.cur_platform == 'Linux':
            os_system('cp ' + gp.sequence_dir + gp.sequences[seq_idx] + '.yuv '
                      + sequence_dir)
        else:
            os_system('unzip ' + gp.sequence_dir + gp.sequences[seq_idx] + '.yuv.zip -d '
                      + sequence_dir)

    tmp = ori_sequence.split('_')
    ori_width = int(tmp[-2].split('x')[0])
    ori_height = int(tmp[-2].split('x')[1].split('p')[0])
    ori_fps = int(tmp[-2].split('x')[1].split('p')[1])

    for seq_name in gp.seq_candidates[seq_idx]:
        tmp_seq_name = seq_name.split('_')
        width = int(tmp_seq_name[3].split('p')[0].split('x')[0])
        height = int(tmp_seq_name[3].split('p')[0].split('x')[1])
        fps = int(tmp_seq_name[3].split('p')[1])

        scale_seq_name = ori_sequence
        scale_width = ori_width
        scale_height = ori_height
        if width * ori_height != height * ori_width:
            if width * 1.0 / height < ori_width * 1.0 / ori_height:
                scale_width = ori_height * width / height
                scale_height = ori_height
            else:
                scale_width = ori_width
                scale_height = ori_width * height / width

            scale_seq_name = tmp[0] + '_' + tmp[1] + '_' + tmp[2] + '_' \
                             + str(scale_width) + 'x' + str(scale_height) + 'p' \
                             + str(ori_fps) + '_' + tmp[4]
            if not os.path.exists(sequence_dir + scale_seq_name):
                os_system(gp.scale.get_full_path_executable() + ' ' + str(ori_width) + ' ' + str(ori_height) + ' '
                          + str(scale_width) + ' ' + str(scale_height) + ' '
                          + sequence_dir + ori_sequence + ' '
                          + sequence_dir + scale_seq_name + ' 4 1')
                gp.print_log(gp.LogLevel.Normal, 'Scaling ' + scale_seq_name)

        if not os.path.exists(sequence_dir + seq_name):
            os_system(gp.scale.get_full_path_executable() + ' ' + str(scale_width) + ' ' + str(scale_height) + ' '
                      + str(width) + ' ' + str(height) + ' ' + sequence_dir
                      + scale_seq_name + ' ' + sequence_dir + seq_name + ' 3 '
                      + str(ori_fps) + ' ' + str(fps))
            gp.print_log(gp.LogLevel.Normal, 'Scaling ' + seq_name)


def clean_up(is_match):
    gp.print_log(gp.LogLevel.Normal, 'Cleaning Up Folders')
    anchor_result_dir = gp.result_dir[:-1] + '_anchor/'
    if gp.connection_type == gp.connection[1]:
        if is_match:
            gp.remove_dir(gp.cur_log_dir)
            gp.remove_dir(gp.ref_log_dir)
            gp.remove_dir(gp.result_dir)
            gp.remove_dir(anchor_result_dir)
            if gp.cur_platform != 'Linux':
                for seqIdx in gp.sequences:
                    gp.remove_dir(gp.sequence_dir + gp.sequences[seqIdx])
        else:
            gp.remove_dir(gp.result_dir)
            gp.remove_dir(anchor_result_dir)
    elif gp.connection_type == gp.connection[0]:
        if gp.mode == 'Overnight':
            if gp.save_to_backup_dir:
                gp.create_dir(gp.backup_log_dir)
                gp.zip_to_folder(gp.cur_log_dir[:-1] + '.zip', gp.cur_log_dir, gp.backup_log_dir)

                gp.create_dir(gp.temp_dir)
                zip_name = gp.cur_time + gp.folder_join + gp.cur_commit_id[0:7] + '.zip'
                gp.zip_to_folder(zip_name, gp.result_dir, gp.temp_dir)

            gp.remove_dir(gp.cur_log_dir)
            gp.remove_dir(gp.ref_log_dir)
            gp.remove_dir(gp.result_dir)
        else:
            gp.remove_dir(anchor_result_dir)
            os_system('mv ' + gp.result_dir + ' ' + anchor_result_dir)
        gp.print_log(gp.LogLevel.Normal, 'Finish Cleaning Up Folders')


def find_corresponding_orig_yuv(case, uid):
    for client in gp.clients:
        if client.case_ == case and client.uid_ == uid:
            return client.sequence_dir_ + client.anchor_seq_


def calculate_running_time(doc):
    gp.print_log(gp.LogLevel.Debug, 'Entering calculate_running_time at directory ' + os.getcwd() + ' with doc ' + doc)
    fp = open(doc, 'r')
    start_time = end_time = 0
    for lines in fp:
        end_time = int(lines.split('\n')[0])
        if start_time == 0:
            start_time = end_time

    gp.print_log(gp.LogLevel.Debug, 'Start time is ' + str(start_time) + ', End time is ' + str(end_time))

    if end_time < start_time:
        end_time += 1000000

    fp.close()

    gp.print_log(gp.LogLevel.Debug, 'Finish calculate_running_time at directory ' + os.getcwd() + ' with doc ' + doc)

    return (end_time - start_time) / 1000


def running_with_delay(client):
    gp.print_log(gp.LogLevel.Debug,
                 'Entering running_with_delay at directory ' + os.getcwd() + ' with client '
                 + client.case_ + ' UID ' + str(client.uid_))
    assert isinstance(client, Client)
    running_time = 0
    doc_list = os.listdir('./')
    for doc in doc_list:
        if re.search('_timestamp_', doc):
            running_time = calculate_running_time(doc)
            if running_time > client.duration_ + 2:
                gp.print_log(gp.LogLevel.Normal,
                             'Error Running Case ' + client.case_ + ' Client with UID ' + str(client.uid_)
                             + ', Duration ' + str(client.duration_) + '. Running Time not sufficient '
                             + str(running_time) + ' seconds with documents ' + doc)
                gp.print_log(gp.LogLevel.Normal,
                             'Used capacity ' + str(gp.used_capacity.value))
                return True

    gp.print_log(gp.LogLevel.Debug,
                 'Success Running Case ' + client.case_ + ' Client with UID ' + str(client.uid_)
                 + ', Duration ' + str(client.duration_) + ', Running Time totally sufficient '
                 + str(running_time) + ' seconds with dir ' + os.getcwd())

    return False


def run_client(*args):
    success = gp.RunningState.Unfinished
    cmd = ''
    client = gp.clients[args[0]]
    assert isinstance(client, Client)

    tmp = client.resolution_.split('x')
    width = int(tmp[0])
    height = int(tmp[1])
    try:
        cur_pid = os.popen('pgrep ' + gp.server.get_executable_name()).read()
        if gp.connection_type == gp.connection[0] and cur_pid == '':
            gp.print_log(gp.LogLevel.Normal,
                         'Can not find ServerAgora process, Exit ' + str(client.room_) + ' and uid ' + str(client.uid_))
            return

        time.sleep(1)

        client_dir = args[1]
        scenario = args[2]
        os.chdir(client_dir)
        cmd = gp.client.get_executable_name() + ' ' + str(client.room_) + ' ' + str(client.uid_) + ' ' \
              + str(client.fps_) + ' ' + str(width) + ' ' + str(height) + ' ' + str(client.rate_) + ' ' \
              + client.sequence_dir_ + client.anchor_seq_ + ' ' \
              + tc.suit[client.case_.split(gp.folder_join)[0]][0] + ' ' + tc.suit[client.case_.split(gp.folder_join)[0]][1] + ' ' \
              + tc.suit[client.case_.split(gp.folder_join)[0]][2] + ' ' + gp.networks[client.network_] + ' ' + str(client.duration_)

        start_time = time.time()
        if gp.cur_platform == 'Linux':
            result = os_system('LD_LIBRARY_PATH=' + gp.result_dir + scenario + ' ./' + cmd)
        else:
            result = os_system('./' + cmd)
        end_time = time.time()

        time.sleep(1)
        # Clean the zero byte doc and also removing the time prefix
        doc_list = os.listdir('./')
        for doc in doc_list:
            if os.path.getsize(doc) == 0:
                os_system('rm -rf ' + doc)
            else:
                t = re.search('..?h_..?m_..?s_', doc)
                if t is not None:
                    new_file = doc.replace(t.group(0), '')
                    if not os.path.exists(new_file) or os.path.getsize(new_file) < os.path.getsize(doc):
                        os_system('mv ' + doc + ' ' + new_file)
                    elif os.path.exists(new_file):
                        os_system('rm ' + doc)

        gp.print_log(gp.LogLevel.Debug,
                     'Start checking time of ' + client.case_ + ' Client with UID ' + str(client.uid_) + ', Duration '
                     + str(client.duration_) + ', Running Time ' + str(end_time - start_time) + ' seconds.')

        if running_with_delay(client):
            return

        gp.print_log(gp.LogLevel.Debug,
                     'Finish checking time of ' + client.case_ + ' Client with UID ' + str(client.uid_) + ', Duration '
                     + str(client.duration_) + ', Running Time ' + str(end_time - start_time) + ' seconds.')

        time.sleep(1)

        os.chdir(gp.data_dir)

        pid_temp = os.popen('pgrep ' + gp.server.get_executable_name()).read()
        if gp.connection_type == gp.connection[0] and (pid_temp == '' or pid_temp != cur_pid):
            gp.print_log(gp.LogLevel.Normal,
                         'ServerAgora is down, Re-run the process with case ' + client.case_ + ' and uid '
                         + str(client.uid_) + ' ' + time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time())))
            return

        if end_time - start_time > client.duration_ + 6:
            gp.print_log(gp.LogLevel.Normal,
                         'Case ' + client.case_ + ' Client with UID ' + str(client.uid_) + ', Duration '
                         + str(client.duration_) + ', Running Time ' + str(end_time - start_time)
                         + ' seconds which is larger than expected ' + str(client.duration_))
            gp.print_log(gp.LogLevel.Normal, 'Command Line is ' + cmd)

        if result != 0:
            gp.print_log(gp.LogLevel.Normal,
                         'Case ' + client.case_ + ' Client with UID ' + str(client.uid_)
                         + ', Duration ' + str(client.duration_) + ' Crashed!!!!!')
            gp.print_log(gp.LogLevel.Normal, 'Command Line is ' + cmd)
            success = gp.RunningState.Crash
            gp.scenario_crash.value += 1
        else:
            gp.print_log(gp.LogLevel.Debug,
                         'Finish Running Case ' + client.case_ + ' Client with UID ' + str(client.uid_) + ', Duration '
                         + str(client.duration_) + ', Running Time '
                         + str(end_time - start_time) + ' seconds.')
            success = gp.RunningState.Success

    finally:
        if success == gp.RunningState.Unfinished:
            gp.print_log(gp.LogLevel.Normal,
                         'Rerun Running Case ' + client.case_ + ' Client with UID ' + str(client.uid_)
                         + ', Duration ' + str(client.duration_) + '. Check it out!!!!!')
            gp.print_log(gp.LogLevel.Normal, 'Command Line is ' + cmd)

        if success == gp.RunningState.Crash:
            file_crash = open(client_dir + '../crash.txt', 'a')
            file_crash.write(cmd)
            file_crash.close()

        gp.process_lock.acquire()
        gp.client_flag[args[0]] = success
        gp.running_process.value -= 1
        gp.used_capacity.value -= client.capacity_
        gp.process_lock.release()


def run_vqm(*args):
    success = gp.RunningState.Unfinished
    try:
        client = gp.clients[args[0]]
        assert isinstance(client, Client)

        tmp = client.resolution_.split('x')
        width = int(tmp[0])
        height = int(tmp[1])

        if width * height > 1280 * 720:
            gp.print_log(gp.LogLevel.Normal, 'VQM skip due to large resolution')
            success = gp.RunningState.Success
            return

        client_dir = args[1]
        os.chdir(client_dir)

        vqm_result = 0
        doc_list = os.listdir('./')
        for doc in doc_list:
            if re.search('dec_save_stream_received', doc):
                handle = doc.split('.')[0].split('_')[-1]
                decode_yuv = 'dec_save_reconstructed_yuv_' + handle + '.yuv'
                os_system('./' + gp.decode_stream.get_executable_name() + ' ' + doc + ' ' + decode_yuv)
                for score_file in doc_list:
                    if re.search('dec_quality_score_' + handle, score_file):
                        break
                for uid_file in doc_list:
                    if re.search('dec_offline_test_' + handle, uid_file):
                        fp = open(uid_file, 'r')
                        fp.readline()
                        data = fp.readline()
                        ref_uid = int(data.split('\t')[1])
                        fp.close()
                        break
                ref_sequence = find_corresponding_orig_yuv(client.case_, ref_uid)
                vqm_result = os_system('./' + gp.vqm_test.get_executable_name() + ' ' + str(ref_sequence) + ' ' 
                                       + decode_yuv + ' ' + str(score_file) + ' ' + str(width) + ' ' 
                                       + str(height) + ' ' + str(client.fps_) + ' ' + str(client.duration_) 
                                       + ' psnr_ssim_' + handle + '.xls' + ' vqmg_' + handle + '.xls')
                os.system('rm *.yuv')
        os.chdir(gp.data_dir)

        if vqm_result != 0:
            gp.print_log(gp.LogLevel.Normal, 'VQM return ' + str(vqm_result))
            success = gp.RunningState.Success
        else:
            success = gp.RunningState.Success

    finally:
        gp.process_lock.acquire()
        gp.client_flag[args[0]] = success
        gp.running_process.value -= 1
        gp.process_lock.release()
