import pytubefix
import ffmpeg
import openai

openai.api_key = "Chave-API"


#Baixar o áudio do arquivo
import sys 
url = sys.argv[1]
filename = "audio.wav"
yt = pytubefix.YouTube(url)
stream = yt.streams.filter(only_audio=True).first().url
ffmpeg.input(stream).output(filename,
                            format = 'wav',
                            loglevel = "error").run()

#Cria a transcrição
audio_file = open(filename, "rb")
transcript = openai.Audio.transcribe(
    model="whisper-1",
    file=audio_file
)["text"]

#Pede pela revisão
completion =  openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": """
        Você é um assistente que resume vídeos desta forma:
        Responda com formatação Markdown.
        """},
        {"role": "user", "content": f"Descreva o seguinte vídeo: {transcript}"}
    ]
)
with open("resumo.md", "w+") as md:
    md.write(completion.choices[0].message.content)
