#!/usr/bin/env python

from pexpect import pxssh

def push(ip, un, pw):
    def push_key(s, key):
        s.sendline('mkdir -p ~/.ssh')
        s.prompt(1)
        s.sendline('cat >> ~/.ssh/authorized_keys << EOF')
        s.sendline(key)
        s.sendline('EOF')
        s.prompt(1)
        s.sendline('chmod 700 ~/.ssh')
        s.prompt(1)
        s.sendline('chmod 644 ~/.ssh/authorized_keys')
        s.prompt(1)
    s = pxssh.pxssh()
    s.login(ip, un, pw)
    s.prompt(1)
    my_key = ''
    s.sendline('[ -d ~/.ssh ] || mkdir ~/.ssh')
    my_key = 'ssh-rsa AAAAB3NzaC1yc.....ypxPdrwIw== myusername@ruby'
    appadm_key = 'ssh-rsa AAAAB3NzaC1yc....kl9BalMvlWxw== appadm@diamond'
    prompt = '\\[\\w+@.* ~\\]\\$ '
    s.PROMPT = prompt
    push_key(s, my_key)
    s.sendline('sudo su - appadm')
    push_key(s, appadm_key)
    s.close()

un, pw = 'myusername', 'mypasword'
hosts = ('10.10.10.111', '10.10.10.112', '10.10.10.113',)
for host in hosts:
    print 'Push to {}'.format(host)
    push(host, un, pw)
