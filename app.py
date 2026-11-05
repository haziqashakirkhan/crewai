
import os
import re
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

load_dotenv()

# 1. Load Groq credentials
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing from .env")

# 2. Configure Groq LLM
llm = LLM(
    model="openai/openai/gpt-oss-20b",
    custom_openai=True,
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY,
    temperature=0.3,
    timeout=120,
    max_retries=3
)

# 3. Create agents

# Agent 1: Query Router
router_agent = Agent(
    role="Query Router",
    goal="Classify queries as MATH or EXPLAIN",
    backstory="You route queries to the correct agent.",
    llm=llm,
    verbose=True
)

# Agent 2: Math
math_agent = Agent(
    role="Math Expert",
    goal="Solve mathematical problems accurately",
    backstory="You are a math expert.",
    llm=llm,
    verbose=True
)

# Agent 3: Explanation
explain_agent = Agent(
    role="Teacher",
    goal="Explain concepts simply",
    backstory="You are a helpful teacher.",
    llm=llm,
    verbose=True
)


# 4. Router task
def create_router_task():
    return Task(
        description="""
        Analyze the user's query:

        {query}

        Classify it into exactly ONE category:

        MATH:
        Mathematical calculations, equations, algebra,
        arithmetic, calculus and statistics.

        EXPLAIN:
        Requests to explain concepts, theories,
        academic topics or technical subjects.

        Return ONLY MATH or EXPLAIN.
        """,
        expected_output="One category: MATH or EXPLAIN.",
        agent=router_agent
    )


# 5. Specialist task creation
def create_specialist_task(category):

    if category == "MATH":
        return Task(
            description="""
            Solve this mathematical query:

            {query}

            Show the calculation steps and explain
            the reasoning behind your solution.
            """,
            expected_output="A correct step-by-step mathematical solution.",
            agent=math_agent
        )

    return Task(
        description="""
        Explain the following query:

        {query}

        Include:
        1. A simple definition
        2. Important concepts
        3. A practical example
        4. Real-world applications where relevant
        """,
        expected_output="A clear explanation with examples.",
        agent=explain_agent
    )


# 6. Query routing function
def run_query(query):

    print("\nClassifying your query...")

    # Run router agent
    router_crew = Crew(
        agents=[router_agent],
        tasks=[create_router_task()],
        process=Process.sequential,
        verbose=True
    )

    routing_result = router_crew.kickoff(
        inputs={"query": query}
    )

    # Extract classification
    raw_result = routing_result.raw.upper().strip()

    match = re.search(r"\b(MATH|EXPLAIN)\b", raw_result)

    category = match.group(1) if match else "EXPLAIN"

    print(f"\nSelected category: {category}")

    # Select specialist
    selected_agent = (
        math_agent if category == "MATH"
        else explain_agent
    )

    # Create specialist task
    specialist_task = create_specialist_task(category)

    # Execute specialist
    specialist_crew = Crew(
        agents=[selected_agent],
        tasks=[specialist_task],
        process=Process.sequential,
        verbose=True
    )

    result = specialist_crew.kickoff(
        inputs={"query": query}
    )

    return result


# 7. Main application
if __name__ == "__main__":

    print("\n===== SMART QUERY ROUTER =====")
    print("Categories: MATH | EXPLAIN")
    print("Type 'exit' to stop.")

    while True:

        query = input("\nEnter your query: ").strip()

        if query.lower() == "exit":
            print("Application stopped.")
            break

        if not query:
            print("Please enter a query.")
            continue

        try:
            response = run_query(query)

            print("\n===== FINAL RESPONSE =====")
            print(response)

        except Exception as error:
            print(f"\nError: {error}")
