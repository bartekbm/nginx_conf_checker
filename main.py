import os
import glob
import re
from reconfigure.parsers import NginxParser
#raw string
listen_patern = r'(?i)\blisten\s=\s443\b|\blisten\s=\sssl\b'
www_pattern = r'(:?www\.|\*\.)[\-a-zA-Z0-9\w.]*\.[a-z]*'
#ssl_certificate /etc/nginx/ssl/77byte.com/77byte.com_fullchain.cer;
#ssl_certificate_key /etc/nginx/ssl/77byte.com/77byte.com.key;
ssl_certificate = '/etc/nginx/ssl/{string}}/{string}_fullchain.cer'
ssl_certificate_key = '/etc/nginx/ssl/{string}/{string}.key'
folder_path = 'conf.d_tests'
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


                        if re.findall(listen_patern,str(i)):
                            #[print(i) for i in a.get_all('listen')]
                            #print(a.get('server_name'))
                            #print(filename)
                            parser(str(a.get('server_name')),str(a.get('ssl_certificate')),str(a.get('ssl_certificate_key')))
                            #print(a.get('ssl_certificate'))
                            pass


def parser(server_name,ssl_certificate,ssl_certificate_key):
    print(ssl_certificate +'\n'+ ssl_certificate_key)
    if 'server_name ' in server_name:
        get_www = re.search(www_pattern, server_name)
        #print('string przed replace', string)
        #print('pattern znalazl',get_www)
        if get_www:

            #print('replace get_www 0 na rempty',get_www[0])
            x=server_name.replace(get_www[0],'')
            x = x.replace('server_name =','')
            x = x.replace(" ", "")
            print(x)
        else:
            x=server_name.replace('server_name =','')
            x = x.replace(" ", "")
            print(x)
initial_check_for_ssl()



            # for line in f:
            #
            #     word = re.findall(pattern, line)
            #
            #     if word:
            #         word.append(filename.strip('conf.d\\')), data.append(word)



