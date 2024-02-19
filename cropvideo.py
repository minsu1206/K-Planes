import numpy as np
import cv2
import argparse
import os


def crop_video(logdir, output_paths):

    src_video = f"{logdir}/step90000.mp4"

    cap = cv2.VideoCapture(src_video)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fps = cap.get(cv2.CAP_PROP_FPS)

    cropped_height = height // 3

    writers = [cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, cropped_height)) for output_path in output_paths]

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        crop1 = frame[:cropped_height, :, :]
        crop2 = frame[cropped_height:2*cropped_height, :, :]
        crop3 = frame[2*cropped_height:3*cropped_height, :, :]

        for writer, cropped_frame in zip(writers, [crop1, crop2, crop3]):
            writer.write(cropped_frame)
    
    cap.release()
    for writer in writers:
        writer.release()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="")

    parser.add_argument("--logdir", type=str, required=True)
    parser.add_argument("--nstep", type=int, default=90000)
    args = parser.parse_args()

    logdir = args.logdir

    os.makedirs(f"{logdir}/cropped", exist_ok=True)

    output_paths = [f"{logdir}/cropped/step{args.nstep}-predrgb.mp4", f"{logdir}/cropped/step{args.nstep}-gtrgb.mp4", f"{logdir}/cropped/step{args.nstep}-errrgb.mp4"]
    crop_video(logdir, output_paths)


