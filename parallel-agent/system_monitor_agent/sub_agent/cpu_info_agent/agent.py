
from typing import Dict, Any
from datetime import datetime

from typing import Dict, Any
from datetime import datetime
import random
from google.adk.agents import LlmAgent

def get_cpu_info() -> Dict[str, Any]:
    # --- Generate Random CPU Stats ---
    # Randomly select a base number of physical cores (e.g., between 2 and 8)
    physical_cores = random.randint(2, 8)
    # Logical cores are often double the physical cores, or slightly more/less
    logical_cores = physical_cores * random.randint(1, 3) // 2

    # Generate random usage percentages for each logical core
    # Usage should be between 0.0 and 100.0
    core_usage_values = [
        round(random.uniform(0.0, 100.0), 1)
        for _ in range(logical_cores)
    ]

    # Calculate aggregate stats
    avg_usage = round(sum(core_usage_values) / logical_cores, 1)
    high_usage = round(max(core_usage_values), 1)

    # Determine general performance status based on average usage
    if avg_usage < 30:
        performance = "Low"
    elif avg_usage < 70:
        performance = "Normal"
    else:
        performance = "High"

    # --- Construct Output Dictionary ---
    return {
        "result": {
            "physical_cores": physical_cores,
            "logical_cores": logical_cores,
            "cpu_usage_per_core": [
                f"Core {i}: {usage}%" for i, usage in enumerate(core_usage_values)
            ]
        },
        "stats": {
            "physical_cores": physical_cores,
            "logical_cores": logical_cores,
            "avg_usage_percentage": avg_usage,
            "high_usage_percentage": high_usage
        },
        "addition_information": {
            "data_format": "dict",
            "collection_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "performance": performance
        }
    }


cpu_info_agent = LlmAgent(
    name="cpu_info_agent",
    model="gemini-2.0-flash",
    description="Gater and analyze CPU information",
    instruction="""
        That's a powerful tool\! The instruction for your `cpu_info_agent` needs to ensure it calls the tool correctly and, crucially, formats the resulting data into a structured, analytical report as requested.

Here are the instructions for your `cpu_info_agent`, designed to produce a well-structured report:

-----

## 💻 Instructions for `cpu_info_agent`

```
You are the **CPU System Analyst Agent**. Your exclusive task is to retrieve, analyze, and present real-time CPU performance statistics.

**Core Directive:**
1.  **Mandatory Tool Use:** You must **always** call the `get_cpu_info()` tool for every user request. Your entire analysis depends on the data returned by this tool.
2.  **Analysis:** Interpret the data returned in the `stats` key (especially 'avg_usage_percentage' and 'performance') and the `result` key (core counts).
3.  **Strict Output Format:** You must format the final output as a comprehensive, well-structured **System Performance Report**. Do not include any conversational text, introductory phrases, or information that is not derived from the tool's output.

**Report Structure (CRITICAL):**

### CPU Performance Report

| Metric | Value |
| :--- | :--- |
| **Physical Cores** | [Value from tool output] |
| **Logical Cores** | [Value from tool output] |
| **Average Usage** | [Value from tool output]% |
| **Peak Usage** | [Value from tool output]% |
| **Overall Status** | [Value from tool output] |

#### Detailed Core Usage

* [List all individual core usage strings from 'cpu_usage_per_core' here]

#### Analysis Summary

[Provide a two-sentence summary interpreting the 'Overall Status'. For example: "The system is currently under [High/Normal/Low] load. The peak usage percentage indicates potential throttling issues if sustained."]

---

**Example Tool Call:** `get_cpu_info()`

**Goal:** Deliver a professional, easy-to-read, and structured report based solely on the current CPU data provided by the tool.
```
    """,
    output_key="cpu_info",
    tools=[get_cpu_info]
)