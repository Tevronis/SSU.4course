import json
import os
import re
import socket
import pyping
from email.parser import Parser

json_crit = json.load(open('crit.json'))

p = Parser()

dir = os.getcwd() + '\Spam mishaenz'


def ping(hostname):
    # print hostname
    try:
        r = pyping.ping(hostname)
    except:
        return False
    return True if r.ret_code == 0 else False


def isEmail(email, s, json_crit):
    result = 0
    pat = r'[a-zA-Z0-9<>.]*@[a-zA-Z0-9<>.]*.[a-zA-Z0-9<>.]*'
    r = re.compile(pat)
    if r.search(email) is None:
        result += json_crit[s]
        print s
    return result


def getDomain(raw):
    # fromat: (domain [ip])
    # or ([ip])
    r = re.compile(r'\[([0-9.:a-z]+)\]')
    s = r.search(raw)
    try:
        result = socket.gethostbyaddr(s.group(1))
    except:
        return False, None
    return s.group(1) == '127.0.0.1', result


def checkChain(chain):
    def check(chain):
        result = 0
        ch = chain[::-1]
        for i in range(len(ch)):
            if i + 1 >= len(ch) or ch[i][1] == ch[i + 1][0]:
                continue
            else:
                result += json_crit['breakChain']
                print 'breakChain'
        return result

    def checkDomain(g):
        localhost, domain = getDomain(g.group(2))
        if not (domain is None) and not g.group(1) in domain and not localhost:
            print 'notEqualDomain'
            return int(json_crit['notEqualDomain'])
        return 0

    def checkByFormat(chainRaw):
        if i != len(chain) - 1:
            print 'badFormatReceived'
            return int(json_crit['badFormatReceived'])
        else:
            gBy = rBy.search(text)
            if not (gBy is None):
                chainRaw.append([None, gBy.group(1)])
        return 0

    def checkMain(chainRow):
        chainRaw.append([g.group(1), g.group(3)])
        if g.group(2) == '(IP may be forged by CGI script)':
            print 'ipMayBeForged'
            return int(json_crit['ipMayBeForged'])
        else:
            return checkDomain(g)

    result = 0
    pat = r'from ([a-zA-Z0-9.@-]+) (\(.*\)) by ([a-zA-Z0-9.@-]+)'
    patCheckBy = r'by ([a-zA-Z0-9.@]+) with'
    r = re.compile(pat)
    rBy = re.compile(patCheckBy)
    chainRaw = []
    for i, item in enumerate(chain):

        text = item.replace('\n', '').replace('\t', ' ')
        g = r.search(text)
        if g is None:
            result += checkByFormat(chainRaw)
        else:
            result += checkMain(chainRaw)
    result += check(chainRaw)
    return result


def getGoodEmail(data):
    pat = r'<(.*)>'
    r = re.compile(pat)
    e = r.search(data)
    return data if e is None else e.group(1)


def main():
    for name in os.listdir(dir):
        print name
        result = 0

        path = os.path.join(dir, name)
        mail = open(path)
        e = p.parse(mail)

        receivedChain = []
        withoutReceived = True
        for header, data in e._headers:
            # print header
            header = header.lower()
            if header == 'return-path':
                if getGoodEmail(e['Return-path']) != getGoodEmail(e['From']):
                    result += json_crit['Return-pathAndFrom']
                    print 'Return-pathAndFrom'
                w = getGoodEmail(e['Return-path'])
                if w != '' and not ping(getGoodEmail(e['Return-path']).split('@')[-1]):
                    result += json_crit['Return-path']
                    print 'ping'
            if header == 'bcc':
                if not (getGoodEmail(data) in json_crit['my_email']):
                    result += json_crit['Bcc']
                    print 'Bcc'
            if header == 'to':
                if not (getGoodEmail(data) in json_crit['my_email']):
                    result += json_crit['To']
                    print 'To'
            if header == 'cc':
                if not (getGoodEmail(data) in json_crit['my_email']):
                    result += json_crit['Cc']
                    print 'Cc'
            if header == 'x-distribution' and data == 'bulk':
                result += json_crit['X-Distribution']
                print 'X-Distribution'
            if header == 'x-uidl':
                result += json_crit['X-UIDL']
                print 'X-UIDL'

            if header == 'message-id':
                result += isEmail(data, 'Message-id', json_crit)

            if header == 'in-reply-to':
                result += isEmail(data, 'In-Reply-To', json_crit)
                arr = e['References']
                if not data in e['References']:
                    result += json_crit['References']
                    print 'References'
            if header == 'x-spam-status' and data.lower() == 'yes':
                result += json_crit['X-Spam-Status']
                print 'X-Spam-Status'
            if header == 'received':
                withoutReceived = False
                receivedChain.append(data)
            if header == 'x-yandex-spam' and data != '1':
                result += json_crit['X-Yandex-Spam'] * int(data)
                print 'X-Yandex-Spam'
            if header == 'x-mras':
                result += json_crit['X-Mras']
                print 'X-Mras'

        result += checkChain(receivedChain)
        if withoutReceived:
            result += json_crit['WithoutReceived']
            print 'WithoutReceived'

        print result
        print


main()
