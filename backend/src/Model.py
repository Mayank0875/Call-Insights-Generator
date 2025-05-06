import langchain 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from src.Prompt import separation_prompt_template, summary_prompt_template, performance_prompt_template
from src.Audio_Ingestion import transcribe_audio

from dotenv import load_dotenv
import os
load_dotenv()


google_api_key = os.getenv('GOOGLE_API_KEY')

llm = ChatGoogleGenerativeAI(
    model = 'gemini-2.0-flash-001',
    google_api_key = google_api_key,
)


class CallAssistant:
    def __init__(self):
        pass

    def generate_structured_dialogue(self, transcript):
        prompt = PromptTemplate(
            template = separation_prompt_template,
            input_variables = ['transcript']
        )
        separation_chain = prompt | llm
        separated_dialogue = separation_chain.invoke({'transcript': transcript})
        return separated_dialogue.content
    

    def generate_summary(self, structured_dialogue):
        prompt = PromptTemplate(
            template = summary_prompt_template,
            input_variables = ['structured_dialogue']
        )
        summary_chain = prompt | llm
        summary = summary_chain.invoke({'structured_dialogue': structured_dialogue})
        return summary.content
    
    def generate_performance_report(self, structured_dialogue):
        prompt = PromptTemplate(
            template = performance_prompt_template,
            input_variables = ['structured_dialogue']
        )
        performance_report_chain = prompt | llm 
        performance_report = performance_report_chain.invoke({'structured_dialogue': structured_dialogue})
        return performance_report.content

if __name__ == "__main__":
    transcript_string = ''
    with open("data/transcript.txt", "r") as f:
        transcript_string = f.read()

    call_assistant = CallAssistant()
    structured_dialogue = call_assistant.generate_structured_dialogue(transcript_string)
    summary_prompt_template = call_assistant.generate_summary(structured_dialogue)
    performance_report_template = call_assistant.generate_performance_report(structured_dialogue)
    print(performance_report_template)