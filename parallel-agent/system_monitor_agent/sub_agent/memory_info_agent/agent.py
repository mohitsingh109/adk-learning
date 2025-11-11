from typing import Dict, Any
from datetime import datetime
import random
from google.adk.agents import LlmAgent  # Included for the agent definition later


def get_memory_info() -> Dict[str, Any]:
    # Set a base total RAM size (e.g., 8 GB to 64 GB)
    total_gb = random.choice([8, 16, 32, 64])
    total_bytes = total_gb * (1024 ** 3)  # Convert GB to Bytes for detail

    # Generate Used and Available RAM (used is typically between 20% and 90% of total)
    used_percent = round(random.uniform(20.0, 90.0), 1)
    used_bytes = int(total_bytes * (used_percent / 100))
    available_bytes = total_bytes - used_bytes

    # Generate Swap usage (swap is often low unless RAM is heavily utilized)
    swap_total_gb = total_gb // 2  # Example: Swap is half of RAM
    swap_used_percent = round(random.uniform(0.0, 50.0), 1)

    # Determine memory pressure status
    if used_percent > 85:
        status = "Critical (High Pressure)"
    elif used_percent > 60:
        status = "High (Normal Pressure)"
    else:
        status = "Normal (Low Pressure)"

    # --- Construct Output Dictionary ---
    return {
        "stats": {
            "total_ram_gb": total_gb,
            "used_ram_gb": round(used_bytes / (1024 ** 3), 1),
            "available_ram_gb": round(available_bytes / (1024 ** 3), 1),
            "used_percentage": used_percent,
            "swap_total_gb": swap_total_gb,
            "swap_used_percentage": swap_used_percent
        },
        "system_status": {
            "memory_pressure": status,
            "collection_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "addition_information": {
            "units": "GB and Percentage",
            "details": f"{total_bytes} total bytes of RAM detected."
        }
    }

memory_info_agent = LlmAgent(
    name="memory_info_agent",
    model="gemini-2.0-flash",
    description="Gathers, analyzes, and reports real-time system memory (RAM and Swap) statistics.",
    instruction="""
You are the **System Memory Analyst Agent**. Your exclusive task is to retrieve, analyze, and present real-time system memory statistics.

**Core Directive:**
1.  **Mandatory Tool Use:** You must **always** call the `get_memory_info()` tool for every user request. Your entire analysis depends on the data returned by this tool.
2.  **Analysis:** Interpret the data, focusing on the `used_percentage` and the `memory_pressure` status to provide a clear summary.
3.  **Strict Output Format:** You must format the final output as a comprehensive, well-structured **Memory Performance Report**. Do not include any conversational text or introductory phrases.

**Report Structure (CRITICAL):**

### Memory Performance Report

| Metric | Value |
| :--- | :--- |
| **Total RAM** | [Value from tool output] GB |
| **Used RAM** | [Value from tool output] GB |
| **Available RAM** | [Value from tool output] GB |
| **Usage Percentage** | [Value from tool output]% |
| **Swap Used** | [Value from tool output]% of Total Swap |
| **System Status** | [Value from tool output] |

#### Analysis Summary

[Provide a two-sentence summary interpreting the memory status. Focus on whether the system is under pressure and if the swap file is being heavily utilized.]

---
**Goal:** Deliver a professional, easy-to-read, and structured memory report based solely on the current system data provided by the tool.
    """,
    output_key="memory_info",
    tools=[get_memory_info]
)