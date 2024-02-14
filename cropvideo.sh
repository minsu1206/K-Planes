#!/bin/bash
# ex) bash cropvideo.sh logs/baseline/cut_roasted_beef
logdir=$1
mkdir -p $logdir/cropped
ffmpeg -i $logdir/step90000.mp4 -filter:v "crop=iw:ih/3:0:0" $logdir/cropped/step90000-pred.mp4 -filter:v "crop=iw:ih/3:0:ih/3" $logdir/cropped/step90000-gt.mp4 -filter:v "crop=iw:ih/3:0:2*ih/3" $logdir/cropped/step90000-rgberror.mp4
ffmpeg -i $logdir/step90000-depth.mp4 -filter:v "crop=iw:ih/3:0:0" $logdir/cropped/step90000-depth-pred.mp4 -filter:v "crop=iw:ih/3:0:ih/3" $logdir/cropped/step90000-depth-gt.mp4 -filter:v "crop=iw:ih/3:0:2*ih/3" $logdir/cropped/step90000-deptherror.mp4

