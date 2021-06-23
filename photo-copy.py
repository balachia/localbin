#!/usr/bin/env python3

import argparse
import re
import datetime
import tempfile
import subprocess
from contextlib import closing
from pathlib import Path

# Dates and Dirs
# today
today_str = datetime.date.today().strftime('%Y-%m-%d')

# output base
outdir = Path.home() / 'Pictures' / 'working'
outraw = outdir / today_str / ('raw-' + today_str)
outvid = outdir / today_str / ('_video')
outjpg = outdir / today_str / ('_jpg')

# Workflows

def get_dcim(volume):
    dcim = volume / 'DCIM'
    if dcim.exists():
        return(dcim)
    else:
        return(None)

def get_msdcfs(dcim):
    msdcfs = [it for it in dcim.iterdir() if re.match(r'^\d{3}MSDCF$', it.name)]
    return(msdcfs)

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', dest='debug', action='store_true')
parser.add_argument('--novideo', dest='video', action='store_false')
parser.add_argument('--nophoto', dest='photo', action='store_false')
parser.add_argument('volume', nargs='?')

if __name__=="__main__":
    args = parser.parse_args()
    print(args)

    # check for volume existence
    if args.volume:
        volume_name = args.volume
    else:
        volume_name = 'NO NAME'
        if args.debug:
            print('Using default volume (%s)' % volume_name)
    volume_dir = Path('/Volumes') / volume_name

    if not volume_dir.exists():
        raise ValueError('Volume (%s) does not exist' % str(volume_dir))

    # pull raws + jpgs
    # find dcims/msdcfs
    if args.photo:
        dcim = get_dcim(volume_dir)
        if not dcim:
            print('No DCIM found, skipping ARW/JPG')
        else:
            msdcfs = get_msdcfs(dcim)
            # TODO: what if msdcfs don't exist

            for msdcf in msdcfs:
                arws = [it for it in msdcf.iterdir() if re.match(r'^\.ARW$', it.suffix)]
                arw_names = [it.stem for it in arws]

                # copy arws via tempfile
                if arws:
                    # create output directories
                    outraw.mkdir(parents=True, exist_ok=True)

                    print('Copying ARWs')
                    with closing(tempfile.NamedTemporaryFile('w')) as filelist:
                        print(*[it.name for it in arws], sep='\n', flush=True, file=filelist)
                        subprocess.check_call(['rsync', '-av', '--info=progress2', '--files-from', filelist.name, str(msdcf), str(outraw)])

                # find non-redundant jpgs
                jpgs = [it for it in msdcf.iterdir() if (re.match(r'^\.JPG$', it.suffix)) and (it.stem not in arw_names)]
                if jpgs:
                    # create output directories
                    outjpg.mkdir(parents=True, exist_ok=True)

                    print('Copying JPGs')
                    with closing(tempfile.NamedTemporaryFile('w')) as filelist:
                        print(*[it.name for it in jpgs], sep='\n', flush=True, file=filelist)
                        subprocess.check_call(['rsync', '-av', '--info=progress2', '--files-from', filelist.name, str(msdcf), str(outjpg)])

    # pull videos
    if args.video:
        videos = volume_dir / 'PRIVATE' / 'M4ROOT' / 'CLIP'
        if videos.exists:
            mp4s = [it for it in videos.iterdir() if re.match(r'^.MP4$', it.suffix)]
            if mp4s:
                # create output dir
                outvid.mkdir(parents=True, exist_ok=True)

                # rsync
                print('Copying MP4s')
                with closing(tempfile.NamedTemporaryFile('w')) as filelist:
                    print(*[it.name for it in mp4s], sep='\n', flush=True, file=filelist)
                    subprocess.check_call(['rsync', '-av', '--info=progress2', '--files-from', filelist.name, str(videos), str(outvid)])

# # find camera directories
# volume_dir = Path('/Volumes/NO NAME')
# dcim = volume_dir / 'DCIM'
# print('dcim exists ' + str(dcim.exists()))

# find MSCDF dirs
# msdcf_re = re.compile(r'^\d{3}MSDCF$')
# msdcfs = [it for it in dcim.iterdir() if msdcf_re.match(it.name)]

# ARW handling #############################################

# find raws (.ARW)
# msdcf = msdcfs[0]
# arws = [it for it in msdcf.iterdir() if re.match(r'^\.ARW$', it.suffix)]
# arw_names = [it.stem for it in arws]

# # copy arws via tempfile
# with closing(tempfile.NamedTemporaryFile('w')) as filelist:
#     print(*[it.name for it in arws], sep='\n', flush=True, file=filelist)
#     subprocess.check_call(['rsync', '-av', '--info=progress2', '--files-from', filelist.name, str(msdcf), str(outraw)])

# JPG handling #############################################

# find non-redundant jpgs
# jpgs = [it for it in msdcf.iterdir() if (re.match(r'^\.JPG$', it.suffix)) and (it.stem not in arw_names)]

