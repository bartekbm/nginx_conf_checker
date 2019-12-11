import os
import glob
import re
from reconfigure.parsers import NginxParser
import inspect
import json


def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno


# raw string
listen_patern = r'(?i)\blisten\s=\s443\b|\blisten\s=\sssl\b'
www_pattern = r'(:?www\.|\*\.)[\-a-zA-Z0-9\w.]*\.[a-z]*'

folder_path = 'conf.d'
what_file = '*.conf'
count_no_cert_define = 0
count_all_files = 0
files = []
final_list = []
parse_error = []
no_cert_define = []
#{file:name,server_name:server_name,ssl}


def initial_check_for_ssl():
    global count_no_cert_define
    global count_all_files
    for filename in glob.glob(os.path.join(folder_path, what_file)):
        count_all_files += 1
        with open(filename, 'r') as f:

            f = f.read()
            filename = filename.strip('conf.d\\')
            config = NginxParser()
            try:
                config = config.parse(content=f)
            except Exception as e:
                error_message = str(e)
                parse_error.append({'error_parsing':filename,'error_message':error_message})
                pass
            else:
                test = config.get_all('server')

            for a in test:
                for i in a.get_all('listen'):
                    if re.findall(listen_patern, str(i)):
                        if str(a.get('ssl_certificate')) == 'None' or str(a.get('ssl_certificate_key')) == 'None':
                            count_no_cert_define += 1
                            no_cert_define.append({'no_cert_define_for':filename})

                        parser(str(a.get('server_name')), str(a.get('ssl_certificate')),
                               str(a.get('ssl_certificate_key')), filename)


def parser(server_name, ssl_certificate, ssl_certificate_key, filename):

    ssl_certificate = ssl_certificate.replace('ssl_certificate = ', '')
    ssl_certificate_key = ssl_certificate_key.replace('ssl_certificate_key = ', '')
    if 'server_name ' in server_name:
        get_www = re.search(www_pattern, server_name)
        if get_www:

            server_name = server_name.replace(get_www[0], '')
            server_name = server_name.replace('server_name =', '')
            server_name = server_name.replace(" ", "")

            if f'/etc/nginx/ssl/{server_name}/{server_name}_fullchain.cer' == ssl_certificate and \
                    f'/etc/nginx/ssl/{server_name}/{server_name}.key' == ssl_certificate_key:
                pass

            else:
                if ssl_certificate == 'None' or ssl_certificate_key == 'None':
                    pass
                else:
                    final_list.append({'file_name':filename,'domain_name':server_name,
                                       'wrong_ssl_certificate_path':ssl_certificate,
                                       'corect_ssl_certificate_path':f'/etc/nginx/ssl/{server_name}/{server_name}',
                                       'wrong_ssl_key_path':ssl_certificate_key,'correct_ssl_key_path':
                                       f'/etc/nginx/ssl/{server_name}/{server_name}.key'})
                pass
        else:
            server_name = server_name.replace('server_name =', '')
            server_name = server_name.replace(" ", "")
            if f'/etc/nginx/ssl/{server_name}/{server_name}_fullchain.cer' == ssl_certificate and \
                    f'/etc/nginx/ssl/{server_name}/{server_name}.key' == ssl_certificate_key:
                pass
            else:
                if ssl_certificate == 'None' or ssl_certificate_key == 'None':
                    pass
                else:
                    final_list.append({'file_name': filename, 'domain_name': server_name,
                                       'wrong_ssl_certificate_path': ssl_certificate,
                                       'corect_ssl_certificate_path': f'/etc/nginx/ssl/{server_name}/{server_name}',
                                       'wrong_ssl_key_path': ssl_certificate_key, 'correct_ssl_key_path':
                                           f'/etc/nginx/ssl/{server_name}/{server_name}.key'})

                pass


initial_check_for_ssl()

final_list.append(no_cert_define)
final_list.append(parse_error)
with open('test.txt', 'w') as json_file:
  json.dump(final_list, json_file, indent=2)