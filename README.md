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

- Constraint Satisfaction AI  
- Planning & Optimization AI  
- Rule-Based Decision Making  
- Explainable AI (XAI)  
- Content-Based Recommender System  
- Reasoning AI (Plan-B logic)  
- API-assisted Geo Reasoning  
- Optional LLM-based Natural Language Generation  

---

##  Overall Workflow (Step-by-Step)

1. User enters:
   - City
   - Interest type
   - Total trip budget
   - Number of travelers
   - Number of days

2. System reads place data from the dataset.

3. The system calculates:
   - Stay + food cost using `avg_daily_cost_per_person`
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

