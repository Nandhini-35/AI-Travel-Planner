import urllib.request
import urllib.parse
import json

def test_server():
    base_url = "http://127.0.0.1:5000"
    
    # Test 1: Home Page
    try:
        with urllib.request.urlopen(base_url) as response:
            html = response.read().decode('utf-8')
            if "AI Travel Planner" in html:
                print("SUCCESS: Home page loaded.")
            else:
                print("FAILURE: Home page loaded but title missing.")
    except Exception as e:
        print(f"FAILURE: Could not load home page. {e}")
        return

    # Test 2: Recommendation (POST) - Valid
    try:
        data = urllib.parse.urlencode({
            'city': 'Delhi',
            'type': 'Temple',
            'budget': '100',
            'travelers': '1'
        }).encode()
        req = urllib.request.Request(f"{base_url}/recommend", data=data)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            if "Your Itinerary" in html:
                print("SUCCESS: Recommendation page loaded.")
                if "Why this?" in html:
                    print("SUCCESS: XAI Explanation found.")
            else:
                print("FAILURE: Recommendation page content unexpected.")
    except Exception as e:
        print(f"FAILURE: POST /recommend failed. {e}")

    # Test 3: Recommendation (POST) - Plan B
    try:
        data = urllib.parse.urlencode({
            'city': 'Mumbai',
            'type': 'Amusement Park',
            'budget': '10',
            'travelers': '1'
        }).encode()
        req = urllib.request.Request(f"{base_url}/recommend", data=data)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            if "Intelligent Adjustment" in html:
                print("SUCCESS: Plan-B Alert found.")
            else:
                print("FAILURE: Plan-B Alert NOT found.")
    except Exception as e:
        print(f"FAILURE: POST /recommend (Plan B) failed. {e}")

if __name__ == "__main__":
    test_server()
