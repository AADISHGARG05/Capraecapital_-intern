# importing some libraries
# Code By: Aadish Garg
# Internship Project Submission
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from urllib.parse import urlparse, urljoin
from googlesearch import search

# Function to extract emails from a single page
def extract_emails_from_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        emails = set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", soup.get_text())) # here i am using the re module of python of findimg emails.
        return emails
    except:
        return set()

# Function to find the contact details of he company
def find_contact_pages(base_url):
    possible_paths = ["/contact", "/about", "/team"]
    contact_urls = []
    for path in possible_paths:
        full_url = urljoin(base_url, path)
        contact_urls.append(full_url)
    return contact_urls

# Function to scrape  the emails from a domain on internet
def scrape_emails_from_domain(domain):
    all_emails = set()
    contact_pages = find_contact_pages(domain)
    for page in contact_pages:
        emails = extract_emails_from_url(page)
        all_emails.update(emails)
    return all_emails

# Main function to run the tool
def generate_leads(query, num_results=10):
    print(f"Searching for top {num_results} sites for query: {query}\n")
    leads = []
    for url in search(query, num_results=num_results):
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        emails = scrape_emails_from_domain(base_url)
        for email in emails:
            if not email.endswith(('png', 'jpg', 'jpeg')):
                leads.append({"company_url": base_url, "email": email})


    df = pd.DataFrame(leads).drop_duplicates()
    df.to_csv("leads.csv", index=False)
    print(f"\n Done! Results saved to 'leads.csv'.")

# Taking your input for excecution
if __name__ == "__main__":
    search_query = input("Enter your generation query: ")
    generate_leads(search_query)
