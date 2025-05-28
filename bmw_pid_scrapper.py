#!/usr/bin/env python3
"""
Script to extract the "BMW Enhanced PID Data" table from a given URL and output it as CSV.
The script downloads the webpage, parses the HTML for the table, converts it to CSV,
saves the CSV file locally, and prints the CSV content to the console.
"""
import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse
import argparse

def fetch_page(url):
    """Fetch the HTML content from the given URL and return a BeautifulSoup object."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
    except requests.RequestException as e:
        # Any network-related errors or non-200 status codes will be caught here
        raise e  # Propagate exception to be handled by the caller
    # Parse the page content with BeautifulSoup
    return BeautifulSoup(response.text, 'html.parser')

def extract_pid_table(soup):
    """
    Locate and extract the 'BMW Enhanced PID Data' table from the BeautifulSoup object.
    Returns a pandas DataFrame of the table data.
    """
    # Find the heading for the Enhanced PID Data table (case-insensitive match)
    heading = soup.find(lambda tag: tag.name and "bmw enhanced pid data" in tag.get_text().lower())
    if not heading:
        raise ValueError("Table title 'BMW Enhanced PID Data' not found on the page.")
    # The table is expected to be the next HTML table after the heading
    table = heading.find_next("table")
    if not table:
        raise ValueError("No HTML table found following the 'BMW Enhanced PID Data' heading.")
    
    # Extract table header cells (assuming the first row contains headers)
    headers = [th.get_text().strip() for th in table.find_all('th')]
    data_rows = []
    # If no <th> elements were found, assume the first <tr> has the headers as <td>
    table_rows = table.find_all('tr')
    if not headers and table_rows:
        # Use first row as header if it's not marked with <th>
        first_cells = table_rows[0].find_all(['th', 'td'])
        headers = [cell.get_text().strip() for cell in first_cells]
        # The remaining rows are data
        data_rows = table_rows[1:]
    else:
        # If headers found, all rows after the first are data rows
        data_rows = table_rows[1:]
    
    # Extract data for each row
    records = []
    for row in data_rows:
        cells = [td.get_text().strip() for td in row.find_all('td')]
        if cells and len(cells) == len(headers):
            records.append(cells)
    if not records:
        raise ValueError("The table was found, but no data rows were extracted.")
    
    # Create a DataFrame from the extracted table data
    df = pd.DataFrame(records, columns=headers)
    return df

def main():
    # Parse command-line arguments for the URL input
    parser = argparse.ArgumentParser(description="Extract a BMW engine PID data table from a webpage and save it as CSV.")
    parser.add_argument("url", help="URL of the BMW engine page (e.g. https://thesecretingredient.neocities.org/bmw/dme/n55)")
    args = parser.parse_args()
    url = args.url

    # Step 1: Download and parse the webpage
    try:
        soup = fetch_page(url)
    except requests.RequestException as e:
        print(f"Network error while fetching the page: {e}")
        sys.exit(1)
    
    # Step 2: Extract the 'BMW Enhanced PID Data' table and convert to DataFrame
    try:
        df = extract_pid_table(soup)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Step 3: Derive output CSV filename from the URL (engine code from URL path)
    path = urlparse(url).path.strip('/')
    engine_code = path.split('/')[-1] if path else "output"
    csv_filename = f"{engine_code}_pid_data.csv"
    
    # Step 4: Save the DataFrame to a CSV file
    try:
        df.to_csv(csv_filename, index=False)
    except Exception as e:
        print(f"Error saving CSV file: {e}")
        sys.exit(1)
    
    # Step 5: Print the CSV content to the console
    csv_content = df.to_csv(index=False)
    # Strip the trailing newline for clean console output, then print
    print(csv_content.strip())
    print(f"\nCSV data has been saved to '{csv_filename}'.")  # Inform the user of the saved file

# Entry point for script execution
if __name__ == "__main__":
    main()

