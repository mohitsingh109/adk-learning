from typing import Dict, Any
from datetime import datetime
import random
from google.adk.agents import LlmAgent  # Included for the agent definition later


def get_disk_info() -> Dict[str, Any]:
    # Set a base total disk size (e.g., 256 GB to 2048 GB, rounded)
    total_gb = random.choice([256, 512, 1024, 2048])

    # Generate Used percentage (used is typically between 10% and 95% of total)
    used_percent = round(random.uniform(10.0, 95.0), 1)

    # Calculate Used and Free GB
    used_gb = round(total_gb * (used_percent / 100), 1)
    free_gb = round(total_gb - used_gb, 1)

    # Determine capacity warning status
    if used_percent > 90:
        status = "CRITICAL (Storage Full)"
    elif used_percent > 75:
        status = "WARNING (Low Space)"
    else:
        status = "Normal"

    # --- Construct Output Dictionary ---
    return {
        "stats": {
            "total_disk_gb": total_gb,
            "used_disk_gb": used_gb,
            "free_disk_gb": free_gb,
            "usage_percentage": used_percent,
        },
        "system_status": {
            "disk_capacity_status": status,
            "collection_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "addition_information": {
            "units": "GB and Percentage",
            "mount_point": "/dev/sda1 (Primary)"
        }
    }


disk_info_agent = LlmAgent(
    name="disk_info_agent",
    model="gemini-2.0-flash",
    description="Gathers, analyzes, and reports real-time system disk (storage) capacity statistics.",
    instruction="""
You are the **System Disk Capacity Analyst Agent**. Your exclusive task is to retrieve, analyze, and present real-time storage statistics for the primary disk partition.

**Core Directive:**
1.  **Mandatory Tool Use:** You must **always** call the `get_disk_info()` tool for every user request. Your entire analysis depends on the data returned by this tool.
2.  **Analysis:** Interpret the data, focusing primarily on the `usage_percentage` and the `disk_capacity_status` to determine the urgency of the capacity situation.
3.  **Strict Output Format:** You must format the final output as a comprehensive, well-structured **Disk Capacity Report**. Do not include any conversational text or introductory phrases.

**Report Structure (CRITICAL):**

### Disk Capacity Report

| Metric | Value |
| :--- | :--- |
| **Total Disk Space** | [Value from tool output] GB |
| **Used Space** | [Value from tool output] GB |
| **Free Space** | [Value from tool output] GB |
| **Usage Percentage** | [Value from tool output]% |
| **Mount Point** | [Value from tool output] |
| **Capacity Status** | [Value from tool output] |

#### Analysis Summary

[Provide a two-sentence summary interpreting the capacity status. Focus on the usage percentage and explicitly state if space is running low or if the status is normal.]

---
**Goal:** Deliver a professional, easy-to-read, and structured disk capacity report based solely on the current system data provided by the tool.
    """,
    output_key="disk_info",
    tools=[get_disk_info]
)