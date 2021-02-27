#!/bin/bash -x

for pid in `ps aux | grep cycle_keyword_subscription_subsman`; do sudo kill -9 $pid; done