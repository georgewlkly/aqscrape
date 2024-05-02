# This assumes that you have 1) signed up for an OpenAI API key and 2) that your API key is saved as an environmental variable locally, see https://platform.openai.com/docs/quickstart
from openai import OpenAI
import csv
import os
import pandas as pd

client = OpenAI()

# Load the episodes data from CSV - update path and filenames
input_dir = "path/to"
input_file = os.path.join(input_dir, 'episode_details.csv')
episodes = pd.read_csv(input_file)

# Prepare the output directory and file
os.makedirs(input_dir, exist_ok=True)
output_csv_path = os.path.join(input_dir, 'panellists.csv')

# Prepare to write output
with open(output_csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['URL', 'Broadcast Date', 'Panellist Name'])  # Header for the CSV file

    # Process each episode
    for index, row in episodes.iterrows():
        synopsis = row['Synopsis']
        url = row['URL']
        broadcast_date = row['Broadcast Date']

        # Generate the prompt and get the completion from OpenAI GPT-3.5 Turbo
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant and knowledgeable political researcher."},
                {"role": "user", "content": f"Identify the names of the guest panellists from this episode synopsis. You must always exclude the presenter. The only text you should return is the name of the panellists. The expected output is four names only. Synopsis: {synopsis}"}
            ]
        )

        # Extract panellists names from the response
        panellists_text = completion.choices[0].message.content
        panellists_list = [name.strip() for name in panellists_text.split(',') if name.strip()]

        # Write each panellist to the CSV file with the episode's URL and Broadcast Date
        for panellist in panellists_list:
            writer.writerow([url, broadcast_date, panellist])

print("Panellists have been written to:", output_csv_path)
