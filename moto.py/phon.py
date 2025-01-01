import requests

def google_custom_search(query, api_key, cx):
    url = "https://www.googleapis.com/customsearch/v1"
    
    # Set up the parameters for the API request
    params = {
        'q': query,  # The search query
        'key': api_key,  # Your API key
        'cx': cx  # Your Custom Search Engine ID (CSE ID)
    }
    
    # Make the GET request to the Google Custom Search API
    response = requests.get(url, params=params)
    
    # Check if the response was successful (status code 200)
    if response.status_code == 200:
        data = response.json()  # Parse the response JSON
        
        # Extract search result links
        search_results = []
        for item in data.get('items', []):
            search_results.append(item['link'])
        
        return search_results
    else:
        print("Error:", response.status_code)
        return []

# Example usage
api_key = "YOUR_GOOGLE_API_KEY"  # Replace with your API key
cx = "<script async src="https://cse.google.com/cse.js?cx=072b7a1dbf73c4e66">
</script>
<div class="gcse-search"></div>"  # Replace with your Custom Search Engine ID (CSE ID)

# Perform a search query (e.g., "Artificial Intelligence")
results = google_custom_search("Artificial Intelligence", api_key, cx)

# Display the results
if results:
    for idx, link in enumerate(results):
        print(f"{idx + 1}: {link}")
else:
    print("No results found.")
