import subprocess
from tqdm import tqdm
import os
import shutil
def extract_frames_from_videos(directory, extension = '.m4v', h = 240, w = 240):
    for i in range(0,len(os.listdir(directory))):
        fname = os.listdir(directory)[i]
        if(os.path.isdir(os.path.join(directory, fname))):
            cwd = os.path.join(directory, fname)
            file = os.path.join(cwd, fname + extension)
            img_names = os.path.join(cwd, "c01_%04d.jpeg")
            subprocess.call(['ffmpeg', '-i', '{}'.format(file), '-vf' ,'scale={}:{}'.format(h,w), '{}'.format(img_names)]) 


def put_vids_into_dir(directory, extension = '.mp4'):
    fnames = os.listdir(directory)
    for i in fnames:
        os.makedirs(os.path.join(directory,i.split(".")[0]))                            #assuming the video filenames do not contain any dots
        shutil.move(os.path.join(directory,i),os.path.join(directory,i.split(".")[0]))

def main():
    import argparse
    parser = argparse.ArgumentParser(description="  python blah blah  ")
    parser.add_argument('--dir',
                            type=str,
                            help="""full path to directory where the video is stored""")

    parser.add_argument('--ext',
                            type=str,
                            help="""extension of your video files""")
    parser.add_argument('--h',
                            type=int,
                            help="""height of output frame""")

    parser.add_argument('--w',
                            type=int,
                            help="""width of output frame""")

    args=parser.parse_args()

    directory = args.dir
    extension = args.ext
    height = args.h
    width = args.w
    put_vids_into_dir(directory,extension)
    extract_frames_from_videos(directory,extension,h,w)


if __name__=="__main__":
    main()
