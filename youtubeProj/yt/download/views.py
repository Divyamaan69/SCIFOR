from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
import yt_dlp
import os

def download_video(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        if video_url:
            try:
                desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
                ydl_opts = {
                    'outtmpl': os.path.join(desktop_path, '%(title)s.%(ext)s'),
                    'format': 'best'
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                return HttpResponse(f'Video downloaded successfully to {desktop_path}')
            except Exception as e:
                return HttpResponse(f'Error: {e}')
    return render(request, 'download.html')
