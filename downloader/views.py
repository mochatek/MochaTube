from django.shortcuts import render, redirect
import pafy

# Create your views here.

def sizeConvert(size,precision=2):
    suffixes=[' B',' KB',' MB',' GB',' TB']
    suffixIndex = 0
    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1 #increment the index of the suffix
        size = size/1024.0 #apply the division
    return "%.*f%s"%(precision,size,suffixes[suffixIndex])

def index(request):
    context = {"results" : None,"success":True}
    if request.method == 'GET':
        if 'url' in request.GET:
            url = request.GET.get("url")
            try:
                results = []
                video = pafy.new(url)
                for s in reversed(video.streams):
                    results.append({
                        "resolution" :s.resolution,
                        "extension" : s.extension+" (Video)",
                        "size" : sizeConvert(s.get_filesize()),
                        "url" : s.url
                    })
                for s in reversed(video.audiostreams):
                    results.append({
                        "resolution" :s.bitrate,
                        "extension" : s.extension+" (Audio)",
                        "size" : sizeConvert(s.get_filesize()),
                        "url" : s.url
                    })
                context = {"results":results,
                "title":video.title,
                "like":video.likes,
                "dislike":video.dislikes,
                "view":video.viewcount,
                "duration":video.duration,
                "thumb":video.thumb
                }
            except:
                context = {"results" : None,"success":False}
    return render(request, "downloader/index.html", context = context)