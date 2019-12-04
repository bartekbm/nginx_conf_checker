import os
import glob
import re

pattern = r"listen.*\b (443|ssl)\b"
folder_path = 'conf.d'
what_file = '*.conf'
data = []


def initial_check_for_ssl():
    for filename in glob.glob(os.path.join(folder_path, what_file)):
        with open(filename, 'r') as f:

            for line in f:

                word = re.findall(pattern, line)

                if word:
                    word.append(filename.strip('conf.d\\')), data.append(word)


initial_check_for_ssl()
print(data)