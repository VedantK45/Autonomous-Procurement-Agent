import os
from crewai import Agent,LLM
from crewai_tools import PDFSearchTool, FileReadTool, CSVSearchTool, DirectoryReadTool
from dotenv import load_dotenv

#loading env file
load_dotenv()

#Initializing Groq LLM
groq_llm=LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.1
)

#Initializing tools for interacting with different types of files
pdf_tool=PDFSearchTool()
file_tool=FileReadTool()
csv_tool=CSVSearchTool()
dir_tool=DirectoryReadTool(directory='./data_files')

class IntelligenceAgents:
    """A collection of agents designed for data intelligence """

    def document_specialist(self):
        """Finds technical specs, legal terms, and dates."""
        return Agent(
            role='Document Intelligence Analyst',
            goal='Extract precise technical and non-financial details from provided files.',
            backstory="""You are a veteran auditor. You don't just find keywords; 
            you understand context. You specialize in reading warranty clauses, 
            delivery timelines, and technical product specifications.""",
            tools=[pdf_tool, file_tool, csv_tool, dir_tool],
            llm=groq_llm,
            verbose=True,
            memory=True
        )

    def pricing_analyst(self):
        """Specializes in math, tables, and cost comparisons."""
        return Agent(
            role='Financial Procurement Analyst',
            goal='Extract and compare pricing, discounts, and tax terms across all vendors.',
            backstory="""You are an expert in financial data. You excel at turning 
            messy PDF quotes into clean comparison tables. You always look for the 
            lowest unit price and hidden costs.""",
            tools=[pdf_tool, csv_tool, file_tool, dir_tool],
            llm=groq_llm,
            verbose=True,
            memory=True
        )
    
    def fact_auditor(self):
        """The 'Safety Net' that prevents hallucinations."""
        return Agent(
            role='Source Verification Officer',
            goal='Verify every claim against the original raw text and provide citations.',
            backstory="""You are skeptical and detail-oriented. Your job is to 
            prevent hallucinations. If you cannot find a direct quote in the file 
            to support a claim, you must reject the answer. 
            You always add 'Source: [filename]' to every response.""",
            llm=groq_llm,
            verbose=True
        )
    
    def manager_agent(self):
        """The 'Brain' that decides which specialist to use."""
        return Agent(
            role='Project Manager',
            goal='Direct the query to the correct specialist and ensure a high-quality final report.',
            backstory="""You are a high-level supervisor. You receive user queries. 
            If a query is about price, you call the Pricing Analyst. 
            If it is about specs, you call the Document Specialist. 
            You ensure the Auditor checks everything before giving the final answer.""",
            llm=groq_llm,
            allow_delegation=True, # This allows the manager to assign tasks to others
            verbose=True
        )
