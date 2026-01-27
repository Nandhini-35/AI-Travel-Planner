# AI Powered Travel Planner

##  Project Concept

The AI Powered Travel Planner is a backend-driven intelligent system that helps users plan trips based on **budget, number of days, number of travelers, and interest type**.  
Instead of manually selecting places, the system uses **AI reasoning and planning logic** to recommend feasible places, generate day-wise itineraries, explain its decisions, and suggest the best travel mode.

This project focuses on **AI logic and decision-making**, not just UI filtering or ML model training.



##  What This Project Does

- Recommends tourist places within the **total trip budget**
- Calculates **stay + food + entry fee cost**
- Ensures recommendations satisfy **budget and time constraints**
- Generates **multi-day travel plans**
- Explains **why each place is recommended**
- Suggests **best travel mode** based on distance and group size
- Provides **map visualization** and alternative recommendations



##  Core AI Ideas Used

- Constraint Satisfaction AI: Filtering places based on strict budget/time limits.
- Planning & Optimization AI: Greedy algorithm for itinerary generation.
- Explainable AI (XAI): Rule-based natural language generation for "Why this place?".
- Content-Based Recommender System: Recommending similar places based on user interest.
- Reasoning AI (Plan-B logic): Automatically relaxing constraints if no exact matches are found.
- LLM Integration: Natural Language Generation via OpenRouter API.

##  Overall Workflow (Step-by-Step)

1. User enters:
   - City
   - Interest type
   - Total trip budget
   - Number of travelers
   - Number of days

2. System reads place data from the dataset.

3. The system calculates:
   - Stay + food cost using `avg_budget`
   - Entry fee cost for places
   - Total estimated trip cost

4. AI filters places using constraints:
   - City must match
   - Type must match
   - TotalTripCost ≤ UserBudget

5. If no places are found:
   - Budget is slightly relaxed
   - Related place types are tried
   - System explains the compromise (Plan-B reasoning)

6. For valid places:
   - Places are sorted by rating
   - A greedy algorithm creates a day-wise itinerary
   - Daily visit time limits are respected

7. Each place includes:
   - A “Why this place?” explanation (XAI)
   - Similar place suggestions (Recommender AI)

8. User provides starting location:
   - Distance is calculated
   - Best travel mode is suggested using rule-based AI

9. Final output includes:
   - Recommended places
   - Cost breakdown
   - Day-wise itinerary
   - Travel mode suggestion
   - Map route
   - Human-readable summary

## Project File Structure
```
AI-Powered-Travel-Planner/
│
├── app.py                         # Flask application entry point
│                                  # Handles routes, requests, and responses
│
├── travel_planner.py              # Core AI logic
│                                  # Budget calculation, place filtering,
│                                  # planning, reasoning, XAI, recommender logic
│
├── update_data.py                 # Dataset preprocessing and enrichment
│                                  # Adds avg_daily_cost_per_person and cleans data
│
├── Top Indian Places to Visit 1.csv
│                                  # Main dataset containing places, costs,
│                                  # visit time, ratings, and city information
│
├── templates/                     # HTML templates
│   ├── index.html                 # User input page
│   ├── results.html               # Recommendations and itinerary page
│   ├── explore.html               # Show all places in a selected city
│   └── map_view.html              # Map view and route visualization
│
├── static/                        # Static assets
│   └── style.css                  # Styling for all pages
│
├── tests/                         # Test files for validation
│   ├── test_logic.py              # Tests AI filtering and planning logic
│   ├── test_cost.py               # Tests budget and cost calculations
│   └── test_distance.py           # Tests distance and travel mode logic
│
├── requirements.txt               # Python dependencies
│
├── Screenshot *.png               # Output screenshots and UI results
│
└── README.md                      # Project documentation
```
## Installation & Deployment

Local Setup
1. Clone the repo and install dependencies:
      pip install -r requirements.txt
2. Create a.env file and add your key:
      env
      OPENROUTER_API_KEY=your_key_here
3. Run the app:
      python app.py
## Render Deployment
This project is pre-configured for Render. Simply connect your GitHub repository, add your OPENROUTER_API_KEY in the Environment tab, and set the Root Directory to ai-powered-travel-planner.

## Output 
<img width="1890" height="911" alt="Screenshot 2026-01-27 154001" src="https://github.com/user-attachments/assets/b86d020f-7614-4006-952d-d7dd4d9f4250" />
<img width="1887" height="907" alt="Screenshot 2026-01-27 154051" src="https://github.com/user-attachments/assets/3d5b77e3-3c25-4a94-bf1c-cb3b9bf56bad" />
<img width="1905" height="913" alt="Screenshot 2026-01-27 154155" src="https://github.com/user-attachments/assets/5fdfd90a-48db-4b24-a143-829e673c82b7" />
<img width="1885" height="912" alt="Screenshot 2026-01-27 154525" src="https://github.com/user-attachments/assets/c860a8a8-8821-4441-912e-1de19ecf1662" />




