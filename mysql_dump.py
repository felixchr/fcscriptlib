#!/usr/bin/env python

import datetime
import sys
import os
import MySQLdb as mdb
import logging

def dump_table(cursor, table_name, line_count = 1000):
    cur = cursor
    lines = ['DROP TABLE IF EXISTS `{}`;'.format(table_name)]
    cur.execute('SHOW CREATE TABLE `{}`;'.format(table_name))
    lines.append(str(cur.fetchone()[1]) + ';')
    i = 0
    lc = line_count
    sql_s = 'SELECT * FROM `{}` LIMIT {},{}'
    while True:
        sql = sql_s.format(table_name, lc * i, lc)
        rn = cur.execute(sql)
        if rn == 0:
            break
        rows = ['INSERT INTO `{}` VALUES'.format(table_name),]
        for row in cur.fetchall():
            cols = []
            for field in row:
                if field == None:
                    cols.append('NULL')
                elif isinstance(field, str):
                    cols.append("'{}'".format(field.replace("'", "''")))
                elif isinstance(field, (int, long)):
                    cols.append('{}'.format(field))
                elif isinstance(field, datetime.datetime):
                    cols.append("'{}'".format(field.strftime('%Y-%m-%d %H:%M:%S')))
                elif isinstance(field, datetime.date):
                    cols.append("'{}'".format(field.strftime('%Y-%m-%d')))
                else:
                    print type(field)
            data = ','.join(cols)
            rows.append('    ({}),'.format(data))
        #     data = ','.join(['"{}"'.format(v) if v else 'NULL' for v in row])
        rows[-1] = rows[-1][:-1] + ';'
    #     lines.append(data)
        lines.append('\n'.join(rows))
        i += 1
    return '\n\n'.join(lines)

def dump_db(db_args, tables, out_dir):
    '''db_args: {'host': host, 'user': user, 'passwd': passwd, 'db': db_name, 'port': port}
    tables: table list
    '''
    conn = mdb.connect(**db_args)
    cursor = conn.cursor()
    output = os.path.join(out_dir, '{host}_{port}_{db}.sql'.format(**db_args))
    open(output, 'w').write('')
    for table in tables:
        open(output, 'a').write(dump_table(cursor, table, 1000))
    conn.close()