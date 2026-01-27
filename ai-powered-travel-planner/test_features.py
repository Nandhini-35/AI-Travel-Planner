import urllib.request
import urllib.parse

def test_features():
    base_url = "http://127.0.0.1:5000/recommend"
    
    # Test Case: Start Chennai, Dest Bangalore (Inter-city), 4 Pax
    data = urllib.parse.urlencode({
        'starting_city': 'Chennai',
        'city': 'Bangalore',
        'type': 'Park', # Cubbon Park etc
        'budget': '10000',
        'travelers': '4',
        'days': '1'
    }).encode()
    
    try:
        req = urllib.request.Request(base_url, data=data)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
            # Print for Debug if needed
            # print(html)

            # Check Journey Mode
            if "Chennai" in html and "Bangalore" in html and "Train/Bus" in html:
                print("SUCCESS: Journey Mode (Chennai -> Bangalore) = Train/Bus.")
            elif "Cab" in html:
                print("PARTIAL: Journey Mode found but might be Cab (Check logic).")
            else:
                print("FAILURE: Journey Mode text not found.")

            # Check Cost Breakdown existence
            if "Stay + Food + Travel" in html:
                print("SUCCESS: Cost Breakdown Visible.")
            else:
                 print("FAILURE: Cost Breakdown Missing.")

    except Exception as e:
        print(f"FAILURE: Request failed. {e}")

if __name__ == "__main__":
    test_features()
