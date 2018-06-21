#!/usr/bin/env python3
# _*_ coding: utf-8 _*

import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pi/Desktop/txt2speech.json"

def synthesize_text(text):
    """Synthesizes speech from the input string of text."""
    from google.cloud import texttospeech_v1beta1
    client = texttospeech_v1beta1.TextToSpeechClient()

    input_text = texttospeech_v1beta1.types.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech_v1beta1.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech_v1beta1.enums.SsmlVoiceGender.FEMALE)

    audio_config = texttospeech_v1beta1.types.AudioConfig(
        audio_encoding=texttospeech_v1beta1.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(input_text, voice, audio_config)

    # The response's audio_content is binary.
    with open('output.mp3', 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

synthesize_text('hello')