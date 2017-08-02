#!/usr/bin/python

import os
import re
import sys

import data_class as dc
import global_parameters as gp
from pdb import set_trace as bp


def find_latest_ref_log(commit_id):
    gp.ref_log_dir = ''
    ref_file = ''
    if os.path.isdir(gp.backup_log_dir):
        zip_list = os.listdir(gp.backup_log_dir)
        time_commit = 0
        time_run = 0
        for zip_file in zip_list:
            tmp = zip_file.split('.')[0].split(gp.folder_join)
            # to avoid .DS_Store file problem
            if tmp[0] != '':
                time_run_tmp = int(tmp[0])
                time_commit_id_tmp = tmp[1]
                time_commit_tmp = int(tmp[2])
                if commit_id != '':
                    if re.search(commit_id, time_commit_id_tmp) and time_run < time_run_tmp:
                        time_run = time_run_tmp
                        ref_file = zip_file
                else:
                    if time_commit < time_commit_tmp:
                        if time_run < time_run_tmp:
                            time_run = time_run_tmp
                            time_commit = time_commit_tmp
                            commit_id = tmp[1]
                            ref_file = zip_file

    if ref_file != '':
        gp.print_log(gp.LogLevel.Normal, 'Selected commit id is ' + commit_id)
        
        os.system('unzip -oq ' + gp.backup_log_dir + ref_file + ' -d ' + gp.data_dir)
        gp.ref_log_dir = gp.generate_dir_path(gp.data_dir, ref_file.split('.')[0])

        return commit_id[0:7]

    gp.print_log(gp.LogLevel.Normal, 'No commit is available!!!')
    return ''


def generate_data(scenario):
    enc_result_file = open(gp.cur_log_dir + 'Enc_File_' + scenario + '_'
                           + gp.cur_time + '_' + gp.cur_commit_id + '.txt', 'w')
    dec_result_file = open(gp.cur_log_dir + 'Dec_File_' + scenario + '_'
                           + gp.cur_time + '_' + gp.cur_commit_id + '.txt', 'w')

    anchor_dir = gp.cur_log_dir + scenario
    if os.path.isdir(anchor_dir):
        room_list = os.listdir(anchor_dir)
        for room in room_list:
            room_dir = gp.generate_dir_path(anchor_dir, room)
            if os.path.isdir(room_dir):
                # Encoder result analyse
                enc_result = analyse_encoder_for_one_room(room_dir, room)
                enc_result_file.write(enc_result)

                # Decoder result analyse
                dec_result = analyse_decoder_for_one_room(room_dir, room)
                dec_result_file.write(dec_result)

    enc_result_file.close()
    dec_result_file.close()


def analyse_encoder_for_one_room(room_dir, room):
    output = ''
    client_list = os.listdir(room_dir)
    for client in client_list:
        output += room + gp.string_join + client + '\n'
        client_dir = gp.generate_dir_path(room_dir, client)
        if os.path.isdir(client_dir):
            anchor_list = os.listdir(client_dir)
            for anchor_file in anchor_list:
                if re.search('enc_offline_test_0', anchor_file):
                    output += analyse_encoder_for_one_client(client_dir + anchor_file)
                    break
        else:
            gp.print_log(gp.LogLevel.Normal, 'Error: Folders do not exist! ' + room_dir + client)
            exit()

    return output


def analyse_encoder_for_one_client(file_name):
    fp = open(file_name, 'r')
    enc_data = dc.ResultRecorder(fp.readline())
    while enc_data.add_one_fame_result(fp.readline()) == 0:
        pass
    fp.close()

    return enc_data.get_data_total_str()


def analyse_decoder_for_one_room(room_dir, room):
    output = ''
    client_list = os.listdir(room_dir)
    for client in client_list:
        output += room + gp.string_join + client + '\n'
        client_dir = gp.generate_dir_path(room_dir, client)
        if os.path.isdir(client_dir):
            anchor_list = os.listdir(client_dir)
            result = []
            for anchor_file in anchor_list:
                if re.search('dec_offline_test', anchor_file):
                    result.append(analyse_decoder_for_one_client(client_dir + anchor_file))

            for data in result:
                found = False
                for anchor_file in anchor_list:
                    if re.search('vqmg_' + data[1][1] + '.', anchor_file):
                        vqmg_file = client_dir + anchor_file
                        fp = open(vqmg_file, 'r')
                        fp.readline()
                        tmp = fp.readline().split('\n')[0].split('\t')[-1]
                        fp.close()
                        data[1][0] = data[1][0] + 'vqmg\t' + tmp + '\n'
                        found = True

                if not found:
                    data[1][0] = data[1][0] + 'vqmg\t0\n'

            result.sort()
            for idx in range(0, len(result)):
                output += 'For' + gp.string_join + 'UID' + gp.string_join + str(result[idx][0]) + '\n'
                output += result[idx][1][0]
        else:
            gp.print_log(gp.LogLevel.Normal, 'Error: Folders do not exist! ' + client_dir)
            exit()

    return output


def analyse_decoder_for_one_client(file_name):
    suffix = file_name.split('/')[-1].split('.')[0].split('_')[-1]
    fp = open(file_name, 'r')
    dec_data = dc.ResultRecorder(fp.readline())
    while dec_data.add_one_fame_result(fp.readline()) == 0:
        pass
    fp.close()

    return dec_data.get_current_uid(), [dec_data.get_data_total_str(), suffix]


if __name__ == '__main__':
    gp.cur_log_dir = sys.argv[1]
    if gp.cur_log_dir[-1] != '/':
        gp.cur_log_dir += '/'
    for sc in gp.scenario:
        generate_data(sc)
