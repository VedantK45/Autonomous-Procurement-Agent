import os
from crewai import Agent, LLM
from crewai_tools import PDFSearchTool, FileReadTool, CSVSearchTool, DirectoryReadTool
from dotenv import load_dotenv

# Loading env file
load_dotenv()

# Initializing Groq LLM - Using Llama 3.3 70B for maximum reasoning capability
groq_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.1
)

# Initializing tools
pdf_tool = PDFSearchTool()
file_tool = FileReadTool()
csv_tool = CSVSearchTool()
dir_tool = DirectoryReadTool(directory='./data_files')

class IntelligenceAgents:
    """A collection of enhanced agents designed for Universal Data Intelligence."""

    def semantic_researcher(self):
        """Profile: The 'Context Master' - Finds nuances in unstructured text."""
        return Agent(
            role='Lead Semantic Researcher',
            goal='Extract and interpret complex narratives, policies, and technical specs from documents.',
            backstory="""You are a master of linguistic context. Your expertise lies in 
            uncovering hidden details in PDFs and text files—be it a complex return policy, 
            a technical standard, or a legal liability clause. You don't just find text; 
            you explain the implications of what you found.""",
            tools=[pdf_tool, file_tool, dir_tool],
            llm=groq_llm,
            verbose=True,
            memory=True
        )

    def structural_analyst(self):
        """Profile: The 'Pattern Matcher' - Handles all structured logic and tables."""
        return Agent(
            role='Structural Data Analyst',
            goal='Identify, extract, and harmonize structured data across disparate file formats.',
            backstory="""You are an expert in data architecture. Whether it is an 
            Excel price list, a CSV inventory, or a PDF table, you align the data 
            perfectly. You specialize in quantitative analysis, comparison matrices, 
            and logical grouping of information.""",
            tools=[pdf_tool, csv_tool, file_tool, dir_tool],
            llm=groq_llm,
            verbose=True,
            memory=True
        )
    
    def integrity_auditor(self):
        """Profile: The 'Truth Guard' - Ensuring zero-hallucination compliance."""
        return Agent(
            role='Compliance & Integrity Officer',
            goal='Verify findings against the raw source data with 100% precision.',
            backstory="""You are the ultimate safety net. You treat AI hallucinations 
            as a critical system failure. Your job is to ensure that every claim, 
            date, and decimal point is physically present in the source files. 
            You force the team to cite the exact filename for every response.""",
            llm=groq_llm,
            verbose=True
        )
    
    def project_manager(self):
        """Profile: The 'Strategic Orchestrator' - The Brain of the operation."""
        return Agent(
            role='Chief Intelligence Coordinator',
            goal='Deconstruct user queries and delegate sub-tasks to maximize document insights.',
            backstory="""You are a high-level strategist. When a user asks a question, 
            you decide: Does this need a deep semantic read? A structural comparison? 
            Or both? You coordinate the Researcher and Analyst to work together, 
            ensuring the Auditor provides the final seal of approval.""",
            llm=groq_llm,
            allow_delegation=True,
            verbose=True
        )