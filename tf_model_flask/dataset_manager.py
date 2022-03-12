#!/usr/bin/env python3

import os, logging
from os.path import exists

class DS_Manager:
    def __init__(self, live_path, archive_path, tmp_path):
        logging.basicConfig(
            format='%(asctime)s-TF_Model_Server{%(levelname)s}: %(message)s',
            level=logging.INFO,
            datefmt='%H:%M:%S')
        self.live_lock = False
        self.ds_count = 0
        self.live_ds_path = live_path
        self.archive_ds_path = archive_path
        self.tmp_ds_path = tmp_path
        self.get_ds_count()

    def transfer_to_tmp(self):
        line_count = 0
        while self.live_lock:
            pass
        self.live_lock = True
        src = open(self.live_ds_path, 'r')
        dest = open(self.tmp_ds_path, 'w+')
        for line in src:
            dest.write(line)
            line_count += 1
            if line_count == 1000:
                src.close()
                dest.close()
                self.live_lock = False
                break

    # ARCHIVE DATA IN LIVE DS AND CLEAR TMP DS
    def archive_live_ds(self):
        while self.live_lock:
            pass
        self.live_lock = True
        # LOAD LIVE DS TO MEMORY
        ds_mem = []
        src = open(self.live_ds_path, 'r+')
        dest = open(self.archive_ds_path, 'a+')
        ds_mem = src.readlines()
        src.truncate()
        src.seek(0)
        # WRITE TO ARCHIVE
        for i in range(1000):
            dest.write(ds_mem[i])
        # WRITE OVERFLOW BACK TO LIVE DS
        for i in range(1000, len(ds_mem)):
            src.write(ds_mem[i])
        src.close()
        des.close()
        self.live_lock = False
        # EMPTY TMP DATASET FILE
        with open(self.tmp_ds_path, 'r+') as tmp:
            tmp.truncate()

    def record_entry(self, record):
        with open(self.live_ds_path, 'a+') as f:
            f.write(record)
        self.ds_count += 1
        logging.info("Dataset Count: {}".format(self.ds_count))
        if ds_count >= 1000:
            return 1
        return 0

    def count_generator(self, reader):
        b = reader(1024 * 1024)
        while b:
            yield b
            b = reader(1024 * 1024)

    def get_ds_count(self):
        if exists(self.live_ds_path):
            with open(self.live_ds_path, 'rb') as f:
                cnt_gen = self.count_generator(f.raw.read)
                count = sum(buffer.count(b'\n') for buffer in cnt_gen)
                self.ds_count = count
        else:
            self.ds_count = 0
        logging.info("Dataset Count: {}".format(self.ds_count))
