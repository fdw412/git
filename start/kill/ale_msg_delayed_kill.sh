#!/bin/bash -x

for pid in `ps aux | grep cycle_ale_msg_delayed`; do sudo kill -9 $pid; done