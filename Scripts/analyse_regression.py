#!/usr/bin/python

import os
import re
import sys

import data_class as dc
import global_parameters as gp


def analyse_data(scenario, anchor, test):
    anchor_dir = gp.generate_dir_path(anchor, scenario)
    test_dir = gp.generate_dir_path(test, scenario)
    is_match = True

    if os.path.isdir(test_dir) and os.path.isdir(anchor_dir):
        room_list = os.listdir(test_dir)
        for room in room_list:
            test_room_dir = gp.generate_dir_path(test_dir, room)
            anchor_room_dir = gp.generate_dir_path(anchor_dir, room)
            if os.path.isdir(test_room_dir) and os.path.isdir(anchor_room_dir):
                uid_list = os.listdir(test_room_dir)
                is_room_totally_match = True
                for uid in uid_list:
                    test_uid_dir = gp.generate_dir_path(test_room_dir, uid)
                    anchor_uid_dir = gp.generate_dir_path(anchor_room_dir, uid)
                    if not os.path.isdir(test_uid_dir):
                        continue

                    case = uid.split(gp.string_join)
                    case[0] = int(case[0])
                    if os.path.isdir(test_uid_dir) and os.path.isdir(anchor_uid_dir):
                        result = analyse_encoder_data(anchor_uid_dir, test_uid_dir)
                        is_match = is_match & result
                        is_room_totally_match = is_room_totally_match & result

                doc_list = os.listdir(test_room_dir)
                for doc in doc_list:
                    if re.search('crash.txt', doc):
                        is_room_totally_match = False
                        is_match = False
                        
                doc_list = os.listdir(anchor_room_dir)
                for doc in doc_list:
                    if re.search('crash.txt', doc):
                        is_room_totally_match = False
                        is_match = False

                if is_room_totally_match:
                    gp.remove_dir(test_room_dir)
                    gp.remove_dir(anchor_room_dir)

    if is_match == 0:
        gp.print_log(gp.LogLevel.Normal, '\nMismatch Detected!!!\n')
    else:
        gp.print_log(gp.LogLevel.Normal, '\nAll Match!!!\n')

    return is_match


def analyse_encoder_data(anchor_dir, test_dir):
    anchor_list = os.listdir(anchor_dir)
    test_list = os.listdir(test_dir)
    a_file = ''
    t_file = ''

    for anchor_file in anchor_list:
        if re.search('enc_offline_test_0', anchor_file):
            a_file = open(anchor_dir + anchor_file, 'r')
            break

    for test_file in test_list:
        if re.search('enc_offline_test_0', test_file):
            t_file = open(test_dir + test_file, 'r')
            break

    if a_file == '' or t_file == '':
        return False

    # Read the header line
    anchor_data = dc.ResultRecorder(a_file.readline())
    test_data = dc.ResultRecorder(t_file.readline())

    is_match = True

    while anchor_data.add_one_fame_result(a_file.readline()) == 0 \
            and test_data.add_one_fame_result(t_file.readline()) == 0:
        if anchor_data.get_current_md5() != test_data.get_current_md5():
            is_match = False

    a_file.close()
    t_file.close()

    return is_match


class MisMatchPacket():
    def __init__(self):
        self.case_ = ''
        self.number_ = 0


def add_one_case(result_packet, case):
    result_packet.number_ += 1
    if result_packet.case_ == '':
        result_packet.case_ += '<table border="1">\n'

    if result_packet.number_ % 5 == 1:
        result_packet.case_ += '<tr align="center">'

    result_packet.case_ += '<td>' + case + '</td>'
    if result_packet.number_ % 5 == 0:
        result_packet.case_ += '</tr>\n'
    return result_packet


def finish_one_case(result_packet):
    if result_packet.number_ % 5 != 0:
        result_packet.case_ += '</tr>\n'
    if result_packet.number_ != 0:
        result_packet.case_ += '</table>\n'
    return result_packet


def output_mismatch_case(anchor, test):
    result = '<html>\n<head>\n'

    for scenario in gp.scenario:
        anchor_dir = gp.generate_dir_path(anchor, scenario)
        test_dir = gp.generate_dir_path(test, scenario)
        header = '<hr>\n'
        header += '<h2>\nComparing ' + scenario + ' result:\n</h2>\n'
        result += header
        mismatch_packet = MisMatchPacket()
        crash_packet = MisMatchPacket()
        if os.path.isdir(test_dir):
            room_list = os.listdir(test_dir)
            for room in room_list:
                test_room_dir = gp.generate_dir_path(test_dir, room)
                anchor_room_dir = gp.generate_dir_path(anchor_dir, room)
                if os.path.isdir(test_room_dir) and os.path.isdir(anchor_room_dir):
                    is_crash = False

                    doc_list = os.listdir(test_room_dir)
                    for doc in doc_list:
                        if re.search('crash.txt', doc):
                            is_crash = True

                    doc_list = os.listdir(anchor_room_dir)
                    for doc in doc_list:
                        if re.search('crash.txt', doc):
                            is_crash = True

                    if is_crash:
                        crash_packet = add_one_case(crash_packet, room)
                    else:
                        mismatch_packet = add_one_case(mismatch_packet, room)

            crash_packet = finish_one_case(crash_packet)
            mismatch_packet = finish_one_case(mismatch_packet)

            if crash_packet.number_ == 0 and mismatch_packet.number_ == 0:
                result += '<p>All Match!!!</p>\n'
            else:
                if mismatch_packet.number_ != 0:
                    result += '<p>Mismatch Case:</p>\n'
                    result += mismatch_packet.case_
                if crash_packet.number_!= 0:
                    result += '<p>Crash Case:</p>\n'
                    result += crash_packet.case_

    result += '</head>\n</html>\n'
    return result


if __name__ == '__main__':
    for sc in gp.scenario:
        analyse_data(sc, sys.argv[1], sys.argv[2])

    output_mismatch_case(sys.argv[1], sys.argv[2])
