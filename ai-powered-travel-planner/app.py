from flask import Flask, render_template, request, jsonify
from travel_planner import TravelPlanner
import random

app = Flask(__name__)
planner = TravelPlanner()

@app.route('/')
def planner_form():
    cities = planner.get_unique_cities()
    types = planner.get_unique_types()
    return render_template('index.html', cities=cities, types=types)

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        # Get form data
        city = request.form.get('city')
        interest_type = request.form.get('type')
        try:
            budget = float(request.form.get('budget'))
        except (ValueError, TypeError):
            budget = 0
            
        travelers = int(request.form.get('travelers', 1))
        days = int(request.form.get('days', 1))
        starting_city = request.form.get('starting_city') 

        # 1. Mandatory Filtering & Cost Calc (Now includes Lat/Long)
        results, base_cost, avg_budget = planner.filter_places(city, interest_type, budget, travelers, days)
        plan_b_message = None

        # 2. Plan-B Logic
        if results.empty:
            results, plan_b_message, base_cost = planner.plan_b_search(city, interest_type, budget, travelers, days)
        
        # Step 9: Journey Mode Suggestion
        journey_details = planner.calculate_journey_details(starting_city, city, travelers)

        recommendations = []
        
        # Prepare recommendations list (used for display list + map)
        if not results.empty:
            for _, row in results.iterrows():
                # Simulate Distance
                dist_km = round(random.uniform(1.0, 15.0), 1)
                mode, cost_est = planner.suggest_travel_mode(dist_km, travelers)
                explanation = planner.generate_explanation(row, budget, base_cost)
                similar = planner.find_similar_places(row['place'], row['City'], row['type'])

                recommendations.append({
                    'place': row['place'],
                    'type': row['type'],
                    'rating': row['ratings'],
                    'fee': row['Entrance Fee in INR'],
                    'time_needed': row['time needed to visit in hrs'],
                    'explanation': explanation,
                    'distance': dist_km,
                    'travel_mode': mode,
                    'travel_cost': cost_est,
                    'similar_places': similar,
                    'est_total_cost': row.get('est_total_cost', 0),
                    'lat': row.get('lat', 0),
                    'lng': row.get('lng', 0)
                })

        # 3. Generate Itinerary (Scheduling) - Greedily Sorted
        itinerary, budget_exhausted = planner.generate_itinerary(results, days, budget, base_cost, travelers)
        
        # 4. Calculate Final Actual Cost of Itinerary
        entry_fees_total = 0
        scheduled_places_count = 0
        
        for day, places in itinerary.items():
            if isinstance(places, list):
                for p in places:
                    entry_fees_total += (p['Entrance Fee in INR'] * travelers)
                    scheduled_places_count += 1
                
        total_trip_cost = base_cost + entry_fees_total
        
        cost_breakdown = {
            'stay_food': int(base_cost),
            'entry_fees': int(entry_fees_total),
            'total': int(total_trip_cost),
            'avg_budget_per_person': avg_budget,
            'budget_exhausted': budget_exhausted # Still pass flag for top-level warning if needed
        }

        # 5. LLM Summary
        trip_summary = planner.generate_trip_summary(results.to_dict('records')[:5], cost_breakdown)

        return render_template('results.html', 
                               recommendations=recommendations, 
                               city=city, 
                               plan_b_message=plan_b_message,
                               trip_summary=trip_summary,
                               itinerary=itinerary,
                               cost_breakdown=cost_breakdown,
                               days=days,
                               travelers=travelers,
                budget=budget,
                interest_type=interest_type,
                               journey_details=journey_details)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return render_template('error.html', error=str(e))

@app.route('/map', methods=['POST'])
def view_map():
    try:
        # Get form data from results page
        city = request.form.get('city')
        interest_type = request.form.get('type')
        budget = float(request.form.get('budget', 0))
        travelers = int(request.form.get('travelers', 1))
        days = int(request.form.get('days', 1))
        starting_city = request.form.get('starting_city')

        # Re-run logic to get the same data (efficient enough for OSM/Mock data)
        results, base_cost, avg_budget = planner.filter_places(city, interest_type, budget, travelers, days)
        if results.empty:
            results, _, base_cost = planner.plan_b_search(city, interest_type, budget, travelers, days)

        journey_details = planner.calculate_journey_details(starting_city, city, travelers)
        
        recommendations = []
        if not results.empty:
            for _, row in results.iterrows():
                explanation = planner.generate_explanation(row, budget, base_cost)
                recommendations.append({
                    'place': row['place'],
                    'type': row['type'],
                    'rating': row['ratings'],
                    'explanation': explanation,
                    'lat': row.get('lat', 0),
                    'lng': row.get('lng', 0)
                })

        itinerary, _ = planner.generate_itinerary(results, days, budget, base_cost, travelers)

        return render_template('map_view.html',
                               city=city,
                               interest_type=interest_type,
                               budget=budget,
                               days=days,
                               travelers=travelers,
                               itinerary=itinerary,
                               recommendations=recommendations,
                               journey_details=journey_details)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/explore/<city>')
def explore(city):
    # Show More Page - Show all places for a city
    mask = (planner.df['City'].str.lower() == city.lower())
    all_places = planner.df[mask].to_dict('records')
    return render_template('explore.html', city=city, places=all_places)

if __name__ == '__main__':
    app.run(debug=True)
