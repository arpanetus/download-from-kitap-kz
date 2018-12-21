import requests
import re
import wget
import argparse
import sys
import os
from pathlib import Path

def get_link(read_link):
  print(" --- Starting to fetch the link --- ")
  r = requests.get(read_link)
  link = re.findall("data\-book\=\".+\.epub\"",r.text)[0].split('=')[1]
  print(" --- Link's been fetched --- ")
  return "https://kitap.kz"+link[1:len(link)-1]

def download_from_link(link):
  print(" --- Starting to download --- ")
  print("\n")
  downloaded_filename = wget.download(link)
  print("\n")
  return downloaded_filename

def get_default_filename(url):
  filename_raw = re.findall("s\/.+\/r",url)[0]
  return filename_raw[2:len(filename_raw)-2]+".epub"

def arguments(def_dir):
  parser = argparse.ArgumentParser()
  parser.add_argument("--filename", help="the name under which you'd like to save")
  parser.add_argument("--url", help="the url of book to download")
  parser.add_argument("--link", const=1, nargs='?', type=int, help="generate link of download")
  parser.add_argument("--dir", default=def_dir, help="directory of download")
  args = parser.parse_args()

  if not (args.url):
    print(" --- Please provide a link! ---")
    sys.exit(0)
  else:
    url = args.url
  filename = get_default_filename(url)
  link = args.link
  if args.filename:
    filename = args.filename + ".epub"
  return filename, url, link, args.dir

def rename_file(downloaded_filename,filename,def_dir):
  print(" --- Starting to rename downloaded file --- ")
  try:
      os.mkdir('{}'.format(def_dir))
  except Exception:
      pass
  for current_filename in os.listdir("."):
    if current_filename.startswith(downloaded_filename):
      os.rename(current_filename, '{}/{}'.format(def_dir, filename))
  print(" --- Renaming is done --- ")

def downloaded(filename, def_dir):
  return os.path.isfile('{}/{}'.format(def_dir, filename))

if __name__=="__main__":

  default_dir = str(Path.home()) + '/Documents/books'
  filename, url, getlink, def_dir = arguments(default_dir)
  def_dir = def_dir.replace("~", str(Path.home()))
  if not downloaded(filename, def_dir):
    if getlink:
      print("Your download link: {}".format(get_link(url)))
    else:
      downloaded_filename = download_from_link(get_link(url))
      rename_file(downloaded_filename, filename, def_dir)
      print(" --- File from: \n\t" + url + "\nhas been successfully downloaded! --- ")
      print(" --- It lies under the filename: \n\t"+filename+" --- ")
  else:
    print(" --- You have already downloaded this book --- ")
