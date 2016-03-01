#!/bin/bash
sudo tail /var/log/nginx/error.log -n 40
sudo tail /var/log/php5-fpm.log -n 5
