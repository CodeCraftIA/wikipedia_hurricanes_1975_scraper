### 🌪️ **1975 Atlantic Hurricane Data Scraper & Processor**  
📋 **Overview**

This project extracts storm data from the [1975 Atlantic hurricane season Wikipedia page](https://en.wikipedia.org/wiki/1975_Atlantic_hurricane_season) and processes it into a clean, structured CSV file using a combination of web scraping and LLM-based data refinement.

Using **Beautiful Soup**, the script scrapes raw hurricane data from Wikipedia, and then a **Language Learning Model (LLM)** processes the data into a structured table. The final output is saved as a CSV file named hurricanes_1975.csv.  
  

<br/>  



### 🛠️ **Technologies Used**  
- **Python**  
  

- **Beautiful Soup** (for web scraping)  
  

- **Replicate API** (for interacting with the LLM)  
  

- **Pandas** (for data manipulation)  
  

- **Regular Expressions** (for data extraction)  
  

<br/>  



### 🚀 **Project Workflow**  
- **Scraping**: Extract hurricane data from Wikipedia using Beautiful Soup.  
  

- **Data Processing**: Send the scraped data to an LLM for conversion into a structured format.  
  

- **Table Extraction**: Extract and clean the table using regex.  
  

- **Save as CSV**: Convert the cleaned data to a CSV format and save it.  
  

<br/>  



### ⚙️ **How to Run**  
- **Clone the Repository**: 

   git clone https://github.com/CodeCraftIA/wikipedia_hurricanes_1975_scraper

   cd wikipedia_hurricanes_1975_scraper  
  

- **Install Requirements**:

   pip install -r requirements.txt  
  

- **Set Up API Token**: 

   Replace "your_api_key" in the code with your Replicate LLM API key.  
  

- **Run the Script**:

   python wikipedia_exercise.py  
  

<br/>  



### 📝 **Details**  
- **Scraping**: The script scrapes the Wikipedia page and retrieves relevant hurricane data, including storm names, dates, affected areas, and fatalities.  
  

- **LLM Processing**: The scraped data is fed into the **Llama 3 LLM** to structure it into a readable and precise table.  
  

- **Regex & CSV Conversion**: Using regex, the table is extracted from the LLM's output and saved as hurricanes_1975.csv.  
  

<br/>  



### 🔗 **References**  
- [1975 Atlantic Hurricane Season (Wikipedia)](https://en.wikipedia.org/wiki/1975_Atlantic_hurricane_season)  
  

- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)  
  

- [Replicate API for LLM](https://replicate.com/meta/meta-llama-3-70b-instruct/api)  

<br />
