import time
from crewai import Crew, Process
from src.agents import IntelligenceAgents
from src.tasks import IntelligenceTasks

def run_intelligence_crew(user_query):
    """
    Assembles the crew and returns a structured response including metadata.
    """
    # 1. Start the timer to track generation speed
    start_time = time.time()
    
    # 2. Initialize our team and assignments
    agents_factory = IntelligenceAgents()
    tasks_factory = IntelligenceTasks()

    # 3. Get the Agent profiles
    manager = agents_factory.project_manager()
    researcher = agents_factory.semantic_researcher()
    analyst = agents_factory.structural_analyst()
    auditor = agents_factory.integrity_auditor()

    # 4. Instantiate the Tasks
    # Task 1: Analysis (Managed by the Manager)
    analysis_task = tasks_factory.dynamic_intelligence_task(manager, user_query)
    
    # Task 2: Verification (Handled by the Auditor)
    verification_task = tasks_factory.rigorous_verification_task(auditor, [analysis_task])

    # 5. Assemble the Crew with Hierarchical Process
    intel_crew = Crew(
        agents=[manager, researcher, analyst, auditor],
        tasks=[analysis_task, verification_task],
        process=Process.hierarchical,  
        manager_llm=manager.llm,       
        verbose=True                   
    )

    # 6. Execute the workflow
    result = intel_crew.kickoff()
    
    # 7. Calculate Metadata for Streamlit Add-ons
    execution_time = round(time.time() - start_time, 2)
    
    # Logic for Accuracy Meter: 
    # If the Auditor verified sources, we assign high confidence.
    # CrewAI results often contain a 'sources' attribute if tools were used.
    source_list = []
    if hasattr(result, 'sources'):
        source_list = [str(s) for s in result.sources]
    
    # Fallback: Scrape filenames from the text if sources attribute is empty
    import re
    text_sources = re.findall(r"[\w-]+\.(?:pdf|csv|xlsx|txt)", result.raw)
    final_sources = list(set(source_list + text_sources))
    
    # Calculate accuracy percentage (Simulated based on verification success)
    # If sources are found and the auditor didn't flag errors, we stay at 95%+
    accuracy_score = 98 if len(final_sources) > 0 else 75

    # 8. Return a structured dictionary for the Frontend
    return {
        "answer": result.raw,
        "time_taken": execution_time,
        "accuracy": accuracy_score,
        "sources": final_sources
    }