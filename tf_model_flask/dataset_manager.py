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

        self.review_count = 0
        self.review_positive = 0
        self.review_negative = 0

        self.ds_count = 0;
        self.ds_positive = 0;
        self.ds_negative = 0;

        self.live_ds_path = live_path
        self.archive_ds_path = archive_path
        self.tmp_ds_path = tmp_path
        self.origin_ds_path = 'datasets/sentiment_dataset.csv'
        self.get_counts()

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

    def record_entry(self, record, predict):
        with open(self.live_ds_path, 'a+') as f:
            f.write(record)
        self.review_count += 1
        if predict:
            self.review_positive += 1
        else:
            self.review_negative += 1
        logging.info("Dataset Count: {}".format(self.review_count))
        if self.review_count >= 1000:
            return 1
        return 0

    def get_counts(self):
        self.get_review_count()
        self.get_dataset_count()
        self.get_archive_count()

    def get_review_count(self):
        self.review_count = 0
        self.review_positive = 0
        self.review_negative = 0
        try:
            with open(self.live_ds_path, 'r') as f:
                while True:
                    dat = f.readline()
                    tmp = dat.split(';')
                    if "1" in tmp[-1]:
                        self.review_positive += 1
                    else:
                        self.review_negative += 1
                    if not dat:
                        break
                    else:
                        self.review_count += 1
        except IOError:
            logging.info("Unable to locate live dataset.")

    def get_dataset_count(self):
        self.ds_count = 0
        self.ds_positive = 0
        self.ds_negative = 0
        try:
            with open(self.origin_ds_path, 'r') as f:
                while True:
                    dat = f.readline()
                    tmp = dat.split(';')
                    if "1" in tmp[-1]:
                        self.ds_positive += 1
                    else:
                        self.ds_negative += 1
                    if not dat:
                        break
                    else:
                        self.ds_count += 1
        except IOError:
            logging.info("Unable to locate origin dataset.")

    def get_archive_count(self):
        try:
            with open(self.archive_ds_path, 'r') as f:
                while True:
                    dat = f.readline()
                    tmp = dat.split(';')
                    if "1" in tmp[-1]:
                        self.ds_positive += 1
                        self.review_positive += 1
                    else:
                        self.ds_negative += 1
                        self.review_negative += 1
                    if not dat:
                        break
                    else:
                        self.ds_count += 1
                        self.review_count += 1
        except IOError:
            logging.info("Unable to locate archive dataset.")
        logging.info("Review Count: Total: {}, Pos: {}, Neg: {}".format(
                                                        self.review_count,
                                                        self.review_positive,
                                                        self.review_negative))
        logging.info("Dataset Count: Total: {}, Pos: {}, Neg: {}".format(
                                                        self.ds_count,
                                                        self.ds_positive,
                                                        self.ds_negative))
