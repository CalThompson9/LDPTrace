import pandas as pd
import ast
import random
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

# Load the CSV file
logging.info("Loading CSV file...")
df = pd.read_csv('../data/train.csv')
logging.info(f"CSV file loaded. Number of rows: {len(df)}")

# Initialize a dictionary to store the trajectories
trajectories = {}

# Iterate through each row and accumulate points for each trajectory
logging.info("Processing trajectories...")
for index, row in df.iterrows():
    trip_id = row['TRIP_ID']
    polyline = row['POLYLINE']
    
    # Convert the POLYLINE string to a list of coordinates
    points = ast.literal_eval(polyline)
    
    if points:
        if trip_id not in trajectories:
            trajectories[trip_id] = []
        
        for point in points:
            # Convert the coordinates from [x, y] format to x,y format
            coords = f"{point[0]},{point[1]}"
            
            # Add coordinates if not already added
            if not trajectories[trip_id] or trajectories[trip_id][-1] != coords:
                trajectories[trip_id].append(coords)
        
        if index % 100000 == 0:
            logging.info(f"Processed {index} rows...")

logging.info("Finished processing trajectories.")
logging.info(f"Total unique trajectories: {len(trajectories)}")

# Remove empty trajectories
trajectories = {k: v for k, v in trajectories.items() if v}

logging.info(f"Trajectories after removing empty ones: {len(trajectories)}")

# Desired number of trajectories
desired_size = 361591

# # Sample the trajectories to achieve the desired size
# logging.info("Sampling trajectories...")
# sampled_keys = random.sample(list(trajectories.keys()), min(desired_size, len(trajectories)))
# sampled_trajectories = {key: trajectories[key] for key in sampled_keys}

# logging.info(f"Sampled number of trajectories: {len(sampled_trajectories)}")

# Write the transformed data to a new file
output_file = '../data/porto.dat'
logging.info(f"Writing transformed data to {output_file}...")
with open(output_file, 'w') as file:
    for i, (trip_id, points) in enumerate(trajectories.items()):
        file.write(f"#{i}:\n")
        file.write(f">0: {'; '.join(points)};\n")
logging.info("Data successfully written to file.")
