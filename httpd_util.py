#!/usr/bin/env python

import re
import sys
import glob
import os

# supported commands:
#  ls-files
#  ls-virtual-hosts
#  


class HttpdConfFile(object):
    def __init__(self, httpd_dir, filename, parent='', lineno_in_parent=0):
        self.httpd_dir = httpd_dir
        self.filename = filename
        self.parent = parent
        self.lineno_in_parent = lineno_in_parent
        self.sub_files = self.find_sub_files()
    def find_sub_files(self):
        filename = os.path.join(self.httpd_dir, self.filename)
        p = re.compile('^\s*Include\s*(.*)$')
        g_files = []
        all_files = []
        with open(filename) as f:
            lineno = 0
            for line in f:
                lineno += 1
                if line.strip() == '' or line.strip()[0] == '#':
                    continue
                m = p.findall(line)
                if m:
                    g_files.extend(m)
        for gl in g_files:
            for fn in glob.glob(os.path.join(httpd_dir, '{0}'.format(gl))):
                if fn not in all_files:
                    all_files.append(fn)
        return all_files
    def conf_parse(self):
        fullname = os.path.join(httpd_dir, filename)
        p = re.compile(r'(<(?P<tag>[^>\s]*)\s*(.*?)>(.*?)</(?P=tag)>)', re.DOTALL)
        plain_text = ''.join([line for line in open(fullname) if line.strip() != '' and line.strip()[0] != '#'])



class HttpdConfParser(object):
    def __init__(self, httpd_dir, main_conf = 'conf/httpd.conf'):
        self.httpd_dir = httpd_dir
        self.main_conf = main_conf
        self.conf_files = self.find_confs(self.main_conf)

    
    def find_confs(self, filename, level=0, spacer=' ', indent_num=4, printable=False):
        conf_file = '{0}/{1}'.format(httpd_dir, filename)
        if printable:
            print('{0}{1}'.format(spacer * level * indent_num, conf_file))
        p = re.compile('^\s*Include\s*(.*)$')
        all_files = [conf_file,]
        g_files = []
        with open(conf_file) as f:
            for line in f:
                if line.strip() == '' or line.strip()[0] == '#':
                    continue
                m = p.findall(line)
                if m:
                    g_files.extend(m)
        for gl in g_files:
            for fn in glob.glob(os.path.join(httpd_dir, '{0}'.format(gl))):
                if fn not in all_files:
                    all_files.append(fn)
        new_files = all_files[1:]
        for fn in [fullname[len(httpd_dir) + 1:] for fullname in new_files]:
            for ff in find_confs(httpd_dir, fn, level=level+1, printable=printable):
                if ff not in all_files:
                    all_files.append(ff)
        return all_files

def find_confs(httpd_dir, filename, level=0, spacer=' ', indent_num=4, printable=False):
    conf_file = '{0}/{1}'.format(httpd_dir, filename)
    if printable:
        print('{0}{1}'.format(spacer * level * indent_num, conf_file))
    p = re.compile('^\s*Include\s*(.*)$')
    all_files = [conf_file,]
    g_files = []
    with open(conf_file) as f:
        for line in f:
            if line.strip() == '' or line.strip()[0] == '#':
                continue
            m = p.findall(line)
            if m:
                g_files.extend(m)
    for gl in g_files:
        for fn in glob.glob(os.path.join(httpd_dir, '{0}'.format(gl))):
            if fn not in all_files:
                all_files.append(fn)
    new_files = all_files[1:]
    for fn in [fullname[len(httpd_dir) + 1:] for fullname in new_files]:
        for ff in find_confs(httpd_dir, fn, level=level+1, printable=printable):
            if ff not in all_files:
                all_files.append(ff)
    return all_files

def conf_parse(httpd_dir):
    all_files = find_confs(httpd_dir, 'conf/httpd.conf', printable=True)
    # print all_files


def func_disp(httpd_dir, command):
    default_conf = 'conf/httpd.conf'
    if command == 'ls-files':
        find_confs(httpd_dir, default_conf, printable=True)

if __name__ == '__main__':
    command = sys.argv[1]
    httpd_dir = sys.argv[2]
    func_disp(httpd_dir, command)