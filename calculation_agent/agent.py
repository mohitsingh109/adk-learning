from google.adk.agents import Agent
from google.adk.tools import google_search


def calculate_share_value(price: float, units: int) -> float:
  """
  Calculates the total monetary value of a stock or asset investment.

  The share value is calculated by multiplying the price per unit 
  (e.g., price per share) by the total number of units held.

  Args:
    price (float): The price of a single unit (e.g., price per share). 
                   Must be a positive number.
    units (int): The total number of units held (e.g., number of shares).
                 Must be a non-negative integer.

  Returns:
    float: The total market value of the investment.

  Raises:
    ValueError: If price is not positive or units is negative.
  """
  # 1. Basic input validation
  if price <= 0:
    raise ValueError("Price per unit must be a positive number.")
  if units < 0:
    raise ValueError("Number of units cannot be negative.")

  # 2. Calculation
  total_value = price * units

  # 3. Return the calculated value
  return total_value


root_agent = Agent(
    name="calculation_agent",
    model="gemini-2.0-flash",
    description="An agent specialized in calculating the total value of investment shares or units.",
    instruction=""" You are a precise Financial Calculation Specialist. Your sole purpose is to 
    perform highly accurate investment value calculations. Your primary and mandatory responsibility is to use
    the 'calculate_share_value' tool whenever the user provides a price and a quantity of units (shares) 
    and asks for the total value. Do not attempt to calculate the value yourself; always delegate the task
    to the tool. Respond with the calculated total value clearly and concisely, using appropriate currency 
    formatting.""",
    tools=[calculate_share_value]
)