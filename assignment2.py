import argparse
import urllib.request  
import logging
from datetime import datetime
import csv

# Setup logger to write to errors.log
def setupLogger():
    logging.basicConfig(
        filename='errors.log', 
        level=logging.ERROR,
        format='%(asctime)s %(levelname)s: %(message)s'
    )

def downloadData(url):
    """
    Downloads the contents from the provided URL and returns it.
    
    Args:
        url (str): The URL to download the content from.

    Returns:
        str: The content retrieved from the URL.
    """
    try:
        response = urllib.request.urlopen(url)
        csvData = response.read().decode('utf-8')  # Decode byte content to string
        return csvData
    except Exception as e:
        logging.error(f"Error downloading data from URL: {url} - {e}")
        raise

def processData(csvData):
    """
    Processes the CSV file contents and returns a dictionary mapping an ID to a tuple (name, birthday).
    
    Args:
        csvData (str): The contents of the CSV file as a string.
    
    Returns:
        dict: A dictionary mapping an ID to a tuple of (name, birthday).
    """
    data_dict = {}
    reader = csv.reader(csvData.splitlines())
    
    # Skip header
    next(reader)
    
    for line_num, row in enumerate(reader, start=1):
        id_ = row[0]
        name = row[1]
        try:
            # Parse the birthday into a datetime object
            birthday = datetime.strptime(row[2], '%d/%m/%Y')
        except ValueError:
            # Log errors for malformed dates
            logging.error(f"Error processing line #{line_num} for ID #{id_}: {row[2]}")
            continue
        
        # Store the result in the dictionary
        data_dict[id_] = (name, birthday)
    
    return data_dict

def displayPerson(id, personData):
    """
    Displays a person's information given their ID and the personData dictionary.
    
    Args:
        id (str): The person's ID.
        personData (dict): A dictionary containing person information.
    """
    person = personData.get(id)
    if person:
        name, birthday = person
        print(f"Person #{id} is {name} with a birthday of {birthday.strftime('%Y-%m-%d')}.")
    else:
        print(f"No person found with ID #{id}.")

def main(url):
    """
    Main function that orchestrates downloading, processing, and displaying data.
    
    Args:
        url (str): The URL to download the data from.
    """
    print(f"Running main with URL = {url}...")
    
    # Download and process the data
    try:
        csvData = downloadData(url)
        personData = processData(csvData)
    except Exception as e:
        print(f"Failed to process data: {e}")
        return

    # Ask the user for IDs and display the person's info
    while True:
        try:
            user_input = input("Enter an ID to look up (or 0 to exit): ")
            user_id = int(user_input)

            if user_id <= 0:
                print("Exiting the program.")
                break
            
            # Display person data
            displayPerson(str(user_id), personData)
        
        except ValueError:
            print("Please enter a valid integer ID.")

if __name__ == "__main__":
    """Main entry point"""
    # Setup the logger to log to errors.log
    setupLogger()

    # Setup argument parsing for --url
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    
    # Call main with the provided URL
    main(args.url)
