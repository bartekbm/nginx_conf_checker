import os
import glob
import re
from reconfigure.parsers import NginxParser
#raw string
pattern = r"\blisten\s443\sssl\b|\blisten\s443\b|\blisten\sssl\b|\blisten\sssl\s443\b"
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
                        x = re.search(pattern,str(i))
                        print('PATTERN',x)
                        if str(i) == 'listen = 443 ssl':
                            [print(i) for i in a.get_all('listen')]
                            print(a.get('server_name'))
                            print(a.get('ssl_certificate'))


initial_check_for_ssl()
print(data)



            # for line in f:
            #
            #     word = re.findall(pattern, line)
            #
            #     if word:
            #         word.append(filename.strip('conf.d\\')), data.append(word)



