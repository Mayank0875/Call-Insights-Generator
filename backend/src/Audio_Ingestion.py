import assemblyai as aai
import os
from dotenv import load_dotenv
load_dotenv()


def transcribe_audio(audio_file):
  aai.settings.api_key = os.getenv('ASSEMBLY_API_KEY')
  audio_file = (
      audio_file
  )

  config = aai.TranscriptionConfig(
    speaker_labels=True,
  )
  transcript = aai.Transcriber().transcribe(audio_file, config)

  content = ''
  for utterance in transcript.utterances:
    line = f"Speaker {utterance.speaker}: {utterance.text}\n"
    content += line
    print(line.strip())  # print to console
  return content


if __name__ == "__main__":
    transcribe_audio('data/Conference.wav')





