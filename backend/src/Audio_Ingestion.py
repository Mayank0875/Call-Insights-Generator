import assemblyai as aai
import os
from dotenv import load_dotenv
import uuid
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
  random_filename = f"{uuid.uuid4().hex}.txt"

  # Save diarized transcript to a text file
  with open(f"data/{random_filename}", "w") as f:
      for utterance in transcript.utterances:
          line = f"Speaker {utterance.speaker}: {utterance.text}\n"
          print(line.strip())  # print to console
          f.write(line)        # write to file
  return random_filename


if __name__ == "__main__":
   transcribe_audio('data/Conference.wav')





