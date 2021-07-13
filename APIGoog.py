# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 14:44:43 2021

@author: S7341
"""
import pafy

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
            print("Invalid key! Try again.")
    
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
  print('\n')
  return a 

def title_sort(rep_dict):
  length = len(rep_dict['items'])
  list_res = {}
  print("{:<3.3} || {:<50.50} || {:<30:30}".format('ID','TITLE','CHANNEL'))
  for i in range(length):
    title = rep_dict['items'][i]['snippet']['title']
    vid_ID = rep_dict['items'][i]['id']['videoId']
    ch_ID = rep_dict['items'][i]['snippet']['channelTitle']
    cnum = str(i)
    list_res[cnum] = [title, vid_ID]
    print("{:<3.3} || {:<50.50} || {:<30.30}".format(cnum, title, ch_ID)
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

  streams = video.streams
  best_q = str(streams[-1])
  best_qp = best_q.replace("normal:","")
  
  best = video.getbest(preftype = "mp4")

  print("Downloading best video quality at {}...".format(best_qp))

  best.download()

  print("Download completed!")

    
if __name__ == "__main__":
    authenticate()
    query = query_main()
    res_dict = main(query)
    ref_list = title_sort(res_dict)
    prev_page, next_page = next_prev(res_dict)
    
    while True:
        page = input("[P] Previous Page [N] Next Page [D] Download File [Q] New Query [E] End Search : ")
        if page == "P" or page == "p":
            res_dict = main(query, prev_page)
            ref_list = title_sort(res_dict)
            prev_page, next_page = next_prev(res_dict)
            
        elif page == "N" or page == "n":
            res_dict = main(query, next_page)
            ref_list = title_sort(res_dict)
            prev_page, next_page = next_prev(res_dict)
        
        elif page == "D" or page == "d":
            item_str = input(prompt="Select title number you want to download: ")
            for_dl = ref_list[item_str][1]
            download_file(for_dl)
        
        elif page == "Q" or page == "q":
            query = query_main()
            res_dict = main(query)
            ref_list = title_sort(res_dict)
            prev_page, next_page = next_prev(res_dict)
            
        elif page == "E" or page == "e":
            break
        
        else:
            print("Invalid key!")


 
