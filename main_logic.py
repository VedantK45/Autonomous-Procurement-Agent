from crewai import Crew, Process
from src.agents import IntelligenceAgents
from src.tasks import IntelligenceTasks

def run_intelligence_crew(user_query):
    """
    Assembles and executes the multi-agent crew to resolve the user's query.
    """
    # 1. Initialize our team and assignments
    agents = IntelligenceAgents()
    tasks = IntelligenceTasks()

    # 2. Get the specific Agent profiles
    manager = agents.project_manager()
    researcher = agents.semantic_researcher()
    analyst = agents.structural_analyst()
    auditor = agents.integrity_auditor()

    # 3. Instantiate the Tasks
    # The Manager takes the lead on the dynamic intelligence task
    analysis_task = tasks.dynamic_intelligence_task(manager, user_query)
    
    # The Auditor performs the final verification
    verification_task = tasks.rigorous_verification_task(auditor, [analysis_task])

    # 4. Assemble the Crew
    # We use 'Process.hierarchical' because you want the Manager to lead
    intel_crew = Crew(
        agents=[manager, researcher, analyst, auditor],
        tasks=[analysis_task, verification_task],
        process=Process.hierarchical,  # Manager orchestrates the flow
        manager_llm=manager.llm,       # The Manager uses the Groq LLM to think
        verbose=True                   # Crucial for showing 'Thinking Process' in UI
    )

    # 5. Execute and Return
    result = intel_crew.kickoff()
    return result.raw