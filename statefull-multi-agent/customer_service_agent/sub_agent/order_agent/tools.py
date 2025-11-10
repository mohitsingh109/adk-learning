from google.adk.tools import ToolContext


from google.adk.tools import ToolContext
from datetime import datetime

refund_course_id = "ai_marketing_platform"
refund_window_days = 15
current_time = datetime.now().strftime("%Y-%n-%d %H:%M:%S")

def refund_course(tool_context: ToolContext) -> dict:
    # 1. RETRIEVE the current list from the state
    # It gets the purchased_courses list, defaulting to an empty list if not found.
    current_purchased_course = tool_context.state.get("purchased_courses", [])
    print(f"Purchases BEFORE Refund: {current_purchased_course}")

    # 2. PERFORM the removal using a List Comprehension
    # This creates a NEW list containing only courses whose ID DOES NOT match the requested_course_id.
    updated_course_list = [
        course
        for course in current_purchased_course
        if course["id"] != refund_course_id
    ]

    # 3. SAVE the updated list back to the state
    # This permanently overwrites the old list with the new, shorter one.
    tool_context.state["purchased_courses"] = updated_course_list
    print(f"Purchases AFTER Refund: {tool_context.state.get('purchased_courses')}")

    # TODO: Update intersection history as well

    return {
        "status": "success",
        "message": "Successfully removed the AI marketing platform course",
        "course_id": refund_course_id,
        "timestamp": current_time
    }