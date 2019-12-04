from reconfigure.parsers import NginxParser
from reconfigure.parsers import JsonParser
#test=load(open('conf.d/77byte.com.conf'))

json_parser = JsonParser()

with open('conf.d/77byte.com.conf', 'r') as f:
    f = f.read()

    config = NginxParser()
    config = config.parse(content=f)
    test=config.get_all('server')

    for a in test:
        for i in a.get_all('listen'):
            if str(i) == 'listen = 443 ssl':
                print(a.get('server_name'))
                print(a.get('ssl_certificate'))



    # print(len(test))
    # #print(config.children[3])
    # #print(len(test))
    # for a in test[3]:
    #
    #     print(a)
