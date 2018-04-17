#!/usr/bin/env python3
#!/usr/bin/env python3

#  Copyright (C) 2018 Jussi Pakkanen.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of version 3, or (at your option) any later version,
# of the GNU General Public License as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sqlite3
import sys, os, pathlib
import shutil

def wipe_cookies(cookiefile, permitted_suffixes):
    conn = sqlite3.connect(cookiefile)
    cur = conn.cursor()
    hosts_to_delete = []
    for entry in cur.execute('SELECT DISTINCT(host) FROM moz_cookies ORDER BY host;'):
        curhost = entry[0]
        should_delete = True
        for ps in permitted_suffixes:
            if curhost.endswith(ps):
                should_delete = False
                break
        if should_delete:
            hosts_to_delete.append(curhost)
        else:
            print('Preserving cookies from %s.' % entry)
    conn.commit()
    shutil.copyfile(cookiefile, cookiefile + '~')
    for hd in hosts_to_delete:
        cur.execute('DELETE FROM moz_cookies WHERE host=?;', (hd, ))
    conn.commit()
    cur.execute('VACUUM;')
    conn.commit()

if __name__ == '__main__':
    prospective_cookiefiles = list(pathlib.Path.home().glob('.mozilla/**/cookies.sqlite'))
    if len(prospective_cookiefiles) == 0:
        prospective_cookiefiles = list(pathlib.Path.home().glob('Library/Application Support/Firefox/**/cookies.sqlite'))
    if len(prospective_cookiefiles) != 1:
        print('Did not find exactly one cookie file. Not doing anything to avoid breakage.\n')
        print(' '.join([str(x) for x in prospective_cookiefiles]))
        sys.exit(1)
    #cookiefile = 'cookies.sqlite'
    cookiefile =  str(prospective_cookiefiles[0])
    print('Using cookie file %s.\n' % cookiefile)
    pres_file = 'preserved_host_suffixes.txt'
    if not os.path.exists(pres_file):
        sys.exit('preserved_host_suffixes.txt file not found.')
    permitted_suffixes = []
    for line in open(pres_file):
        line = line.strip()
        if line:
            permitted_suffixes.append(line)
    wipe_cookies(cookiefile, permitted_suffixes)
