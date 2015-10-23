__author__ = 'gavin'

import os
import exifread
import logging
import filecmp
import uuid

from datetime import datetime

from fs_actions import FSActionContext

pic_extensions = ('.jpg', '.png', '.gif', '.bmp', '.jpeg', '')
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

    if timestamp is not None:
        return timestamp.strftime('%Y-%m-%d')
    else:
        # default to todays date if no exif data exists
        return datetime.now().strftime('%Y-%m-%d')

def mangle_filename(filename):
    base, ext = os.path.splitext(filename)
    return( str(uuid.uuid4()) + ext )

def create_destination_folder(path):
    try:
        fs.makedirs(path)
    except:
        logging.exception('Error creating output directory {}'.format(path))

def move_file(fpath, outdir):
    if not os.path.exists(outdir):
        create_destination_folder(outdir)

    filename = os.path.split(fpath)[1]
    outpath = os.path.join(outdir, filename)

    # assume we are going to move the file
    # unless set otherwise
    do_move = True

    # deal with existing file in that folder with the same name
    # if contents are the same, delete the import one as we already have it
    # if contents differ, rename the incoming file with a uuid and dump it in
    if os.path.exists(outpath):
        logging.info('{} already exists'.format(os.path.join(outdir, filename)))
        # check if the file is the same first
        if filecmp.cmp(fpath, os.path.join(outdir, filename)):
            logging.info('existing file equivalent.')
            do_move = False
            fs.remove(fpath)
        else:
            # same filename, different contents. Rename destination
            outpath = os.path.join(outdir, mangle_filename(filename))

    # the only reason we wouldn't want to move the file is if we already
    # deleted the imported one because the file is identical to what we already have
    if do_move:
        try:
            fs.move(fpath, outpath)
        except:
            logging.exception('Error moving {} to {}'.format(fpath, outpath))

def get_current_year_str():
    return str(datetime.now().year)

def get_photo_subdir(fpath):
    date_str = get_picture_date(fpath)
    if date_str is not None:
        subdir = date_str
    else:
        subdir = os.path.join('unsorted', get_current_year_str())
    return subdir

files_to_import = [s.lower() for s in os.listdir(input_file_path)]

#uncomment to write to file
logfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'activity.log')
logging.basicConfig(filename=logfile, level=logging.INFO, format='%(asctime)s %(message)s')
#uncomment for console output
#logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

logging.info('STARTING')

fs = FSActionContext(dry_run=dry_run)
if dry_run:
    logging.info('this is a dry run, no effect should be had')

pics_to_import = ((s, os.path.join(input_file_path, s)) for s in files_to_import if os.path.splitext(s)[1] in pic_extensions)
videos_to_import = ((s, os.path.join(input_file_path, s)) for s in files_to_import if os.path.splitext(s)[1] in video_extensions)

for name, fpath in pics_to_import:
    move_file(fpath, os.path.join(pic_dir_path, get_photo_subdir(fpath)))

for name, fpath in videos_to_import:
    move_file(fpath, os.path.join(video_path, "imported", get_current_year_str()))

logging.info('FINISHED')
