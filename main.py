import os
import glob
import re
from reconfigure.parsers import NginxParser
#raw string
listen_patern = r'(?i)\blisten\s=\s443\b|\blisten\s=\sssl\b'
#nie zadziala z server_name ie.shop.brainbraining.com www.ie.shop.brainbraining.com;
www_pattern = r'\www(.*?)\.com' #tez nie moze byc bo zaczyna sie od com np server_name comfortingmindtraining.com www.comfortingmindtraining.com;
 #r'www\.[a-zA-Za-z1-9]*\.[a-zA-Za-z1-9]*'
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


                        if re.findall(listen_patern,str(i)):
                            #[print(i) for i in a.get_all('listen')]
                            #print(a.get('server_name'))
                            print(filename)
                            parser(str(a.get('server_name')))
                            #print(a.get('ssl_certificate'))
                            pass


def parser(string):
    if 'server_name ' in string:
        get_www = re.search(www_pattern, string)
        if get_www:
            x=string.replace(get_www[0],'')
            #print(x.replace('server_name = ',''))

            print(x)
        #print('??',string)
initial_check_for_ssl()



            # for line in f:
            #
            #     word = re.findall(pattern, line)
            #
            #     if word:
            #         word.append(filename.strip('conf.d\\')), data.append(word)



