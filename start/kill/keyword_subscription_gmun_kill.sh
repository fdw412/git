#!/bin/bash -x

for pid in `ps aux | grep cycle_keyword_subscription`; do sudo kill $pid; done