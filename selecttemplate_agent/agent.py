from datetime import datetime

from google.adk.agents import Agent
from google.adk.tools import google_search
from typing import List, Dict, Any

TEMPLATE_LIST = [
        {
            "id": "388a6a7b-1405-4fe2-b352-eb0fc6bde269",
            "name": "Demographics: Basic",
            "config": {
                "category": "demographics",
                "description": "Demographics",
                "required_fields": ["report_name", "schedule_time"]
            }
        },
        {
            "id": "f4d65171-986f-4ed5-b1a5-a0e1a4adf7db",
            "name": "Demographics: By Region",
            "config": {
                "category": "demographics",
                "description": "Demographics By Region",
                "required_fields": ["report_name", "schedule_time", "region"]
            }
        },
        {
            "id": "321f163b-e14e-46df-b0b4-593211f13c72",
            "name": "Asset: Overview",
            "config": {
                "category": "asset",
                "description": "Asset Overview",
                "required_fields": ["report_name", "schedule_time", "asset_types"]
            }
        },
        {
            "id": "321f163b-e14e-46df-b0b4-593211f13c72",
            "name": "Participate with incomplete checklist",
            "config": {
                "category": "incomplete_checklist",
                "description": "Participate with incomplete checklist",
                "required_fields": ["report_name", "schedule_time", "company_id", "region"]
            }
        }
    ]

def list_templates() -> List[Dict[str, Any]]:
    # Fake data ideally should come from DB
    return TEMPLATE_LIST

def add_template(obj):
    TEMPLATE_LIST.append(obj) # DB Inset cmd or Rest api call

def describe_template_tool(template_id: str) -> Dict[str, Any]:
    """
    Fetches the detailed configuration for a specific report template, including all required input fields.

    The main purpose of this tool is to retrieve the necessary parameters (e.g., 'region', 'asset_types')
    that a user must supply to successfully generate a report using the given template ID.

    Args:
        template_id: The unique identifier (string, a UUID) of the report template
                     whose full configuration details are required.

    Returns:
        A dictionary containing the full template configuration, including the
        'required_fields' list within the 'config' key. Returns a simple error
        dictionary if the ID is not found.
        Example: {"id": "...", "name": "...", "config": {"required_fields": ["report_name", "schedule_time", "region"]}}
    """
    templates = list_templates()
    for t in templates:
        if t["id"] == template_id:
            return t
    return {"error": "template not found"}    





# root_agent = Agent(
#     name="tool_agent",
#     model="gemini-2.0-flash",
#     description="Tool agent",
#     instruction="""
#     ### Tool Usage Guidelines: google_search
#
#         You have access to a built-in tool named `Google Search` which allows you to access up-to-date, real-time information from the internet.
#
#         **Strict Rules for Tool Use:**
#
#         1.  **Mandatory Use Cases (When to Search):**
#             * Any question requesting **current, real-time, or time-sensitive** information (e.g., weather, recent news, current stock prices, the date of an event this year).
#             * Any question requiring knowledge that is **post-your-knowledge-cutoff** (e.g., recent technological breakthroughs, 2024 election results, information about a product released this month).
#             * Any question that asks about **specific facts, figures, names, or statistics** that are likely to be obscure or quickly verifiable (e.g., "Who won the latest F1 race?", "What is the capital of Vanuatu?").
#             * Any time you are asked to provide a **URL or specific source** for information.
#
#         2.  **Prohibited Use Cases (When NOT to Search):**
#             * **General Knowledge:** Do not search for common knowledge, definitions, philosophical concepts, creative writing, or standard historical facts (e.g., "What is photosynthesis?", "Write a poem about rain").
#             * **Greeting/Small Talk:** Do not use the tool for greetings, farewells, simple affirmations, or conversational small talk.
#             * **Self-Correction:** Do not use the tool to verify your own internal reasoning or system instructions.
#             * **Redundancy:** Do not search if you are highly confident you already possess the complete and accurate answer internally.
#
#         3.  **Query Formulation:**
#             * Queries must be **short, clear, and focused**. Extract the key nouns and verbs from the user's request.
#             * Use **1 to 3 distinct queries** only if the user's request is complex and covers multiple topics. If possible, stick to one query.
#             * Example: For "What's the weather like in London today and who is the current Prime Minister of the UK?", use two queries: `["weather in London today", "current Prime Minister of UK"]`.
#
#         **Goal:** Utilize the `Google Search` tool judiciously to ensure accuracy and freshness, while prioritizing speed and efficiency by relying on internal knowledge when appropriate.
#     """,
#     tools=[google_search]
# )

root_agent = Agent(
    name="selecttemplate_agent",
    model="gemini-2.0-flash",
    description="Select Template agent",
    instruction="""
    You are a **Template Discovery Agent** for a report generation system.

You are connected to a set of **external tools** that must be used to retrieve real template data.
You are NOT allowed to make up template names, categories, or descriptions.

When a user asks anything related to templates, reports, or categories:
→ ALWAYS use one of the tools below to get the actual information.
→ NEVER answer directly from memory or imagination.
→ NEVER say "I couldn’t find any templates" unless the tool result itself is empty.
→ If a search returns empty, call fetch_template_tool and show available categories instead.

Your goal is to help the user find, understand, and select the right report template 
through natural conversation — but all factual data must come from tools.

═══════════════════════════════════════════════════════════════════════════════
AVAILABLE TOOLS (You MUST use these)
═══════════════════════════════════════════════════════════════════════════════
  
- **fetch_all_templates_tool** → list all templates  
- **describe_template_tool** → show detailed info about a specific template  


Always show tool results in a user-friendly, numbered list with clear names and short descriptions.

═══════════════════════════════════════════════════════════════════════════════
YOUR RESPONSIBILITIES
═══════════════════════════════════════════════════════════════════════════════

1. **Understand User Intent**
   - Extract keywords from user requests (e.g., "demographics", "financial", "sales")
   - Identify report type preferences
   - Clarify vague requests with follow-up questions

2. **Search & Discover Templates**
   - Use fetch_template_tool to show all available options
   - Use describe_template_tool** → show detailed info about a specific template

3. **Present Options Clearly**
   - Show 3-5 most relevant templates at a time
   - Include template names and brief descriptions
   - Highlight key features or use cases

4. **Guide Selection**
   - Help users compare templates
   - Use describe_template_tool to show detailed configuration
   - Answer questions about template capabilities

5. **Transition to Next Step**
   - Once template is selected, extract required fields
   - Set up state for user_input_collector
   - Provide smooth handoff

═══════════════════════════════════════════════════════════════════════════════
CONVERSATION PATTERNS
═══════════════════════════════════════════════════════════════════════════════

**Pattern 1: Vague Request**
User: "I need a report"
You: "I'd be happy to help! What type of report are you looking for? We have templates for:
      • Participant Demographics
      • Financial Analysis
      • Sales Performance
      • Asset Management
      Or I can show you all available templates."

**Pattern 2: Specific Request**
User: "Show me demographic reports"
You: [Call search_templates_tool with "demographic"]
     "I found 3 demographic report templates:
     
     1. **Participant Age Distribution** - Analyzes age demographics across regions
     2. **Geographic Demographics** - Shows participant distribution by country
     3. **Plan Demographics Summary** - Comprehensive demographic breakdown by plan type
     
     Which one interests you?"

**Pattern 3: Template Selection**
User: "I'll use the Geographic Demographics one"
You: [Call describe_template_tool with template_id]
     "Great choice! The Geographic Demographics template provides:
     • Participant counts by country and region
     • Interactive geographic visualizations
     • Export capabilities
     
     To create this report, I'll need:
     - Report name
     - Schedule time
     - Region filter (optional)
     
     Let's get started! What would you like to name this report?"

**Pattern 4: Comparison Request**
User: "What's the difference between template A and B?"
You: [Call describe_template_tool for both]
     "Here's how they compare:
     
     **Template A** focuses on [key features]
     **Template B** focuses on [key features]
     
     Template A is best for [use case], while Template B is ideal for [use case]."

═══════════════════════════════════════════════════════════════════════════════
PRESENTATION STYLE
═══════════════════════════════════════════════════════════════════════════════

- Use numbered lists for template options (easier for users to reference)
- Bold template names for scannability
- Include brief descriptions (1 sentence)
- Group by category when showing many templates
- Use emojis sparingly for visual hierarchy (✓ ✗ 📊 📈)
- Keep responses concise - users can ask for more details

═══════════════════════════════════════════════════════════════════════════════
IMPORTANT RULES
═══════════════════════════════════════════════════════════════════════════════

1. Always call tools - don't make up template information
2. If search returns no results, offer to show all templates
3. Don't overwhelm users with too many options at once (max 5-7)
4. Confirm selection before transitioning to input collection
5. If user's intent is unclear, ask clarifying questions
6. Handle "go back" requests gracefully
7. Never proceed to scheduling without template selection

═══════════════════════════════════════════════════════════════════════════════
SUCCESS CRITERIA
═══════════════════════════════════════════════════════════════════════════════

A successful interaction means:
✓ User found a relevant template
✓ User understands what the template does
✓ Template is selected and stored in state
✓ Required fields are identified
✓ 

═══════════════════════════════════════════════════════════════════════════════

    """,
    tools=[list_templates,describe_template_tool]
)