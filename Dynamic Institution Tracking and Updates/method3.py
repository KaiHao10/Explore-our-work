import requests
import pandas as pd

API_KEY = "Sorry but we cannot show this"
CX = "and this"

def get_det_page(university_domain, program_type):
    # Define search query for each program type
    queries = {
        "undergraduate": f'site:{university_domain} "Duolingo English Test" OR "DET score" OR "English proficiency" undergraduate OR bachelor',
        "graduate": f'site:{university_domain} "Duolingo English Test" OR "DET score" OR "English proficiency" graduate OR master OR PhD',
        "other": f'site:{university_domain} "Duolingo English Test" OR "DET score" OR "English proficiency" "summer school" OR "exchange program"'
    }
    
    url = f"https://www.googleapis.com/customsearch/v1?q={queries[program_type]}&key={API_KEY}&cx={CX}"
    response = requests.get(url)
    results = response.json()

    if "items" in results:
        return results["items"][0]["link"]  # Get the first search result URL
    else:
        return None  # No result found

def get_contact_page(university_domain):
    query = f'site:{university_domain} "contact us" OR "admissions contact" OR "email"'
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CX}"
    response = requests.get(url)
    results = response.json()

    if "items" in results:
        return results["items"][0]["link"]  # Get the first search result URL
    else:
        return None  # No result found

# Load university domains
df = pd.read_csv('test_version.csv') 

# Check DET acceptance for each category
df["det_undergraduate"] = df["domains"].apply(lambda x: get_det_page(x, "undergraduate"))
df["det_graduate"] = df["domains"].apply(lambda x: get_det_page(x, "graduate"))
df["det_other"] = df["domains"].apply(lambda x: get_det_page(x, "other"))

# Check contact pages
df["contact_page"] = df["domains"].apply(lambda x: get_contact_page(x))

# Save results
df.to_csv("universities_with_det_info.csv", index=False)

print("DET requirement URLs and contact pages saved in universities_with_det_info.csv")
