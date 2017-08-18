import os
import re
import sys
import case_class as cc
import global_parameters as gp

def generate_header(*l):
	res = '<tr align="center">\n'
	for item in l:
		res += '<th>' + item + '</th>'
	res += '</tr>\n'
	return res


def generate_one_cell(value, lower_range = None, higher_range = None):
	cell = '<td>'
	fail = 0
	if isinstance(value, str):
		cell += value
	elif isinstance(value, tuple):
		for data in value:
			if lower_range is not None and higher_range is not None \
					and (data < lower_range or data > higher_range):
				cell += '<span style="color: red">%.2f</span> / ' % data
				fail = 1
			else:
				cell += '%.2f / ' % data
		cell = cell[:-3]
	elif isinstance(value, float):
		if lower_range is not None and higher_range is not None and (value < lower_range or value > higher_range):
			cell += '<span style="color: red">%.2f</span>' % value
			fail = 1
		else:
			cell += '%.2f' % value
	else:
		gp.print_log(gp.LogLevel.Normal, 'Error type in GenerateCrossRowCell ' + str(type(value)))
		exit()
	cell += '</td>'
	return cell, fail


def generate_cross_row_cell(value, row = 1):
	if isinstance(value, str):
		return '<td rowspan="' + str(row) + '">' + value + '</td>'
	elif isinstance(value, float):
		return '<td rowspan="' + str(row) + '">' + ('%.2f' % value) + '</td>'
	else:
		gp.print_log(gp.LogLevel.Normal, 'Error type in GenerateCrossRowCell ' + type(value))
		exit()


def generate_one_row(*l):
	res = '<tr>'
	for item in l:
		if isinstance(item, float):
			res += '<td>%.2f</td>' % item
		elif isinstance(item, list):
			for ii in item:
				if isinstance(ii, float):
					res += '<td>%.2f</td>' % ii
				else:
					res += '<td>%s</td>' % str(ii)
		else:
			res += '<td>%s</td>' % str(item)
	res += '</tr>'
	return res


def find_file(pattern, doc_list):
	for doc in doc_list:
		if re.search(pattern, doc):
			return doc
	return ''


def compare_data():
	if gp.cur_log_dir[-1] != '/':
		gp.cur_log_dir += '/'
	if gp.ref_log_dir[-1] != '/':
		gp.ref_log_dir += '/'

	ref_list = os.listdir(gp.ref_log_dir)
	cur_list = os.listdir(gp.cur_log_dir)

	ref_folder = gp.ref_log_dir.split('/')[-2]
	cur_folder = gp.cur_log_dir.split('/')[-2]

	problem_zip_name = gp.cur_time + gp.folder_join + cur_folder.split(gp.folder_join)[1][0:7] \
					   + '_vs_' + ref_folder.split(gp.folder_join)[1][0:7]
	gp.problem_case_dir = gp.generate_dir_path(gp.data_dir, problem_zip_name)
	gp.create_dir(gp.problem_case_dir)
	if not os.path.isdir(gp.problem_dir):
		gp.create_dir(gp.problem_dir)

	header = '<h1>\nThis email is the overnight comparison results\n</h1>'
	header += '<h2>\n Current Commit:\n</h2>' + gp.read_commit_log(gp.cur_log_dir) + \
			  '<h3>Run on ' + gp.convert_date(cur_folder.split(gp.folder_join)[0]) + '</h3>'
	header += '<h2>\n Ref Commit:\n</h2>' + gp.read_commit_log(gp.ref_log_dir) + \
			  '<h3>Run on ' + gp.convert_date(ref_folder.split(gp.folder_join)[0]) + '</h3>'
	if gp.total_crash != 0:
		header += '<h2>\n<span style="color: red"> Total Crash: ' + str(gp.total_crash) + '</span>\n</h2>'
	else:
		header += '<h2>\n No Crash.\n</h2>'

	result = ''
	#brief-result
	brief_result = ''

	for scenario in gp.scenario:
		result += '<hr>\n'
		found_case = True
		ref_enc_file = find_file('Enc_File_' + scenario, ref_list)
		ref_dec_file = find_file('Dec_File_' + scenario, ref_list)
		if ref_enc_file != '' and ref_dec_file != '':
			ref_case_set = cc.CaseSummary(gp.ref_log_dir + ref_enc_file, gp.ref_log_dir + ref_dec_file)
		else:
			found_case = False

		cur_enc_file = find_file('Enc_File_' + scenario, cur_list)
		cur_dec_file = find_file('Dec_File_' + scenario, cur_list)
		if cur_enc_file != '' and cur_dec_file != '':
			cur_case_set = cc.CaseSummary(gp.cur_log_dir + cur_enc_file, gp.cur_log_dir + cur_dec_file)
		else:
			found_case = False

		if found_case:
			result += compare_encoder_performance(cur_case_set, ref_case_set, scenario)
			result += compare_decoder_performance(cur_case_set, ref_case_set, scenario)
			brief_result += compare_encoder_performance_brief(scenario)
			brief_result += compare_decoder_performance_brief(scenario)

	if gp.total_mismatch != 0:
		header += '<h2>\n<span style="color: red"> Total Mismatch: ' + str(gp.total_mismatch) + '</span>\n</h2>'
	else:
		header += '<h2>\n No Mismatch.\n</h2>'

	output = '<html>\n<head>\n' + header + result + '</head>\n</html>\n'
	brief_output = '<html>\n<head>\n' + header + brief_result + '</head>\n</html>\n'

	result_file = cur_folder.split(gp.folder_join)[1][:7] + '_vs_' + ref_folder.split(gp.folder_join)[1][:7] + '.html'
	result_file_handle = open(gp.problem_case_dir + result_file, 'w')
	result_file_handle.write(output)
	result_file_handle.close()

	brief_result_file = cur_folder.split(gp.folder_join)[1][:7] + '_vs_' + ref_folder.split(gp.folder_join)[1][:7] + '_brief.html'
	brief_result_file_handle = open(gp.problem_case_dir + brief_result_file, 'w')
	brief_result_file_handle.write(brief_output)
	brief_result_file_handle.close()

	gp.move_to_dir(gp.pic_dir, gp.problem_case_dir)
	gp.zip_to_folder(problem_zip_name + '.zip', gp.problem_case_dir, gp.problem_dir)
	gp.remove_dir(gp.problem_case_dir)

	return output


def compare_encoder_performance_brief(scenario):
	fail = 0
	header = '<h2>Encoder comparison result of ' + scenario + ' (prev / curr).</h2>\n'
	content = '<table border="1">\n'
	content += generate_header('t-p_ratio', 'unqualified_ratio', 'diff_br(%)',
				'real_fps', 'PSNR(dB)', 'SSIM(*100)', 'enc_time(us)')
	#type_list can be exported as a module in gp
	type_list = ['target_purposed_ratio', 'unqualified_ratio', 'bitrate_diff', 'real_fps', 'PSNR', 'SSIM', 'encoding_time']
	for i in range(len(type_list)):
		cur_type_inc = gp.enc_comparison_class.inc_[scenario][type_list[i]]
		cur_type_hold = gp.enc_comparison_class.hold_[scenario][type_list[i]]
		cur_type_dec = gp.enc_comparison_class.dec_[scenario][type_list[i]]
		#three values, direcly convert them into str
		(content, fail) = generate_cell(content, fail, str(cur_type_inc)+ '/' + str(cur_type_hold) + '/' + str(cur_type_dec))
	content += '</table>\n'
	return header + content


def compare_encoder_performance(cur_case_set, ref_case_set, scenario):
	error_case = 0
	header = '<h2>Encoder comparison result of ' + scenario + ' (prev / curr).</h2>\n'
	content = '<table border="1">\n'
	content += generate_header('case', 'configure', 't-p_ratio', 'unqualified_ratio', 'diff_br(%)',
							   'real_fps', 'PSNR(dB)', 'SSIM(*100)', 'enc_time(us)')

	for idx in range(0, cur_case_set.get_total_case_num()):
		cur_case = cur_case_set.case_set_[idx]
		ref_case = ref_case_set.find_case(cur_case.get_case())
		if ref_case != 0:
			return_val = compare_one_enc_case(cur_case, ref_case, scenario)
			if return_val != '':
				error_case += 1
				content += return_val
				copy_corresponding_log(cur_case.get_case(), scenario)
	content += '</table>\n'

	if error_case > 0:
		return header + content
	else:
		return header + '<p>All Cases are in normal range!!!</p>'


def copy_corresponding_log(case_name, scenario):
	case_dir = gp.generate_dir_path(gp.problem_case_dir, scenario, case_name)
	if os.path.exists(case_dir):
		return

	cur_case = find_corresponding_case_path(case_name, scenario, gp.cur_log_dir)
	dest_dir = gp.generate_dir_path(gp.problem_case_dir, scenario, case_name, 'cur')
	gp.create_dir(dest_dir)
	os.system('cp -rf ' + cur_case + '* ' + dest_dir)

	ref_case = find_corresponding_case_path(case_name, scenario, gp.ref_log_dir)
	dest_dir = gp.generate_dir_path(gp.problem_case_dir, scenario, case_name, 'ref')
	gp.create_dir(dest_dir)
	os.system('cp -rf ' + ref_case + '* ' + dest_dir)


def find_corresponding_case_path(case_name, scenario, search_dir):
	case_list = os.listdir(search_dir + scenario)
	for case in case_list:
		if case == case_name:
			return gp.generate_dir_path(search_dir, scenario, case)


def generate_cell(content, fail, cell_data, lower_range = None, higher_range = None, absolute_value = False):
	cell_lower_range = None
	cell_higher_range = None

	if lower_range is not None and higher_range is not None:
		if not absolute_value:
			cell_lower_range = cell_data[0] * lower_range
			cell_higher_range = cell_data[0] * higher_range
		else:
			cell_lower_range = lower_range
			cell_higher_range = higher_range

	(cnt, fl) = generate_one_cell(cell_data, cell_lower_range, cell_higher_range)
	content += cnt
	fail += fl
	return content, fail

def compare_one_enc_case(cur_case, ref_case, scenario):
	content = ''
	for idx in range(0, cur_case.get_client_number()):
		if idx == 0:
			cur_content = generate_cross_row_cell(cur_case.get_case(), cur_case.get_client_number())
			fail = 0
		else:
			cur_content = ''

		cur_content += generate_one_cell(cur_case.get_config(idx))[0]

		(cur_content, fail) = generate_cell(cur_content, fail,
											(ref_case.get_enc_data('target_purposed_ratio')[idx],
											 cur_case.get_enc_data('target_purposed_ratio')[idx]),
											0.7, 1.3, True)
		gp.enc_comparison_class.add_one_comparison(scenario, 'target_purposed_ratio', 
											ref_case.get_enc_data('target_purposed_ratio')[idx], 
											cur_case.get_enc_data('target_purposed_ratio')[idx])

		(cur_content, fail) = generate_cell(cur_content, fail,
											(ref_case.get_enc_data('unqualified_ratio')[idx],
											 cur_case.get_enc_data('unqualified_ratio')[idx]),
											0.0, 1.05, True)
		gp.enc_comparison_class.add_one_comparison(scenario, 'unqualified_ratio', 
											ref_case.get_enc_data('unqualified_ratio')[idx], 
											cur_case.get_enc_data('unqualified_ratio')[idx])

		(cur_content, fail) = generate_cell(cur_content, fail,
											(ref_case.get_enc_data('bitrate_diff')[idx],
											 cur_case.get_enc_data('bitrate_diff')[idx]),
											0.00, 10, True)
		gp.enc_comparison_class.add_one_comparison(scenario, 'bitrate_diff', 
											ref_case.get_enc_data('bitrate_diff')[idx], 
											cur_case.get_enc_data('bitrate_diff')[idx])

		(cur_content, fail) = generate_cell(cur_content, fail,
											(ref_case.get_enc_data('real_fps')[idx],
											 cur_case.get_enc_data('real_fps')[idx]),
											0.95, 1.05)
		gp.enc_comparison_class.add_one_comparison(scenario, 'real_fps', 
											ref_case.get_enc_data('real_fps')[idx], 
											cur_case.get_enc_data('real_fps')[idx])

		(cur_content, fail) = generate_cell(cur_content, fail,
											(ref_case.get_enc_data('PSNR')[idx],
											 cur_case.get_enc_data('PSNR')[idx]),
											0.95, 1.05)
		gp.enc_comparison_class.add_one_comparison(scenario, 'PSNR', 
											ref_case.get_enc_data('PSNR')[idx], 
											cur_case.get_enc_data('PSNR')[idx])

		(cur_content, fail) = generate_cell(cur_content, fail,
											(ref_case.get_enc_data('SSIM', 100)[idx],
											 cur_case.get_enc_data('SSIM', 100)[idx]))
		gp.enc_comparison_class.add_one_comparison(scenario, 'SSIM', 
											ref_case.get_enc_data('SSIM')[idx], 
											cur_case.get_enc_data('SSIM')[idx])

		(cur_content, fail) = generate_cell(cur_content, fail,
											(ref_case.get_enc_data('encoding_time')[idx],
											 cur_case.get_enc_data('encoding_time')[idx]))
		gp.enc_comparison_class.add_one_comparison(scenario, 'encoding_time', 
											ref_case.get_enc_data('encoding_time')[idx], 
											cur_case.get_enc_data('encoding_time')[idx])

		content += '<tr align="center">' + cur_content + '</tr>\n'
		
		if fail > 0:
			ref_client_ = ref_case.client_[idx]
			cur_client_ = cur_case.client_[idx]
			cur_pic_dir = gp.pic_dir + cur_client_.get_case() + '_Encoder/'
			if gp.exists_dir(cur_pic_dir) == 0:
				gp.create_dir(cur_pic_dir)
			gp.drawOneEncoderClient(cur_pic_dir, cur_client_.get_case()+'_'+cur_client_.get_config(),
															(cur_client_.raw_data_['target_bitrate'], ref_client_.raw_data_['target_bitrate']),
															(cur_client_.raw_data_['real_bitrate'], ref_client_.raw_data_['real_bitrate']),
															(cur_client_.raw_data_['real_fps'], ref_client_.raw_data_['real_fps']),
															(cur_client_.raw_data_['PSNR'], ref_client_.raw_data_['PSNR']),
															(cur_client_.raw_data_['SSIM'], ref_client_.raw_data_['SSIM']))
	if fail > 0:
		return content
	else:
		return ''


def compare_decoder_performance_brief(scenario):
	fail = 0
	header = '<h2>Decoder comparison result of ' + scenario + ' (prev / curr).</h2>\n'
	content = '<table border="1">\n'
	content += generate_header('real_fps', 'real_br(kbit/s)', 'PSNR(dB)', 'SSIM(*100)', 'is_decodable', 'VQMG')
	#type_list can be exported as a module in gp
	type_list = ['real_fps', 'real_bitrate', 'PSNR', 'SSIM', 'is_decodable', 'vqmg']
	for i in range(len(type_list)):
		cur_type_inc = gp.dec_comparison_class.inc_[scenario][type_list[i]]
		cur_type_hold = gp.dec_comparison_class.hold_[scenario][type_list[i]]
		cur_type_dec = gp.dec_comparison_class.dec_[scenario][type_list[i]]
		#three values, direcly convert them into str
		(content, fail) = generate_cell(content, fail, str(cur_type_inc)+ '/' + str(cur_type_hold) + '/' + str(cur_type_dec))
	content += '</table>\n'
	return header + content


def compare_decoder_performance(cur_case_set, ref_case_set, scenario):
	error_case = 0
	header = '<h2>Decoder comparison result of ' + scenario + ' (prev / curr).</h2>\n'
	content = '<table border="1">\n'
	content += generate_header('case', 'configure', 'real_fps', 'real_br(kbit/s)',
							   'PSNR(dB)', 'SSIM(*100)', 'is_decodable', 'VQMG')

	for idx in range(0, cur_case_set.get_total_case_num()):
		cur_case = cur_case_set.case_set_[idx]
		ref_case = ref_case_set.find_case(cur_case.get_case())
		if ref_case != 0:
			return_val = compare_one_dec_case(cur_case, ref_case, scenario)
			if return_val != '':
				error_case += 1
				content += return_val
				copy_corresponding_log(cur_case.get_case(), scenario)
	content += '</table>\n'

	if error_case > 0:
		return header + content
	else:
		return header + '<p>All Cases are in normal range!!!</p>'


def compare_one_dec_case(cur_case, ref_case, scenario):
	content = ''
	if cur_case.get_client_number() <= 1:
		return content
	
	for idx in range(0, cur_case.get_client_number()):

		if idx == 0:
			cur_content = generate_cross_row_cell(cur_case.get_case(), cur_case.get_client_number())
			fail = 0
		else:
			cur_content = ''

		cur_content += generate_one_cell(cur_case.get_config(idx))[0]

		
		(cur_content, fail) = generate_cell(cur_content, fail,
											(ref_case.get_dec_data('real_fps')[idx],
											 cur_case.get_dec_data('real_fps')[idx]),
											0.95, 1.05)
		gp.dec_comparison_class.add_one_comparison(scenario, 'real_fps', ref_case.get_dec_data('real_fps')[idx],
											 cur_case.get_dec_data('real_fps')[idx])

		# (cur_content, fail) = generate_cell(cur_content, fail,
		#                                     (ref_case.get_enc_data('target_bitrate')[idx],
		#                                      cur_case.get_enc_data('target_bitrate')[idx]),
		#                                     0.95, 1.05)

		(cur_content, fail) = generate_cell(cur_content, fail,
											(ref_case.get_dec_data('real_bitrate')[idx],
											 cur_case.get_dec_data('real_bitrate')[idx]),
											0.95, 1.05)
		gp.dec_comparison_class.add_one_comparison(scenario, 'real_bitrate', ref_case.get_dec_data('real_bitrate')[idx],
											 cur_case.get_dec_data('real_bitrate')[idx])

		(cur_content, fail) = generate_cell(cur_content, fail,
											(ref_case.get_dec_data('PSNR')[idx],
											 cur_case.get_dec_data('PSNR')[idx]),
											0.95, 1.05)
		gp.dec_comparison_class.add_one_comparison(scenario, 'PSNR', ref_case.get_dec_data('PSNR')[idx],
											 cur_case.get_dec_data('PSNR')[idx])

		(cur_content, fail) = generate_cell(cur_content, fail,
											(ref_case.get_dec_data('SSIM', 100)[idx],
											 cur_case.get_dec_data('SSIM', 100)[idx]),
											0.95, 1.05)
		gp.dec_comparison_class.add_one_comparison(scenario, 'SSIM', ref_case.get_dec_data('SSIM')[idx],
											 cur_case.get_dec_data('SSIM')[idx])

		mismatch = fail
		(cur_content, fail) = generate_cell(cur_content, fail,
											(ref_case.get_dec_data('is_decodable')[idx],
											 cur_case.get_dec_data('is_decodable')[idx]),
											0, 0)
		gp.dec_comparison_class.add_one_comparison(scenario, 'is_decodable', ref_case.get_dec_data('is_decodable')[idx],
											 cur_case.get_dec_data('is_decodable')[idx])
		
		if fail > 0:
			ref_client_ = ref_case.client_[idx]
			cur_client_ = cur_case.client_[idx]
			cur_pic_dir = gp.pic_dir + cur_client_.get_case() + '_Decoder/'
			if gp.exists_dir(cur_pic_dir) == 0:
				gp.create_dir(cur_pic_dir)
			if len(ref_client_.decoded_client_) != len(cur_client_.decoded_client_):
				continue
			for i in range(len(ref_client_.decoded_client_)):
				ref_dec = ref_client_.decoded_client_[i]
				cur_dec = cur_client_.decoded_client_[i]
				gp.drawOneDecoderClient(cur_pic_dir, cur_client_.get_case()+'_'+cur_client_.get_config(),
																str(cur_dec.uid_),
																(cur_dec.raw_data_['real_fps'], ref_dec.raw_data_['real_fps']),
																(cur_dec.raw_data_['real_bitrate'], ref_dec.raw_data_['real_bitrate']),
																(cur_dec.raw_data_['PSNR'], ref_dec.raw_data_['PSNR']),
																(cur_dec.raw_data_['SSIM'], ref_dec.raw_data_['SSIM']))

		if fail > mismatch:
			gp.total_mismatch += 1

		(cur_content, fail) = generate_cell(cur_content, fail,
											(ref_case.get_dec_data('vqmg')[idx],
											 cur_case.get_dec_data('vqmg')[idx]),
											0, 0)
		gp.dec_comparison_class.add_one_comparison(scenario, 'vqmg', ref_case.get_dec_data('vqmg')[idx],
											 cur_case.get_dec_data('vqmg')[idx])
		
		

		content += '<tr align="center">' + cur_content + '</tr>\n'

		

	if fail > 0:
		return content
	else:
		return ''


if __name__ == '__main__':
	gp.cur_log_dir = sys.argv[1]
	gp.ref_log_dir = sys.argv[2]
	compare_data()
