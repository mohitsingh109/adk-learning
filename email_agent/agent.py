from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field


# Define the output schema
class EmailContent(BaseModel):
    subject: str = Field(
        description="A **concise, attention-grabbing, and professional** summary of the email's content. Should be suitable for the recipient's inbox and not exceed 10-15 words."
    )
    body: str = Field(
        description="The **full, well-formatted text content** of the email, including a salutation (e.g., 'Dear [Recipient Name]'), the core message, and a professional closing signature (e.g., 'Best regards, [Your Name]'). Ensure clear paragraphs and complete sentences."
    )

root_agent = LlmAgent(
    name="email_agent",
    model="gemini-2.0-flash",
    description="A specialist agent for generating a complete email, including the subject and body. It always outputs a single, valid JSON object conforming to the EmailContent schema.",
    instruction="""
    You are a dedicated **Email Content Generator Agent**. Your sole function is to process the user's request and synthesize a **complete, high-quality email**.

    **Strict Output Rule:**
    Your final and *only* output must be a single, valid JSON object that strictly adheres to the provided `EmailContent` schema (with fields for 'subject' and 'body').

    **Process & Content Requirements:**
    1.  **Analyze** the user's intent (e.g., request for a meeting, a follow-up, a formal complaint, etc.).
    2.  **Generate** a professional and concise `subject` line (10-15 words max).
    3.  **Construct** the `body` of the email, ensuring it is well-formatted and includes all necessary components:
        * A suitable salutation (e.g., "Dear [Name],", "Hello,").
        * The core message based on the user's request.
        * A professional closing/sign-off (e.g., "Best regards,", "Sincerely,").

    **CRITICAL:**
    * **NEVER** include any conversational text, introductory phrases, or explanations outside of the final JSON object.
    * **The entire response** must be the raw JSON string.
    """,
    output_schema=EmailContent,
    output_key="email"
)

"""
{
    "email": {
        "subject": "<>",
        "body": "<>"
    }
}
"""