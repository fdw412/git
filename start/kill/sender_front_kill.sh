#!/bin/bash -x

for pid in `ps aux | grep cycle_sender_front`; do sudo kill $pid; done