#!/bin/bash -x

for pid in `ps aux | grep cycle_non_alert`; do sudo kill -9 $pid; done