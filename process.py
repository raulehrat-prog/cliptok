import sys, os
import whisper
import yt_dlp

link = sys.argv[1]
platform = sys.argv[2].lower()

# 🔥 limpa clips
if os.path.exists("clips"):
    for f in os.listdir("clips"):
        os.remove(os.path.join("clips", f))
else:
    os.makedirs("clips")

if not os.path.exists("videos"):
    os.makedirs("videos")

video_path = f"videos/video_{os.getpid()}.mp4"

# DOWNLOAD
if platform == "youtube":
    ydl_opts = {
        'outtmpl': video_path,
        'format': 'mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
else:
    print("erro")
    sys.exit()

# TRANSCRIÇÃO
model = whisper.load_model("tiny")
result = model.transcribe(video_path)

segments = result["segments"]

cuts = segments[:5] if len(segments) >= 5 else segments

clips = []

# CRIAR CLIPS
for i, seg in enumerate(cuts):
    start, end = seg["start"], seg["end"]

    # 🔥 evita clip vazio
    if end - start < 1:
        continue

    output = f"clips/clip_{i}.mp4"

    cmd = f'ffmpeg -y -i "{video_path}" -ss {start} -to {end} -c:v libx264 -c:a aac "{output}"'
    print("CMD:", cmd)

    os.system(cmd)

    # 🔥 só adiciona se existe
    if os.path.exists(output):
        clips.append(f"/clips/clip_{i}.mp4")

# 🔥 retorna só os válidos
print("CLIPS:", ",".join(clips))