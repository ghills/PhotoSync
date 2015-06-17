__author__ = 'gavin'

import os
import exifread
import shutil
import logging

from datetime import datetime

pic_extensions = ('.jpg', '.png', '.gif', '.bmp', '')
video_extensions = ('.mov', '.mp4', '.avi')

input_file_path = os.path.normpath("e:\\dropbox\\ifttt\\gmail")
pic_dir_path = os.path.normpath("d:\\pictures")
video_path = os.path.normpath("d:\\our videos")

dt_exif_tag = 'EXIF DateTimeOriginal'

dry_run = False

def get_picture_date(fpath):
    # ex. format looks like '(0x9003) ASCII=2015:06:07 12:31:25 @ 592'
    timestamp = None
    with open(fpath) as f:
        tags = exifread.process_file(f, details=False, stop_tag=dt_exif_tag)
        try:
            timestamp = datetime.strptime(str(tags[dt_exif_tag]), '%Y:%m:%d %H:%M:%S')
        except KeyError:
            # no datetime metadata, return nothing
            logging.warning('No timestamp found for {}. tags: {}'.format(fpath, " ".join(tags.keys())))
    return timestamp.strftime('%Y-%m-%d')

def move_file(fpath, outdir):
    if not os.path.exists(outdir):
        try:
            logging.info('os.makedirs({})'.format(outdir))
            if not dry_run:
                os.makedirs(outdir)
        except:
            logging.exception('Error creating output directory {}'.format(outdir))

    try:
        logging.info('shutil.move({}, {})'.format(fpath, outdir))
        if not dry_run:
            shutil.move(fpath, outdir)
    except:
        logging.exception('Error moving {} to {}'.format(fpath, outdir))

def get_current_year_str():
    return str(datetime.now().year)

files_to_import = [s.lower() for s in os.listdir(input_file_path)]

#uncomment to write to file
logfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'activity.log')
logging.basicConfig(filename=logfile, level=logging.INFO, format='%(asctime)s %(message)s')
#uncomment for console output
#logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

logging.info('STARTING')

if dry_run:
    logging.info('this is a dry run, no effect should be had')

pics_to_import = ((s, os.path.join(input_file_path, s)) for s in files_to_import if os.path.splitext(s)[1] in pic_extensions)
videos_to_import = ((s, os.path.join(input_file_path, s)) for s in files_to_import if os.path.splitext(s)[1] in video_extensions)

for name, fpath in pics_to_import:
    date_str = get_picture_date(fpath)
    if date_str is not None:
        subdir = date_str
    else:
        subdir = os.path.join('unsorted', get_current_year_str())
    move_file(fpath, os.path.join(pic_dir_path, subdir))

for name, fpath in videos_to_import:
    move_file(fpath, os.path.join(video_path, "imported", get_current_year_str()))

logging.info('FINISHED')