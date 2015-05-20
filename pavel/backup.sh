#!/bin/bash

backup_date=$(date "+%d.%m.%Y_%H_%M_%S.tar.gz")

tar -cpzf /root/backup/stat_${backup_date}.tar.gz /root/stat
