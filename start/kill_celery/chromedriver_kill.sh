#!/bin/bash -x

for pid in `ps aux | grep chromedriver`; do sudo kill -9 $pid; done