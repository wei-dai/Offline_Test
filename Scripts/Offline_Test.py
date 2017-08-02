#!/usr/bin/python

import multiprocessing
import os
import sys
import time

import analyse_data as ad
import analyse_overnight as ao
import analyse_regression as ar
import functions as fun
import global_parameters as gp
from pdb import set_trace as bp

os.chdir(gp.data_dir)

gp.print_log(gp.LogLevel.Normal, 'Offline test for AgoraRTCEngine')
gp.print_log(gp.LogLevel.Normal, 'Version ' + str(gp.script_version) + '\n')


def start_server():
    """
    Start the server if needed. Only for Anchor and Overnight test
    """
    iterator = 0
    os.system('chmod +x ' + gp.server.get_full_path_executable())
    while iterator < 10:
        pid = os.popen('pgrep ' + gp.server.get_executable_name()).read()

        if pid != '':
            fun.os_system('kill -9 ' + pid)

        os.system(gp.server.get_full_path_executable() + ' >>/dev/null &')

        time.sleep(0.5)

        pid = os.popen('pgrep ' + gp.server.get_executable_name()).read()

        if pid == '':
            gp.print_log(gp.LogLevel.Normal, 'Can not start or find ServerAgora Process!!\n')
            iterator += 1
        else:
            gp.print_log(gp.LogLevel.Normal, 'Server PID is ' + pid)
            break


def run_one_scenario(scenario):
    """
    Only run either Comm/Live/ScSh mode
    """
    fun.gen_dir(scenario)
    fun.check_files()

    p = multiprocessing.Pool()

    gp.print_log(gp.LogLevel.Normal, 'Scaling YUVs...')
    for seqIdx in gp.sequences:
        temp = (seqIdx,)
        p.apply_async(fun.scale_yuv, temp)
        # fun.scale_yuv(seqIdx)
    p.close()
    p.join()
    gp.print_log(gp.LogLevel.Normal, '')

    gp.client_flag = gp.mgr.list([gp.RunningState.Unfinished for _ in range(len(gp.clients))])
    p = multiprocessing.Pool()
    gp.print_log(gp.LogLevel.Normal, 'Start offline test...')

    while 1:
        # Find a unfinished cases
        gp.process_lock.acquire()
        [all_start, all_finish, start_idx, end_idx] = fun.get_next_case()
        gp.process_lock.release()
        client_num = end_idx - start_idx

        if all_finish:
            break
        if all_start:
            time.sleep(1)
            continue

        require_capacity = 0
        for client_idx in range(start_idx, end_idx):
            client = gp.clients[client_idx]
            assert isinstance(client, fun.Client)
            require_capacity += client.capacity_

        # Hold to wait enough processors
        while 1:
            gp.process_lock.acquire()
            if gp.running_process.value + client_num <= gp.active_process \
                    and gp.used_capacity.value + require_capacity <= gp.capacity:
                gp.running_process.value += client_num
                gp.used_capacity.value += require_capacity
                gp.process_lock.release()
                break
            elif gp.used_capacity.value == 0 and require_capacity > gp.capacity:
                gp.print_log(gp.LogLevel.Normal,
                             "Not enough capacity to run this case: " + gp.clients[start_idx].case_)
            gp.process_lock.release()
            time.sleep(1)

        if gp.connection_type == gp.connection[0] and os.popen('pgrep ' + gp.server.get_executable_name()).read() == '':
            os.system(gp.server.get_full_path_executable() + ' >>/dev/null &')
            gp.print_log(gp.LogLevel.Normal,
                         'Restart Server! Current Server PID is ' + os.popen('pgrep ' + gp.server.get_executable_name()).read())

        for client_idx in range(start_idx, end_idx):
            gp.process_lock.acquire()
            gp.client_flag[client_idx] = gp.RunningState.Running
            gp.process_lock.release()
            client = gp.clients[client_idx]
            assert isinstance(client, fun.Client)
            uid_dir_name = str(client.uid_) + gp.string_join + client.config_

            client_dir = gp.generate_dir_path(gp.result_dir, scenario, client.case_, uid_dir_name)
            gp.create_dir(client_dir)
            fun.os_system('cp ' + gp.network_dir + gp.networks[client.network_] + ' ' + client_dir)
            gp.client.copy_executable_to_dir(client_dir)

            if gp.connection_type == gp.connection[1]:
                log_dir = gp.generate_dir_path(gp.cur_log_dir, scenario, client.case_, uid_dir_name)
                fun.os_system('cp ' + log_dir + 'enc_online_parameters* ' + client_dir)

            gp.print_log(gp.LogLevel.Normal,
                         'Running Case ' + client.case_ + ' Client with UID ' + str(client.uid_) + ', Duration '
                         + str(client.duration_) + ', Time ' + time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time())))
            p.apply_async(fun.run_client, args = (client_idx, client_dir, scenario))
            # fun.run_client(client_idx, client_dir, scenario)
        
        gp.print_log(gp.LogLevel.Normal, '')

    p.close()
    p.join()

    if gp.mode == 'Overnight':
        gp.client_flag = gp.mgr.list([gp.RunningState.Unfinished for _ in range(len(gp.clients))])
        p = multiprocessing.Pool()
        gp.print_log(gp.LogLevel.Normal, 'Start VQM test...')

        while 1:
            # Find a unfinished cases
            gp.process_lock.acquire()
            [all_start, all_finish, start_idx, end_idx] = fun.get_next_case()
            gp.process_lock.release()

            if all_finish:
                break
            if all_start:
                time.sleep(1)
                continue

            # Hold to wait enough processors
            for client_idx in range(start_idx, end_idx):
                while 1:
                    gp.process_lock.acquire()
                    if gp.running_process.value < gp.active_process/2:
                        gp.running_process.value += 1
                        gp.process_lock.release()
                        break
                    gp.process_lock.release()
                    time.sleep(1)

                gp.process_lock.acquire()
                gp.client_flag[client_idx] = gp.RunningState.Running
                gp.process_lock.release()

                client = gp.clients[client_idx]
                assert isinstance(client, fun.Client)
                uid_dir_name = str(client.uid_) + gp.string_join + client.config_
                client_dir = gp.generate_dir_path(gp.result_dir, scenario, client.case_, uid_dir_name)
                gp.vqm_test.copy_executable_to_dir(client_dir)
                gp.decode_stream.copy_executable_to_dir(client_dir)
                gp.scale.copy_executable_to_dir(client_dir)

                gp.print_log(gp.LogLevel.Normal,
                             'Running VQM Case ' + client.case_ + ' Client with UID ' + str(client.uid_) + ', Duration '
                             + str(client.duration_) + ', Time ' + time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time())))
                p.apply_async(fun.run_vqm, args = (client_idx, client_dir))
                # fun.run_vqm(client_idx, client_dir)

            gp.print_log(gp.LogLevel.Normal, '')

        p.close()
        p.join()

    fun.saving_logs(scenario)

    if gp.scenario_crash.value != 0:
        gp.print_log(gp.LogLevel.Normal, 'Total ' + str(gp.scenario_crash.value) + ' crashes in for ' + scenario + '!!!')
        gp.total_crash += gp.scenario_crash.value
        gp.scenario_crash.value = 0


def run_test():
    """
    Start running the test
    """
    is_match = True
    for scenario in gp.scenario:
        fun.config_test_case(scenario)
        run_one_scenario(scenario)

        if gp.mode == 'Regression' and gp.connection_type == gp.connection[1]:
            gp.print_log(gp.LogLevel.Normal, 'Analyzing Results')
            is_match = is_match & ar.analyse_data(scenario, gp.cur_log_dir, gp.ref_log_dir)
            gp.print_log(gp.LogLevel.Normal, 'Finish Analyzing Results')
        elif gp.mode == 'Overnight':
            gp.print_log(gp.LogLevel.Normal, 'Analyzing Results')
            ao.generate_data(scenario)
            gp.print_log(gp.LogLevel.Normal, 'Finish Analyzing Results')

        gp.print_log(gp.LogLevel.Normal, '')

    if gp.mode == 'Overnight' and gp.ref_log_dir != '':
        gp.print_log(gp.LogLevel.Normal, 'Comparing Results')
        result = ad.compare_data()
        gp.print_log(gp.LogLevel.Normal, 'Finish Comparing Results')
    
    gp.print_log(gp.LogLevel.Normal, '')

    if gp.mode == 'Regression' and gp.connection_type == gp.connection[1]:
        result = ar.output_mismatch_case(gp.cur_log_dir, gp.ref_log_dir)
        fun.send_unit_test_email(result)
    else:
        if gp.mode == 'Overnight' and gp.ref_log_dir != '' and gp.on_server == 1:
            fun.send_server_test_email(result)

        pid = os.popen('pgrep ' + gp.server.get_executable_name()).read()
        if pid != '':
            fun.os_system('kill -9 ' + pid)

    fun.clean_up(is_match)

    gp.print_log(gp.LogLevel.Normal, 'Finish Running Client!!!!')


def set_up(log_folder_prefix):
    """
    tmp
    """
    if sys.argv[2] == 'save_log':
        gp.save_to_backup_dir = True
    else:
        gp.save_to_backup_dir = False

    gp.cur_commit_id = sys.argv[3][0:7]
    gp.commit_time = int(sys.argv[4])
    if len(sys.argv) == 5:
        gp.ref_commit_id = ao.find_latest_ref_log('')
    else:
        gp.ref_commit_id = ao.find_latest_ref_log(sys.argv[5][0:7])
    gp.cur_log_dir = log_folder_prefix + gp.folder_join + gp.cur_commit_id + gp.folder_join + str(gp.commit_time) + '/'
    gp.create_dir(gp.cur_log_dir)


if __name__ == '__main__':
    t = time.time()
    gp.print_log_filter = gp.LogLevel.Normal
    run = 2
    if len(sys.argv) < 2:
        gp.print_log(gp.LogLevel.Normal, 'Not enough input!')
        exit()

    gp.log_file = open(sys.argv[1] + '.log', 'w', 0)

    if sys.argv[1] == 'Regression':
        gp.mode = 'Regression'
        gp.cur_log_dir = gp.data_dir + 'Anchor/'
        gp.create_dir(gp.cur_log_dir)
        gp.ref_log_dir = gp.data_dir + 'Test/'
        gp.create_dir(gp.ref_log_dir)
        if len(sys.argv) >= 4:
            gp.ref_commit_id = sys.argv[2][0:7]
            gp.cur_commit_id = sys.argv[3][0:7]
    elif sys.argv[1] == 'Overnight':
        gp.mode = 'Overnight'
        gp.backup_log_dir = gp.data_dir + 'Backups/'
        set_up(gp.data_dir + gp.cur_time)
        run = 1
    else:
        gp.print_log(gp.LogLevel.Normal, 'Error configure!')
        exit()

    for iteration in range(0, run):
        gp.connection_type = gp.connection[iteration]
        if gp.connection_type == gp.connection[0]:
            start_server()
        run_test()

    if type(gp.log_file) == file:
        gp.log_file.close()

    gp.print_log(gp.LogLevel.Normal, 'Totally ' + str(int(time.time() - t + 30) / 60) + ' minutes!')
