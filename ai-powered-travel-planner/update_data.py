import pandas as pd

def update_dataset():
    input_path = r'c:\Users\m tamil\OneDrive\Desktop\AI-travel-planner\ai-powered-travel-planner\data\Top Indian Places to Visit 1.csv'
    output_path = r'c:\Users\m tamil\OneDrive\Desktop\AI-travel-planner\ai-powered-travel-planner\data\Top Indian Places to Visit 1.csv'

    import os
    print(f"Checking path: {input_path}")
    print(f"Exists: {os.path.exists(input_path)}")

    try:
        df = pd.read_csv(input_path)
        # Normalize columns
        df.columns = df.columns.str.strip()

        # Define Budget Map
        # Metros: 1500-1800
        # Tourist Hubs: 1200-1500
        # Smaller: 800-1000
        
        # Default fallback
        default_budget = 1000
        
        city_budgets = {
            'Delhi': 1600, 'New Delhi': 1600, 'Mumbai': 2000, 
            'Bangalore': 1500, 'Bengaluru': 1500, 'Kolkata': 1400, 
            'Chennai': 1200, 'Hyderabad': 1300, 'Pune': 1400, 'Ahmedabad': 1300,
            
            'Goa': 1800, 'Jaipur': 1400, 'Udaipur': 1500, 'Agra': 1300,
            'Varanasi': 1000, 'Rishikesh': 1200, 'Manali': 1400, 'Shimla': 1400,
            'Munnar': 1400, 'Ooty': 1400, 'Coorg': 1400, 'Darjeeling': 1300,
            'Gangtok': 1300, 'Leh': 1800, 'Srinagar': 1600, 'Port Blair': 2000,
            
            'Madurai': 900, 'Mysore': 1100, 'Hampi': 1000, 'Amritsar': 1100,
            'Puducherry': 1500, 'Mahabalipuram': 1200, 'Kanyakumari': 1000,
            'Rameswaram': 1000, 'Tirunelveli': 900, 'Thanjavur': 900,
            'Visakhapatnam': 1100, 'Vijayawada': 1000, 'Bhubaneswar': 1000,
            'Puri': 1100, 'Guwahati': 1100
        }

        def get_budget(city):
            # Normalize city name search
            for key, val in city_budgets.items():
                if key.lower() == str(city).lower():
                    return val
            return default_budget

        df['avg_budget'] = df['City'].apply(get_budget)

        df.to_csv(output_path, index=False)
        print(f"Dataset updated successfully with avg_budget column. Saved to {output_path}")
        print(df[['City', 'avg_budget']].head(10))

    except Exception as e:
        print(f"Error updating dataset: {repr(e)}")

if __name__ == "__main__":
    update_dataset()
