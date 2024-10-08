"""
Author: Ilias Adamidis
Date: 17 / 09 / 2024

Description: This python file used Bs4 to scrape storms data of 1975 from wikipedia. Then using LLM via api and regex I clean and process the data
and then I save them in csv file "hurricanes_1975.csv"
"""

import requests
from bs4 import BeautifulSoup
import os
import replicate
import pandas as pd
import re

# Set the API token for Replicate LLM service
api = "your_api_key"
os.environ["REPLICATE_API_TOKEN"] = api

def ask_llama3(text, question):
    """
    Function to interact with the Llama 3 LLM, sending scraped data and a structured prompt.
    
    Args:
        text (str): The text data to provide context (hurricane data).
        question (str): The question or instruction to give to the LLM for processing.
    
    Returns:
        str: The output generated by the LLM in response to the prompt.
    """
    prompt = (
        f"{text}\n\n"
        "Please provide the data in a structured table format. The table should have the following columns: "
        "Storm Name, Date Start, Date End, Areas Affected, and Deaths. "
        "Each row should represent a different storm. Ensure that there are no extra comments or text outside the table."
        f"\n\nQuestion: {question}\n\n"
        "Table format example:\n"
        "| Storm Name | Date Start | Date End | Areas Affected | Deaths |\n"
        "| --- | --- | --- | --- | --- |\n"
        "| Example Storm | January 1 | January 5 | Location A | 10 |\n"
        "Please follow this format exactly.\n"
    )
    # Payload to send to the Llama 2 model
    input_payload = {
        "top_p": 0.9,
        "prompt": prompt,
        "min_tokens": 0,
        "temperature": 0.6,
        "presence_penalty": 1.15
    }

    output = ""
    # Stream the response from the Llama 2 model using the Replicate API
    for event in replicate.stream(
        "meta/meta-llama-3-70b-instruct",  # Use the correct Llama model
        input=input_payload
    ):
        if event.data:
            output += event.data
    # Clean the output and return it
    cleaned_output = output.strip().replace("{}", "").strip()
    return cleaned_output

def extract_table_from_llm_output(output):
    """
    Extracts the table from the LLM output and cleans it up for CSV writing.
    
    Args:
        output (str): The raw output from the LLM, which may include extra text.
        
    Returns:
        str: The cleaned table data in markdown format.
    """
    # Use a regex to find the table in markdown format
    table_pattern = re.compile(
        r'\| Storm Name \| Date Start \| Date End \| Areas Affected \| Deaths \|\n'
        r'\| --- \| --- \| --- \| --- \| --- \|\n'
        r'(?:\| [^\|]+\| [^\|]+\| [^\|]+\| [^\|]+\| [^\|]+\|\n)+',
        re.DOTALL
    )
    
    match = table_pattern.search(output)
    
    if match:
        return match.group(0).strip() # Return the matched table
    else:
        raise ValueError("The expected table format was not found in the LLM output.")

def markdown_table_to_csv(markdown_table):
    """
    Converts a markdown table to a CSV formatted string.
    
    Args:
        markdown_table (str): The markdown table as a string.
        
    Returns:
        str: The table data in CSV format.
    """
    # Split the markdown table into lines
    lines = markdown_table.splitlines()
    csv_lines = []
    
    # Process each line, cleaning and converting it to CSV format
    for line in lines:
        if line == "| --- | --- | --- | --- | --- |":
            continue # Skip the separator line
        # Remove markdown table delimiters and extra spaces
        csv_line = line.strip().replace('|', '').strip()
        
        # Replace commas to avoid issues with CSV format and ensure proper separation
        csv_line_repl_commas = csv_line.replace(',', ' /')
        csv_line_repl_commas = csv_line.replace('  ', ', ')
        csv_lines.append(csv_line_repl_commas)

    # Join lines and return as a CSV string
    return '\n'.join(csv_lines)

def save_table_to_csv(table_data, file_path):
    """
    Save the table data to a CSV file with correct headers.
    
    Args:
        table_data (str): The table data in markdown format.
        file_path (str): The path to the file where the CSV data will be saved.
    """
    # Convert markdown table data to CSV format string
    csv_data = markdown_table_to_csv(table_data)
    
    # Replace the first line (the old headers) with the correct headers
    correct_headers = "hurricane_storm_name, date_start, date_end, list_of_areas_affected, number_of_deaths\n"
    csv_data = correct_headers + '\n'.join(csv_data.split('\n')[1:])
    
    # Save the CSV data with UTF-8 encoding
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(csv_data)
    
    print(f"Data has been saved to: {file_path}")


def scrape_wikipedia_llm(url):
    """
    Scrapes hurricane data from a Wikipedia page and prepares it for LLM processing.

    Args:
        url (str): The Wikipedia URL containing the hurricane data.

    Returns:
        str: The relevant hurricane data in string format for the LLM to process.
    """
    # Define a header to mimic a regular browser request
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}
    
    # Make a request to fetch the webpage content
    response = requests.get(url, headers=headers)

    if not response.ok:
        print('Status Code:', response.status_code)
        raise Exception('Failed to fetch')

    # Parse the content using BeautifulSoup
    soup = BeautifulSoup(response.text, features="html.parser")

    table = soup.find('table', class_="wikitable")

    # Initialize lists to store the data
    data = []

    # Scrape the header row to get the column names dynamically
    headers = [header.get_text(strip=True) for header in table.find_all('tr')[0].find_all(['th', 'td'])]

    # Loop through the rows of the table, starting from the second row (to skip the header)
    for row in table.find_all('tr')[1:]:  
        cols = row.find_all(['th', 'td'])
        # Clean up the column text and store it in a list
        data.append([col.get_text(strip=True).replace('\xa0', ' ') for col in cols])

    # Convert the data to a pandas DataFrame using the dynamic headers
    df = pd.DataFrame(data, columns=headers)
    # Select only the required columns
    df_filtered = df[["Stormname", "Dates active", "Areas affected", "Deaths"]]
    
    # Convert the DataFrame to a string format for LLM to process
    data_str = df_filtered.to_string(index=False)
    
    return data_str  # Return the string representation of the relevant data

if __name__ == '__main__':
    # Scrape the Wikipedia data and pass to the LLM for refining
    url = "https://en.wikipedia.org/wiki/1975_Atlantic_hurricane_season"  

    # Step 1: Scrape the Wikipedia data
    try:
        scraped_data = scrape_wikipedia_llm(url)
    except Exception as e:
        print(f"Error during scraping: {e}")
        raise SystemExit("Terminating the program due to scraping failure.")  # Exit the program

    # Step 2: Define the question you want the LLM to answer or refine
    question = "Can you format the hurricane data into a concise structured table with Storm name, Date start, Date end, Areas affected, and Deaths?"

    # Step 3: Send the scraped data and the question to Llama 3 for further processing
    llm_output = ask_llama3(scraped_data, question) + '\n'

    # Print the response from the LLM
    print(llm_output)

    # Step 4: Extract the table from the LLM output
    output_csv_file = "hurricanes_1975.csv"
    try:
        table_data = extract_table_from_llm_output(llm_output)
        
        # Step 5: Save the table data to a CSV file
        save_table_to_csv(table_data, output_csv_file)
    except ValueError as e:
        print(f"Error extracting table: {e}")