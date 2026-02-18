import os
import csv
from datetime import datetime
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def save_lead(name, email, intent, score):
    file_exists = os.path.isfile('travel_leads.csv')
    with open('travel_leads.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Date', 'Name', 'Email', 'Intent', 'Category'])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), name, email, intent, score])

def analyze_intent(user_query):
    """Categorizes lead as Corporate or Leisure based on keywords."""
    corporate_keywords = ['meeting', 'conference', 'office', 'work', 'project', 'client', 'business']
    query_lower = user_query.lower()
    
    if any(word in query_lower for word in corporate_keywords):
        return "CORPORATE"
    return "LEISURE"

def get_travel_advice(user_query, category):
    # Adjust the personality based on the lead type
    if category == "CORPORATE":
        system_msg = "You are a Senior Corporate Travel Manager. Focus on business hotels, fast Wi-Fi, proximity to airports, and quiet work environments."
    else:
        system_msg = "You are a Luxury Leisure Concierge. Focus on unique experiences, hidden gems, and relaxation."

    response = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=800,
        system=system_msg,
        messages=[{"role": "user", "content": user_query}]
    )
    return response.content[0].text

if __name__ == "__main__":
    print("--- 2026 Travel AI Lead Capture ---")
    u_name = input("Name: ")
    u_email = input("Email: ")
    u_intent = input("What's your trip about? ")

    # 1. AI categorizes the lead
    lead_category = analyze_intent(u_intent)
    
    # 2. Save with the new 'Category' column
    save_lead(u_name, u_email, u_intent, lead_category)
    
    # 3. Get tailored advice
    print(f"\n[Detected Type: {lead_category}] Thinking...")
    itinerary = get_travel_advice(u_intent, lead_category)
    print(f"\n{itinerary}")