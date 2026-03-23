import sys, os
import whisper
import yt_dlp

link = sys.argv[1]
platform = sys.argv[2].lower()

video_path = "videos/video.mp4"

# 🔽 DOWNLOAD YOUTUBE (NOVO - yt-dlp)
if platform == "youtube":
    ydl_opts = {
        'outtmpl': video_path,
        'format': 'mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

else:
    print("Use apenas youtube por enquanto")
    sys.exit()

# 🔽 TRANSCRIÇÃO (LEVE)
model = whisper.load_model("tiny")
result = model.transcribe(video_path)

segments = result["segments"]

# 🔽 PEGA 5 PARTES
cuts = segments[:5] if len(segments) >= 5 else segments

# 🔽 CRIA CLIPES
for i, seg in enumerate(cuts):
    start, end = seg["start"], seg["end"]
    
    os.system(f'ffmpeg -i "{video_path}" -ss {start} -to {end} -c copy "clips/clip_{i}.mp4"')

print("5 clips gerados!")