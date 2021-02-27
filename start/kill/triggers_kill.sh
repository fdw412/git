#!/bin/bash -x

for pid in `ps aux | grep cycle_triggers`; do sudo kill $pid; done