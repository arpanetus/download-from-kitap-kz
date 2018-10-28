import requests
import re
import wget
import argparse
import sys
import os

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

def arguments():
  parser = argparse.ArgumentParser()
  parser.add_argument("--filename", help="the name under which you'd like to save")
  parser.add_argument("--url", help="the url of book to download")
  args = parser.parse_args()

  if not (args.url):
    print(" --- Please provide a link! ---") 
    sys.exit(0) 
  else:
    url = args.url
  filename = get_default_filename(url)
  if args.filename:
    filename = args.filename + ".epub"
  return filename, url

def rename_file(downloaded_filename,filename):
  print(" --- Starting to rename downloaded file --- ")
  for current_filename in os.listdir("."):
    if current_filename.startswith(downloaded_filename):
      os.rename(current_filename, filename)
  print(" --- Renaming is done --- ")

if __name__=="__main__": 
  
  filename, url = arguments()
  downloaded_filename = download_from_link(get_link(url))
  rename_file(downloaded_filename, filename)
  
  print(" --- File from: \n\t" + url + "\nhas been successfully downloaded! --- ")
  print(" --- It lies under the filename: \n\t"+filename+" --- ")
