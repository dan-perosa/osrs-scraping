## **osrs-scraping**

**A Python script to scrape Old School Runescape wiki data.**

### Overview
This repository contains Python scripts designed to scrape the Old School Runescape (OSRS) wiki for detailed information on quests, equipment, and monsters. The extracted data is then exported to Excel (.xlsx) files for further analysis or use in other projects. 

### Features
* Scrapes OSRS wiki pages for quests, equipment, and monsters.
* Extracts a wide range of data, including names, descriptions, requirements, and statistics.
* Exports data to clean and organized Excel files.

### Requirements
* Python 3.6+
* Required libraries can be installed using `pip install -r requirements.txt`

### Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/dan-perosa/osrs-scraping.git
   ```
2. **Install dependencies:**
   ```bash
   cd osrs-scraping
   pip install -r requirements.txt
   ```
3. **Run the scripts:**
   * **To scrape quest data:**
     ```bash
     python osrs_wiki_quests_scraping.py
     ```
   * **To scrape equipment data:**
     ```bash
     python osrs_wiki_equipments_scraping.py
     ```
   * **To scrape monster data:**
     ```bash
     python osrs_wiki_monsters_scraping.py
     ```
   The scripts will generate Excel files in the `output` directory.

### Data Usage
The generated Excel files can be used for various purposes, such as:

* **Data analysis:** Explore trends, relationships, and insights within the OSRS game world.
* **Machine learning:** Train models for tasks like item identification, monster classification, or quest recommendation.
* **Integration with other projects:** Use the data in projects like OSRSdle, a minigame that I've developed.

### Contributing
Contributions are welcome! Please feel free to open an issue or submit a pull request.

**Note:**

* **Customization:** You can customize the scripts to extract additional data or modify the output format.
* **Rate limiting:** Be mindful of the OSRS wiki's rate limits to avoid being blocked.
* **Data cleaning:** Some data cleaning might be necessary before using the extracted data.

### Additional Information
* **OSRSdle:** This repository's data is used in the OSRSdle project, a minigame focused on guessing OSRS-related items. Check it out at [https://github.com/dan-perosa/osrsdle].
* **Supabase:** The scraped data was exported to a Supabase Postgres database for further processing and integration with OSRSdle.
