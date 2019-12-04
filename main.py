import os
import glob
import re
from reconfigure.parsers import NginxParser
pattern = r"listen.*\b (443|ssl)\b"
folder_path = 'conf.d'
what_file = '*.conf'
data = []


def initial_check_for_ssl():
    for filename in glob.glob(os.path.join(folder_path, what_file)):
        with open(filename, 'r') as f:

            f = f.read()

            config = NginxParser()
            config = config.parse(content=f)
            test = config.get_all('server')

            for a in test:
                for i in a.get_all('listen'):
                    if str(i) == 'listen = 443 ssl':
                        print(a.get('listen'))
                        print(a.get('server_name'))
                        print(a.get('ssl_certificate'))





            # for line in f:
            #
            #     word = re.findall(pattern, line)
            #
            #     if word:
            #         word.append(filename.strip('conf.d\\')), data.append(word)


initial_check_for_ssl()
print(data)