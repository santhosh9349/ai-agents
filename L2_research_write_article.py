import warnings
warnings.filterwarnings('ignore')
from crewai import Agent, Task, Crew
from crewai import LLM
import os

# --- USE GEMINI INSTEAD OF OPENAI ---
# 1. Set your Google Gemini API key
# Get your key from https://aistudio.google.com/
# IMPORTANT: Make sure you have also enabled the "Generative Language API"
# in your Google Cloud project console.
os.environ["GEMINI_API_KEY"] = "AIzaSyDvBFH7KvTetODdTg9q0Yo1H2KwN5RWIwA"

# 2. Define the LLM using the gemini/model-name format
# We are using the 'gemini-2.5-flash-lite' model you requested.
llm = LLM(model="gemini/gemini-2.5-flash-lite")

# --- Agent Definitions (No changes needed) ---

planner = Agent(
    role="Content Planner",
    goal="Plan engaging and factually accurate content on {topic}",
    backstory="You're working on planning a blog article "
              "about the topic: {topic}."
              "You collect information that helps the "
              "audience learn something "
              "and make informed decisions. "
              "Your work is the basis for "
              "the Content Writer to write an article on this topic.",
    allow_delegation=False,
    verbose=True,
    llm=llm  # Pass the Gemini llm
)

writer = Agent(
    role="Content Writer",
    goal="Write engaging and factually accurate blog posts on {topic}",
    backstory="You're working on writing a blog article "
              "about the topic: {topic}."
              "You use the content plan from the Content Planner "
              "to craft compelling blog posts that educate and inform.",
    allow_delegation=False,
    verbose=True,
    llm=llm  # Pass the Gemini llm
)

editor = Agent(
    role="Editor",
    goal="Edit a given blog post to align with "
         "the writing style of the organization. ",
    backstory="You are an editor who receives a blog post "
              "from the Content Writer. "
              "Your goal is to review the blog post "
              "to ensure that it follows journalistic best practices,"
              "provides balanced viewpoints "
              "when providing opinions or assertions, "
              "and also avoids major controversial topics "
              "or opinions when possible.",
    allow_delegation=False,
    verbose=True,
    llm=llm  # Pass the Gemini llm
)

# --- Task Definitions (No changes needed) ---

plan = Task(
    description=(
        "1. Prioritize the latest trends, key players, "
            "and noteworthy news on {topic}.\n"
        "2. Identify the target audience, considering "
            "their interests and pain points.\n"
        "3. Develop a detailed content outline including "
            "an introduction, key points, and a call to action.\n"
        "4. Include SEO keywords and relevant data or sources."
    ),
    expected_output="A comprehensive content plan document "
        "with an outline, audience analysis, "
        "SEO keywords, and resources.",
    agent=planner,
)

write = Task(
    description=(
        "1. Use the content plan to craft a compelling "
            "blog post on {topic}.\n"
        "2. Incorporate SEO keywords naturally.\n"
		"3. Sections/Subtitles are properly named "
            "in an engaging manner.\n"
        "4. Ensure the post is structured with an "
            "engaging introduction, insightful body, "
            "and a summarizing conclusion.\n"
        "5. Proofread for grammatical errors and "
            "alignment with the brand's voice.\n"
    ),
    expected_output="A well-written blog post "
        "in markdown format, ready for publication, "
        "each section should have 2 or 3 paragraphs.",
    agent=writer,
)

edit = Task(
    description=("Proofread the given blog post for "
                 "grammatical errors and "
                 "alignment with the brand's voice."),
    expected_output="A well-written blog post in markdown format, "
                    "ready for publication, "
                    "each section should have 2 or 3 paragraphs.",
    agent=editor
)

# --- Crew Definition (No changes needed) ---

crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan, write, edit],
    verbose=True
)

# --- Kickoff ---

print("Kicking off the crew with Gemini...")
result = crew.kickoff(inputs={"topic": "blockchain technology"})

print("\n\n########################")
print("## Crew Execution Result:")
print("########################\n")
print(result)

from IPython.display import Markdown, display
display(Markdown(result))
