import pandas as pd
import numpy as np
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class TravelPlanner:
    def __init__(self, data_path='data/Top Indian Places to Visit 1.csv'):
        # Load dataset
        try:
            self.df = pd.read_csv(data_path)
            # Normalize column names for easier access
            self.df.columns = self.df.columns.str.strip()
            
            # --- START InMemory Data Enhancement ---
            # Map avg_budget since we couldn't write to file
            self._apply_avg_budget()
            # --- END InMemory Data Enhancement ---

            # OpenAI client for LLM
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("OPENROUTER_API_KEY"),
            )
            
        except Exception as e:
            print(f"Error loading data: {e}")
            self.df = pd.DataFrame()

    def _apply_avg_budget(self):
        # Heuristic Map
        city_budgets = {
            'Delhi': 1600, 'New Delhi': 1600, 'Mumbai': 2000, 
            'Bangalore': 1500, 'Bengaluru': 1500, 'Kolkata': 1400, 
            'Chennai': 1200, 'Hyderabad': 1300, 'Pune': 1400, 'Ahmedabad': 1300,
            'Goa': 1800, 'Jaipur': 1400, 'Udaipur': 1500, 'Agra': 1300,
            'Madurai': 900, 'Mysore': 1100, 'Hampi': 1000, 'Ooty': 1400
        }
        default_budget = 1000
        
        def get_budget(city):
            for key, val in city_budgets.items():
                if key.lower() == str(city).lower():
                    return val
            return default_budget
            
        if 'avg_budget' not in self.df.columns:
            self.df['avg_budget'] = self.df['City'].apply(get_budget)

    def get_unique_cities(self):
        if self.df.empty: return []
        return sorted(self.df['City'].unique().tolist())

    def get_unique_types(self):
        if self.df.empty: return []
        return sorted(self.df['type'].unique().tolist())

    def _generate_mock_coordinates(self, place_name, city):
        """
        Generates deterministic mock coordinates based on city center.
        Real production apps would usage Geocoding API.
        """
        # City Centers (Approx Lat, Long)
        city_coords = {
            'Delhi': (28.61, 77.20), 'Mumbai': (19.07, 72.87), 'Bangalore': (12.97, 77.59),
            'Chennai': (13.08, 80.27), 'Hyderabad': (17.38, 78.48), 'Kolkata': (22.57, 88.36),
            'Goa': (15.29, 74.12), 'Jaipur': (26.91, 75.78), 'Agra': (27.17, 78.00),
            'Madurai': (9.92, 78.11), 'Coimbatore': (11.01, 76.95), 'Ooty': (11.41, 76.69)
        }
        
        base = city_coords.get(city, (20.59, 78.96)) # Default to India center
        
        # Hash name to get consistent random offset
        h = hash(place_name)
        lat_offset = (h % 100) / 2000.0  # +/- 0.05 degrees approx 5km
        long_offset = ((h // 100) % 100) / 2000.0
        
        return base[0] + lat_offset, base[1] + long_offset

    def filter_places(self, city, interest_type, user_budget, members=1, days=1):
        """
        Refined Filtering Logic:
        1. Calculate Stay & Food Cost (Fixed per day).
        2. Filter only if UserBudget < StayFoodCost (Impossible trip).
        3. Do NOT strictly filter by Entry Fees here; let the Itinerary Generator do that dynamically.
        """
        if self.df.empty: return pd.DataFrame(), 0, 0

        # filter by city and type first
        mask = (
            (self.df['City'].str.lower() == city.lower()) &
            (self.df['type'].str.lower() == interest_type.lower())
        )
        filtered = self.df[mask].copy()
        
        if filtered.empty:
            return filtered, 0, 0

        # Calculate Base Cost (Stay + Food)
        avg_budget = filtered.iloc[0]['avg_budget']
        base_cost = avg_budget * members * days
        
        # Immediate Fail Check: If budget cannot even cover Stay+Food
        if base_cost > user_budget:
             return pd.DataFrame(), base_cost, avg_budget

        # For the candidates list, we still want to show "affordable" options.
        # So we filter places where "Entry Fee" is not insanely high (< Remaining Budget / 2 approx)
        # But we act leniently to show more options for the Map.
        remaining_budget = user_budget - base_cost
        
        filtered['est_total_cost'] = base_cost + (filtered['Entrance Fee in INR'] * members)
        
        # Strict check only on the individual place: Can I afford to enter THIS place?
        # We check if (Base + Entry) <= Budget to filter out expensive individual spots.
        feasible_mask = filtered['est_total_cost'] <= user_budget
        feasible_places = filtered[feasible_mask].copy()
        
        # Add Coordinates
        feasible_places['lat'], feasible_places['lng'] = zip(*feasible_places.apply(
            lambda x: self._generate_mock_coordinates(x['place'], x['City']), axis=1
        ))

        return feasible_places, base_cost, avg_budget

    def plan_b_search(self, city, interest_type, budget, members=1, days=1):
        """
        Plan-B: Constraint Relaxation
        """
        if self.df.empty: return pd.DataFrame(), "No data.", 0

        # Relaxation 1: Incremented Budget (+20%)
        relaxed_budget = budget * 1.20
        results, base_cost, _ = self.filter_places(city, interest_type, relaxed_budget, members, days)
        
        if not results.empty:
             return results, f"Budget too low. We found places by slightly increasing your budget to ₹{int(relaxed_budget)}.", base_cost

        # Relaxation 2: Same City, Any Type (within original budget)
        mask_city = (self.df['City'].str.lower() == city.lower())
        df_city = self.df[mask_city].copy()
        
        if not df_city.empty:
            avg_budget = df_city.iloc[0]['avg_budget']
            base_cost = avg_budget * members * days
            df_city['est_total_cost'] = base_cost + (df_city['Entrance Fee in INR'] * members)
            feasible = df_city[df_city['est_total_cost'] <= budget].copy()
            
            if not feasible.empty:
                feasible['lat'], feasible['lng'] = zip(*feasible.apply(
                    lambda x: self._generate_mock_coordinates(x['place'], x['City']), axis=1
                ))
                return feasible, f"No '{interest_type}' found in budget. Showing other affordable places in {city}.", base_cost

        return pd.DataFrame(), "No suitable places found even with adjustments.", 0

    def generate_explanation(self, row, user_budget, base_cost):
        """
        XAI: Generate specific reasons.
        """
        reasons = []
        cost = row['est_total_cost']
        
        if cost <= user_budget:
             reasons.append(f"Fits your ₹{user_budget} budget.")
        
        rating = row['ratings']
        if rating >= 4.5:
            reasons.append("Highly rated by visitors.")
            
        return " ".join(reasons)

    # City Coordinates (Lat, Lon)
    CITY_COORDS = {
        'Delhi': (28.6139, 77.2090), 'New Delhi': (28.6139, 77.2090), 
        'Mumbai': (19.0760, 72.8777), 'Bangalore': (12.9716, 77.5946), 'Bengaluru': (12.9716, 77.5946),
        'Chennai': (13.0827, 80.2707), 'Hyderabad': (17.3850, 78.4867), 'Kolkata': (22.5726, 88.3639),
        'Goa': (15.2993, 74.1240), 'Jaipur': (26.9124, 75.7873), 'Udaipur': (24.5854, 73.7125),
        'Agra': (27.1767, 78.0081), 'Madurai': (9.9252, 78.1198), 'Mysore': (12.2958, 76.6394),
        'Coimbatore': (11.0168, 76.9558), 'Ooty': (11.4102, 76.6950), 'Pune': (18.5204, 73.8567),
        'Ahmedabad': (23.0225, 72.5714), 'Hampi': (15.3350, 76.4600), 'Kerala': (10.8505, 76.2711)
    }

    def _haversine_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # Convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

        # Haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a)) 
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles
        return c * r

    def suggest_travel_mode(self, distance_km, travelers):
        # Legacy/Internal usage within city
        if distance_km < 2:
            return "Walk", "Free"
        elif 2 <= distance_km <= 10:
            return "Bike/Auto", f"₹{int(distance_km * 15)}"
        else:
            return "Cab", f"₹{int(distance_km * 25)}"

    def calculate_journey_details(self, start_city, dest_city, travelers):
        """
        Step 9: Distance-Based Travel Mode Suggestion (Inter-city or Commute)
        Uses Haversine formula for real distances.
        """
        if not start_city:
            return None
            
        start_city = start_city.strip().title()
        dest_city = dest_city.strip().title()
        
        distance = 0
        mode = "Cab"
        reason = ""
        
        if start_city.lower() == dest_city.lower():
            # Same city commute (Mock)
            distance = 12.5 # Average intra-city distance
            if distance <= 2:
                mode = "Walk"
                reason = "Short distance, healthy walk."
            elif distance <= 15:
                if travelers <= 2:
                     mode = "Bike/Auto"
                     reason = f"Economical for {travelers} travelers."
                else:
                     mode = "Cab"
                     reason = f"Comfortable for {travelers} travelers."
            else:
                mode = "Local Train/Metro"
                reason = "Best for long city commutes."
        else:
            # Different city travel - Real Haversine Distance
            coords_start = self.CITY_COORDS.get(start_city)
            coords_end = self.CITY_COORDS.get(dest_city)
            
            if coords_start and coords_end:
                distance = self._haversine_distance(coords_start[0], coords_start[1], coords_end[0], coords_end[1])
                distance = round(distance, 1)
            else:
                # Fallback if coordinates missing
                distance = 350 # Default mock
            
            # Mode Logic based on Real Distance
            if distance < 100:
                mode = "Car/Cab"
                reason = "Short inter-city drive."
            elif distance < 800:
                mode = "Train/Bus"
                if travelers > 3:
                     reason = f"Economical group travel for {distance}km."
                else:
                     reason = f"Best balance of cost and comfort."
            else:
                mode = "Flight"
                reason = f"Long distance ({distance}km), save time by flying."
                
        return {
            'start': start_city,
            'end': dest_city,
            'distance': distance,
            'mode': mode,
            'reason': reason
        }

    def find_similar_places(self, current_place_name, current_city, current_type):
        if self.df.empty: return []
        mask = (
            (self.df['place'] != current_place_name) & 
            (
                (self.df['City'] == current_city) | 
                (self.df['type'] == current_type)
            )
        )
        similar_df = self.df[mask].head(2)
        return similar_df.to_dict('records')

    def generate_trip_summary(self, places, cost_breakdown):
        """
        AI Reasoning: Generates a natural language summary using LLM.
        """
        try:
            place_names = ", ".join([p['place'] for p in places])
            prompt = f"""
            You are a helpful travel planner. Generate a short, enthusiastic trip summary for visiting the following places: {place_names}.
            The total estimated cost for the trip is ₹{cost_breakdown['total']}.
            Keep it under 3 sentences.
            """
            
            response = self.client.chat.completions.create(
                model="openai/gpt-3.5-turbo", # or any other preferred model on OpenRouter
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            # Fallback to rule-based summary
            place_names = ", ".join([p['place'] for p in places])
            return f"Trip Plan: Visit {len(places)} locations ({place_names}). Total Est. Cost: ₹{cost_breakdown['total']}."

    def generate_itinerary(self, places_df, days, user_budget, base_cost, members):
        """
        Step 6 Enhanced: Multi-Day Budget-Aware Itinerary Generation.
        - Fills 'days' loop 1 to N.
        - Checks remaining budget for entry fees.
        - If budget exhausted, marks subsequent days as 'BUDGET_EXHAUSTED'.
        """
        if places_df.empty: return {}, False
        
        # Greedy Sort: Best rated first
        places_df = places_df.sort_values(by='ratings', ascending=False)
        all_places = places_df.to_dict('records')
        
        itinerary = {}
        budget_exhausted = False
        remaining_budget_for_fees = user_budget - base_cost
        
        # Track used places to avoid repeats
        used_indices = set()

        # Calculate target places per day to distribute more evenly if we have many
        total_available = len(all_places)
        avg_places_per_day = max(2, int(np.ceil(total_available / days))) if days > 0 else 0

        for day_num in range(1, days + 1):
            day_label = f"Day {day_num}"
            
            if budget_exhausted:
                itinerary[day_label] = "BUDGET_EXHAUSTED"
                continue

            current_day_places = []
            hours_remaining = 8.0 # Increased from 6.0 to allow more places
            places_this_day = 0
            
            # Try to fill this day
            for i, place in enumerate(all_places):
                if i in used_indices:
                    continue
                    
                time_needed = place.get('time needed to visit in hrs', 2.0)
                if pd.isna(time_needed): time_needed = 2.0
                
                entry_cost = place['Entrance Fee in INR'] * members
                
                # Distribution logic: don't cram everything into Day 1 if we have multiple days
                if places_this_day >= avg_places_per_day and days > 1 and (total_available - len(used_indices)) > (days - day_num):
                    # If we already have enough for today and there are plenty left for future days, stop
                    break

                if time_needed <= hours_remaining:
                    if entry_cost <= remaining_budget_for_fees:
                        # Schedule it
                        current_day_places.append(place)
                        hours_remaining -= time_needed
                        remaining_budget_for_fees -= entry_cost
                        used_indices.add(i)
                        places_this_day += 1
                    else:
                        # Cannot afford this specific place
                        pass
                
                if hours_remaining <= 0.5 or places_this_day >= 4: # Max 4 places per day
                    break
            
            if current_day_places:
                itinerary[day_label] = current_day_places
            else:
                if remaining_budget_for_fees < 100:
                     budget_exhausted = True
                     itinerary[day_label] = "BUDGET_EXHAUSTED"
                else: 
                     itinerary[day_label] = [] # Empty day if no places left

        return itinerary, budget_exhausted
