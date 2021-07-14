import pafy
import time
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
        videoDefinition="high",
        maxResults = 10
    )
    response = request.execute()
    print('\n')
    return response

def query_main():
  a = input(prompt="Enter search item: ")
  clear_output()
  return a 

def title_sort(rep_dict):
  length = len(rep_dict['items'])
  list_res = {}
  print("{:<3.3} || {:<50.50} || {:<30.30}".format('ID','TITLE','CHANNEL'))
  for i in range(length):
    title = rep_dict['items'][i]['snippet']['title']
    vid_ID = rep_dict['items'][i]['id']['videoId']
    ch_ID = rep_dict['items'][i]['snippet']['channelTitle']
    cnum = str(i)
    list_res[cnum] = [title, vid_ID]
    print("{:<3.3} || {:<50.50} || {:<30.30}".format(cnum, title, ch_ID))
  print("<< Page: " + str(page_index) + " >>")
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

  streams = video.streams
  best_q = str(streams[-1])
  best_qp = best_q.replace("normal:","")
  
  best = video.getbest(preftype = "mp4")

  print("Downloading best video quality at {}...".format(best_qp))

  best.download()

  print("Download completed!")

  time.sleep(3)
  clear_output()
    
if __name__ == "__main__":
    authenticate()
    query = query_main()
    res_dict = main(query)
    ref_list = title_sort(res_dict)
    prev_page, next_page = next_prev(res_dict)
    
    while True:
        print("Select next action:")
        page = input("[P] Previous Page [N] Next Page [D] Download File [Q] New Query [E] End Search : ")
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
        
        elif page == "Q" or page == "q":
            clear_output()
            page_index = 0
            query = query_main()
            res_dict = main(query)
            ref_list = title_sort(res_dict)
            prev_page, next_page = next_prev(res_dict)
            
        elif page == "E" or page == "e":
            ex_q = input("Quit confirm? [Y] Yes [N] No: ")
            if ex_q == 'N' or ex_q == 'n':
                continue
            else:
                break
        
        else:
            print("Invalid key!")
    
    clear_output()
    print(".....Session Ended.....")