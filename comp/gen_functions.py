def log_time(download_time, converting_time, method_name):

    file_dict = {'seq': 'performance_time.txt',
                 'conccurent': 'performance_time_conc.txt',
                 'async': 'performance_time_async.txt'}

    with open(file_dict.get(method_name), 'a') as perf_file:
        perf_file.write(f'Pictures downloaded within {download_time} secs. '
                        f'Converted within {converting_time} secs. -- METHOD -- {method_name}\n')
