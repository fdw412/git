#!/bin/bash -x

for pid in `ps aux | grep chrom`; do sudo kill -9 $pid; done