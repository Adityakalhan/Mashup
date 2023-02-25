import uyts
import requests
import os
import pytube as pt
import sys
import random
from pydub import AudioSegment

#pydub.AudioSegment.converter = 'c:\\FFmpeg\\bin\\ffmpeg.exe'

class CreateMashup() :
     
     def __init__(self,artist,number_of_songs,duration_of_clip,output_file_name) :
          self.artist = artist
          self.number_of_songs = number_of_songs
          self.duration_of_clip = duration_of_clip
          self.output = output_file_name

     def __valid_url(self,url) :
          return requests.get(url)
     def __duration(self,time) :
          if len(time) > 6 :
               return 100
          minutes = time[0]
          return int(minutes)
     def __getUrls(self) :
          query = self.artist + "songs lyric videos"
          search = uyts.Search(query,minResults = self.number_of_songs*2)
          youtube_links = []

          for result in search.resultsJSON :
               try :
                    
                    if len(youtube_links) == self.number_of_songs :
                         break
                    # print("https://www.youtube.com/watch?v=" + result['id'])
                    # print((result['duration']))
                    if self.__duration(result['duration']) < 6 : 
                         
                         link = "https://www.youtube.com/watch?v=" + result['id']
                         if self.__valid_url(link) :
                              youtube_links.append(link)
                              #print('Added')   
               except : 
                    pass 

          random.shuffle(youtube_links) 
          return youtube_links 
     

     def __create_download_folder(self,link,n=0) :
          yt = pt.YouTube(link)
          t = yt.streams.filter(only_audio=True)
          output_file = t[0].download()
          base,ext = os.path.splitext(output_file)
          output_mp3 = base + str(n) + '.mp3'
          os.rename(output_file,output_mp3)

     def create_mashup(self) :
          youtube_links = self.__getUrls()
          path = os.getcwd()
          os.makedirs(path+'\\download_folder')
          os.chdir(path+'\\download_folder')
          for i in range(len(youtube_links)) :
               self.__create_download_folder(youtube_links[i],i)
          
          combined = AudioSegment.empty()
          for filename in os.listdir(path+'\\download_folder') :

               if os.path.isfile(filename) :
                    #print('\n\n',filename)
                    try:
                         sound = AudioSegment.from_file(filename, "mp3")
                    except:
                         sound = AudioSegment.from_file(filename, format="mp4")
                    #print(filename)
                    
                    first_n_seconds = sound[:self.duration_of_clip*1000]
                    combined += first_n_seconds 
               # print('path is ',path)
               # print('output is ' ,self.output)
               # print(path + self.output)
               combined.export(path +'/'+self.output , format="mp3")        
    





def main() :
     #number of songs used should be 10 minimum
     #numbers should be int and the artist added should be in string format
     for i in sys.argv :
          print(i)
     if len(sys.argv) != 5 :
          print('ERROR : please enter the correct number of arguements')
          print('Format should be in this format : \n <program name> "artist name" number_of_songs duration_of_song <output_file.mp3>')
          exit(1)
     # elif int(sys.argv[2]) < 10 :
     #      print('ERROR : mashup must be for more than 10 songs')
     #      exit(1)
     else :
     
               mashup = CreateMashup(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4]) 
               mashup.create_mashup()
          # except :
          #      print('ERROR : Please ensure that the duration and number of songs input are integers')

if __name__ == '__main__' :
    main()