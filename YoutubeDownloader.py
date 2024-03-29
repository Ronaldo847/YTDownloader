import pafy
import time
from echar import *
from IPython.display import clear_output

# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

global page_index
page_index = 0

def authenticate():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    print('\n')
    
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "CLI.json"

    # Get credentials and create an API client
    while True:
      try:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
          client_secrets_file, scopes)
        credentials = flow.run_console()
        global youtube
        youtube = googleapiclient.discovery.build(
          api_service_name, api_version, credentials=credentials)
        break
      except:
        print("Invalid code! Try again.")
    
    print('\n')

def main(query, next_prev=""):
    request = youtube.search().list(
        part="snippet",
        order="relevance",
        pageToken = next_prev,
        q=query,
        type="video",
        videoDefinition="any",
        maxResults = 10
    )
    response = request.execute()
    print('\n')
    return response

def stat_query(vid_ID):
  request = youtube.videos().list(
    part="statistics,contentDetails",
    id = vid_ID
  )
  response = request.execute()
  views = response['items'][0]['statistics'].get('viewCount', '403 - Forbidden')
  duration = response['items'][0]['contentDetails'].get('duration', '403 - Forbidden')
  stat = (views, duration)
  return stat

def query_main():
  a = input(prompt="Enter search keywords or video link: ")
  return a 

def title_sort(rep_dict):
  length = len(rep_dict['items'])
  list_res = {}
  print(126*"-")
  print("|| {:^3.3} || {:^50.50} || {:^30.30} || {:^11.11} || {:^10.10} ||".format('ID','TITLE','CHANNEL', 'DURATION', 'VIEWS'))
  print(126*"-")
  for i in range(length):
    title_r = rep_dict['items'][i]['snippet']['title']
    title = echar(title_r)
    vid_ID = rep_dict['items'][i]['id']['videoId']
    ch_ID = rep_dict['items'][i]['snippet']['channelTitle']
    views, duration = stat_query(vid_ID)
    cnum = str(i)
    list_res[cnum] = [title, vid_ID]
    print("|| {:^3.3} || {:<50.50} || {:<30.30} || {:<11.11} || {:<10.10} ||".format(cnum, title, ch_ID, duration, views))
    print(126*"-")
  print("<< Page: " + str(page_index) + " >>")
  print('\n')
  return list_res

def next_prev(rep_dict):
    try:
        prev_page = rep_dict['prevPageToken']
    except:
        prev_page = ""
    
    try:
        next_page = rep_dict['nextPageToken']
    except:
        next_page = ""
        
    selection = [prev_page,next_page]
    
    return selection

def download_file(vid_ID):
  pref_url = "https://www.youtube.com/watch?v="
  url = pref_url + vid_ID
  video = pafy.new(url)

  v_streams = video.streams
  a_streams = video.audiostreams

  print("Download as: ")
  dl_op = input("[V] Video only [A] Audio only [B] Both: ")
  print('\n')

  if dl_op == "V" or dl_op == "v":
    for vk in range(len(v_streams)):
      print("[" + str(vk) + "] >>> " + str(v_streams[vk]))
    print('\n')

    v_qs = int(input("Input number of selected quality (press Enter for best quality): ") or "-1")
    v_dl = v_streams[v_qs]

    if v_qs > 0:
      print("Downloading video at {} quality <{} MB>...".format(v_dl, (v_dl.get_filesize()/1000000)))
    else:
      print("Downloading video at {} quality (best) <{} MB>...".format(v_dl, (v_dl.get_filesize()/1000000)))
    v_dl.download()

  elif dl_op == "A" or dl_op == "a":
    if a_streams != None:
      for ak in range(len(a_streams)):
        print("[" + str(ak) + "] >>> " + str(a_streams[ak]))
      print('\n')
      
      a_qs = int(input("Input number of selected quality (press Enter for best quality): ") or "-1")
      a_dl = a_streams[a_qs]

      if a_qs > 0:
        print("Downloading audio at {} quality <{} MB>...".format(a_dl, (a_dl.get_filesize()/1000000)))
      else:
        print("Downloading audio at {} quality (best) <{} MB>...".format(a_dl, (a_dl.get_filesize()/1000000)))
      a_dl.download()
    else:
      print("No audio file available.")
  
  else:
    v_best = video.getbest(preftype = "mp4")
    a_best = video.getbestaudio(preftype = "any")

    print("Downloading best video & audio quality at {} & {}".format(v_best, a_best))
    print("File sizes: Video = " + str(v_best.get_filesize()/1000000) + " MB" + " Audio = " + str(a_best.get_filesize()/1000000) + " MB")
    
    v_best.download()
    a_best.download()

  print("\nDownload completed!\n")

def quit_session():
  ex_q = input("Quit confirm? [Y] Yes [N] No: ")
  if ex_q == 'N' or ex_q == 'n':
    return False
  else:
    clear_output()
    print("<<<<< Session Ended >>>>>")
    return True
    
if __name__ == "__main__":
    passthru = True
    authenticate()
    while True:
      try:
        query = query_main()
        res_dict = main(query)
        ref_list = title_sort(res_dict)
        prev_page, next_page = next_prev(res_dict)
        break
      except KeyError as err:
        print("An error on parsing the contents has occured.")
        print(err + '\n')
      except errors.HttpError as err:
        print("Bad request or connectivity issues has occured.")
        print(err + '\n')

      print("Select next action:")
      ex = input("Enter a [N] new query or [E] exit this program: ")
      if ex == "N" or ex == "n":
        clear_output()
        print("<New Query> <Previous Query = " + str(query) + " >")
      else:
        passthru != quit_session()
        break
       
    while passthru == True:
        print("Select next action:")
        page = input("[P] Previous Page [N] Next Page [D] Download File [Q] New Query [E] End Search : ")
        print('\n')
        if page == "P" or page == "p":
            clear_output()
            if page_index > 0:
              page_index -= 1
            res_dict = main(query, prev_page)
            ref_list = title_sort(res_dict)
            prev_page, next_page = next_prev(res_dict)
            
        elif page == "N" or page == "n":
            clear_output()
            page_index += 1
            res_dict = main(query, next_page)
            ref_list = title_sort(res_dict)
            prev_page, next_page = next_prev(res_dict)
        
        elif page == "D" or page == "d":
            item_str = input(prompt="Select title number you want to download: ")
            for_dl = ref_list[item_str][1]
            download_file(for_dl)
            time.sleep(3)
            clear_output()
            title_sort(res_dict)
        
        elif page == "Q" or page == "q":
            clear_output()
            page_index = 0
            print("<New Query> <Previous Query = " + str(query) + " >")
            query = query_main()
            res_dict = main(query)
            ref_list = title_sort(res_dict)
            prev_page, next_page = next_prev(res_dict)
            
        elif page == "E" or page == "e":
            if quit_session():
              break
        
        else:
            print("Invalid key!")