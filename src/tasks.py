from crewai import Task

class IntelligenceTasks:
    """Universal assignments for deconstructing any document-based request."""

    def dynamic_intelligence_task(self, agent, user_query):
        """
        An open-ended intelligence task that instructs the manager to deconstruct 
        the query into semantic and structural sub-goals.
        """
        return Task(
            description=f"""
            **Objective**: Resolve the following multi-dimensional query: '{user_query}'
            
            **Protocol**:
            1. **Deconstruction**: Break this query into sub-questions. Identify if the user needs:
               - Quantitative Data (tables, numbers, dates)
               - Qualitative Narratives (policies, descriptions, clauses)
               - Comparative Analysis (differences between files)
            2. **Multi-File Synthesis**: Search through all documents in './data_files'. You must connect 
               related information across different files (e.g., if a PDF mentions a model and a CSV 
               mentions its price).
            3. **Semantic Reasoning**: Do not just copy-paste. Explain the 'why' behind the data if the 
               query requires interpretation.
            4. **Zero-Knowledge Guardrail**: Strictly ignore your internal training data. If the specific 
               answer isn't in the provided Excel, PDF, or Text files, admit it clearly.
            """,
            expected_output="""A high-fidelity intelligence report that synthesizes data from all 
            relevant files. Use Markdown tables for data comparisons and bullet points for 
            thematic summaries. Must be professional and boardroom-ready.""",
            agent=agent
        )

    def rigorous_verification_task(self, agent, context_tasks):
        """
        A 'Red-Teaming' task that audits the intelligence report for factual 
        grounding and source transparency.
        """
        return Task(
            description="""
            **Audit Protocol**:
            1. **Source Mapping**: Map every claim, figure, or policy statement to a specific file name.
            2. **Logical Validation**: Check if the 'Structural Analyst' or 'Semantic Researcher' 
               made assumptions that aren't explicitly stated in the docs.
            3. **Citation Format**: Ensure every section has a [Source: filename] tag.
            4. **Completeness Check**: Did the team miss a file in the folder that could have 
               contributed to the answer?
            """,
            expected_output="""An audited, source-indexed final response. If a discrepancy 
            was found during the audit, correct it before presenting the final result.""",
            agent=agent,
            context=context_tasks
        )