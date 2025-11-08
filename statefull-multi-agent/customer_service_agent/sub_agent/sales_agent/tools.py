from google.adk.tools import ToolContext
from datetime import datetime


def purchase_course(tool_context: ToolContext) -> dict:
    course_id = "ai_marketing_platform"
    current_time = datetime.now().strftime("%Y-%n-%d %H:%M:%S")

    # Get current course
    current_purchased_course = tool_context.state.get("purchased_courses", [])

    # Check if user already owns the course
    course_ids = [
        course["id"] for course in current_purchased_course
    ]

    if course_id in course_ids:
        return {
            "status": "error",
            "message": "You already own this course"
        }

    current_purchased_course.append({"id": course_id, "purchase_date": current_time})

    # Update the state
    tool_context.state["purchased_courses"] = current_purchased_course

    # TODO: Update intersection history as well

    return {
        "status": "success",
        "message": "Successfully purchased the AI marketing platform course",
        "course_id": course_id,
        "timestamp": current_time
    }