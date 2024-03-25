from flask import Flask, jsonify
from flask import *
from datetime import datetime,timedelta
from flask_cors import CORS, cross_origin
from flask_restful import Api
from flask_restful import Resource, reqparse
import datetime
import openai
import whisper
import os
import subprocess


class Langchain(Resource):
    def post(self):
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        openai.api_key = ''
        model = whisper.load_model('base.en')
        ffmpeg_path = "C:/Users/PavanKalyanR-2759/Downloads/ffmpeg/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe"
        video_path = "C:/Users/pavanKalyanR-2759/Downloads/"+file.filename
        output_audio_path = 'D:/projectDocuments/TLChatBot/src/server/langChain/extractedAudioFile/'+file.filename+'.wav'
        # ffmpeg_command = f'ffmpeg -i "{video_path}" -vn -acodec pcm_s16le -ar 44100 -ac 2 "{output_audio_path}"'
        ffmpeg_command = [ffmpeg_path, '-i', video_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2', output_audio_path]
        try:
            subprocess.run(ffmpeg_command, check=True)
            # print("Audio extraction successful.")
        except subprocess.CalledProcessError as e:
            print(f"Error during audio extraction: {e}")
        # os.system(ffmpeg_command)
        if os.path.exists(output_audio_path):
            try:
                audio_content = open(output_audio_path, "rb")
                response = openai.Audio.transcribe("whisper-1",audio_content)
                return response
            except FileNotFoundError as e:
                print(f"File not found error: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print(f"The audio file '{output_audio_path}' does not exist.")

        
            



        # option = whisper.DecodingOptions(language='en', fp16=False)
        # result = model.transcribe(fileName)
        # print("resu.....", result)