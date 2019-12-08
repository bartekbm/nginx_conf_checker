import os
import glob
import re
from reconfigure.parsers import NginxParser
# raw string
listen_patern = r'(?i)\blisten\s=\s443\b|\blisten\s=\sssl\b'
www_pattern = r'(:?www\.|\*\.)[\-a-zA-Z0-9\w.]*\.[a-z]*'

folder_path = 'conf.d'
what_file = '*.conf'
data = []


def initial_check_for_ssl():
    for filename in glob.glob(os.path.join(folder_path, what_file)):
        with open(filename, 'r') as f:

            f = f.read()

            config = NginxParser()
            try:
                config = config.parse(content=f)
            except Exception as e:
                s = str(e)
                print(s)
                pass
            else:
                test = config.get_all('server')

            for a in test:
                    for i in a.get_all('listen'):
                        if re.findall(listen_patern, str(i)):

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
            if f'/etc/nginx/ssl/{server_name}/{server_name}_fullchain.cer' == ssl_certificate and\
                    f'/etc/nginx/ssl/{server_name}/{server_name}.key' == ssl_certificate_key:
                pass
            else:
                print('nie ma',filename, server_name, ssl_certificate, ssl_certificate_key)
        else:
            server_name = server_name.replace('server_name =', '')
            server_name = server_name.replace(" ", "")
            if f'/etc/nginx/ssl/{server_name}/{server_name}_fullchain.cer' == ssl_certificate and\
                    f'/etc/nginx/ssl/{server_name}/{server_name}.key' == ssl_certificate_key:
                pass
            else:
                print('nie ma', filename, server_name, ssl_certificate, ssl_certificate_key)


initial_check_for_ssl()





