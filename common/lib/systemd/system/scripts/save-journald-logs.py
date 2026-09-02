#!/usr/bin/env python3
# @@@LICENSE
#
# Copyright (c) 2019 LG Electronics, Inc.
#
# Confidential computer software. Valid license from LG required for
# possession, use or copying. Consistent with FAR 12.211 and 12.212,
# Commercial Computer Software, Computer Software Documentation, and
# Technical Data for Commercial Items are licensed to the U.S. Government
# under vendor's standard commercial license.
#
# LICENSE@@@

import os
import glob
import tarfile
import time

from subprocess import call, PIPE, Popen

def get_timestamp():
    t = time.localtime()
    return str(t.tm_year).zfill(4) + "-" + str(t.tm_mon).zfill(2) + "-" + str(t.tm_mday).zfill(2) + "-" + str(
        t.tm_hour).zfill(2) + "-" + str(t.tm_min).zfill(2) + "-" + str(t.tm_sec).zfill(2)

def remove_journald_old_files():
    filelist = glob.glob("/var/log/journald*")
    for f in filelist:
        os.remove(f)

def flush_journald_log_to_file():
    # -b limits the dump to the boot that is ending. Without it this walks
    # every boot journald still has on disk, which on a device with a
    # persistent journal is the whole 1+ GB of it: 36 seconds to produce and
    # ~180 MB written to flash, on every single shutdown. The older boots are
    # still in /var/log/journal for journalctl -b -1 and friends to read, so
    # nothing is lost by leaving them out of this text copy.
    journalctl_options = ['-a', '-b']
    command = ['journalctl'] + journalctl_options
    log_file_name = "/var/log/journald-" + get_timestamp() + ".log"
    with open(log_file_name, "w") as logFile:
        call(command, stdout=logFile)
    return

def exclude_journal(tarinfo):
    # /var/log/journal is journald's own binary database, and it is persistent
    # here: gzipping it into the backup means compressing a copy of every boot
    # ever recorded, alongside the text dump that was just made of the last
    # one. The text dump is what this backup is for.
    if tarinfo.name == 'log/journal' or tarinfo.name.startswith('log/journal/'):
        return None
    return tarinfo

def backup_var_log():
    rdxdDir = "/var/spool/rdxd/"
    if not os.path.isdir(rdxdDir):
        os.mkdir(rdxdDir)
    saveFile = '/var/spool/rdxd/previous_boot_logs.tar.gz'
    if os.path.isfile(saveFile):
        os.remove(saveFile)

    source = '/var/log/'
    with tarfile.open(saveFile, "w:gz") as tar:
        tar.add(source, arcname='log', filter=exclude_journal)
    return

if __name__ == '__main__':
    remove_journald_old_files()
    flush_journald_log_to_file()
    backup_var_log()

    exit(0)
