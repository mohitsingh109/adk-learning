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


