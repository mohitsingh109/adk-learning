from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext
from typing import Dict, Any

# Hardcoded limits for the LinkedIn Post review
MIN_LEN = 1000
MAX_LEN = 1500

def count_character(text: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Counts characters in the input text and checks if the length is within the required bounds.
    """
    current_len = len(text)

    is_valid = MIN_LEN <= current_len <= MAX_LEN

    status_message = "Length is within range." if is_valid else (
        f"Length is too short (Current: {current_len}, Min: {MIN_LEN})" if current_len < MIN_LEN
        else f"Length is too long (Current: {current_len}, Max: {MAX_LEN})"
    )

    return {
        "status": "success",
        "length": current_len,
        "min_required": MIN_LEN,
        "max_allowed": MAX_LEN,
        "is_length_valid": is_valid,
        "message": status_message
    }

def exit_loop(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Stops the iterative agent loop by setting the escalation flag.
    Should only be called when all review criteria are met.
    """
    tool_context.actions.escalate = True
    return {
        "status": "termination_success",
        "message": "All review requirements met. Stopping iterative refinement."
    }

post_reviewer = LlmAgent(
    name="post_reviewer",
    model="gemini-2.0-flash",
    description="Critically reviews a LinkedIn post for quality, professional tone, and adherence to specific length requirements.",
    instruction="""
You are the **LinkedIn Post Quality Assurance Reviewer**. Your role is to critically assess a draft LinkedIn post based on quality, professional tone, and specific length requirements. You must be **strict** and **professional**.

Current Post: {current_post}

**Strict Constraints:**
1.  **No Emojis:** You MUST NOT include any emojis in your feedback or analysis.
2.  **Tone & CTA:** The post must maintain a highly professional, expert tone, and include a clear Call-to-Action (CTA).

**Execution Workflow (MANDATORY):**

1.  **CALL TOOL:** Immediately call `count_character(text=...)` on the draft post text to assess its length against the MIN (1000) and MAX (1500) limits.
2.  **ANALYZE & DECIDE:** Based on the tool's result and your manual quality assessment:
    * **SUCCESS CONDITION:** If the post is professionally sound (meets all tone/CTA criteria) AND the tool reports `"is_length_valid": True`:
        * **ACTION:** Immediately call the `exit_loop()` tool to terminate the refinement process.
    * **FEEDBACK CONDITION:** If **ANY** requirement is not met (poor quality OR invalid length):
        * **ACTION:** Do NOT call `exit_loop()`. Instead, generate detailed, structured feedback in the format below.

**Feedback Format (If action is Feedback):**
Output only the requested feedback in the following format.

### Post Review Feedback

#### Content & Tone Critique
[Provide specific, actionable feedback on tone, clarity, and professionalism. Mention missing or weak CTA if applicable.]

#### Length Compliance
[State the current character count and whether the post needs to be longer or shorter, using the information gathered from the `count_character` tool.]

**Goal:** Either provide clear, actionable feedback for improvement, or signal termination via the `exit_loop` tool.
    """,
    output_key="review_feedback",
    tools=[count_character, exit_loop]
)