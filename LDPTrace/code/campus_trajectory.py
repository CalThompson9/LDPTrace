import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

file_path = '../data/ubco_buildings_full.geojson'
random_seed = 42  # Set a random seed for reproducibility
random.seed(random_seed)
np.random.seed(random_seed)

# Load the geojson file
with open(file_path, 'r') as file:
    geojson_data = json.load(file)

# Extract buildings and their properties
features = geojson_data['features']
buildings = []

for feature in features:
    properties = feature['properties']
    coordinates = feature['geometry']['coordinates'][0][0] if feature['geometry']['type'] == 'Polygon' else feature['geometry']['coordinates'][0][0][0]
    buildings.append({
        'uid': properties['BLDG_UID'],
        'name': properties['NAME'],
        'code': properties['BLDG_CODE'],
        'usage': properties['BLDG_USAGE'],  # Using building usage as the category
        'coordinates': coordinates  # Extracting the first coordinate point
    })

# Convert to DataFrame
buildings_df = pd.DataFrame(buildings)

# Extract unique values in the BLDG_USAGE column
unique_usages = buildings_df['usage'].unique()
print("Unique BLDG_USAGE values:")
for usage in unique_usages:
    print(usage)

# Define POI categories and buildings
poi_categories = buildings_df.groupby('usage')['uid'].apply(list).to_dict()
poi_coordinates = buildings_df.set_index('uid')['coordinates'].to_dict()

# Set parameters
num_trajectories = 10000  # Number of trajectories
trajectory_length_bounds = (3, 8)  # Trajectory length bounds
time_bounds = (10, 120)  # Time gap bounds in minutes
start_time_bounds = (6, 22)  # Start time bounds in hours

# Function to generate a single trajectory
def generate_trajectory(trajectory_length_bounds, poi_categories, time_bounds, start_time_bounds):
    trajectory_length = np.random.randint(*trajectory_length_bounds)
    start_time = datetime.now().replace(hour=np.random.randint(*start_time_bounds), minute=0, second=0, microsecond=0)
    current_time = start_time

    # First POI
    first_category = random.choice(list(poi_categories.keys()))
    first_poi = random.choice(poi_categories[first_category])
    trajectory = [(current_time, first_poi, first_category)]

    for _ in range(1, trajectory_length):
        time_gap = timedelta(minutes=np.random.uniform(*time_bounds))
        current_time += time_gap

        # Choose the next POI category and POI
        next_category = random.choice(list(poi_categories.keys()))
        next_poi = random.choice(poi_categories[next_category])

        trajectory.append((current_time, next_poi, next_category))

    return trajectory

# Introduce popular events
def introduce_popular_events(trajectory, start_time):
    events = [
        (timedelta(hours=20), 'Residence_A', 'StudentHousing'),
        (timedelta(hours=14), 'Stadium_A', 'Athletics'),
        (timedelta(hours=9), random.choice(poi_categories['Academic']), 'Academic')
    ]
    
    for event_time, event_poi, event_category in events:
        event_datetime = start_time + event_time
        # Find a suitable point in the trajectory
        for i, (time, poi, category) in enumerate(trajectory):
            if event_datetime <= time <= event_datetime + timedelta(hours=2):
                trajectory[i] = (time, event_poi, event_category)
    return trajectory

# Generate multiple trajectories
trajectories = []
for _ in range(num_trajectories):
    single_trajectory = generate_trajectory(trajectory_length_bounds, poi_categories, time_bounds, start_time_bounds)
    start_time = single_trajectory[0][0]  # The start time of the trajectory
    trajectories.append(introduce_popular_events(single_trajectory, start_time))

# Convert trajectories to a DataFrame
trajectories_df = pd.DataFrame([
    {'timestamp': time, 'poi': poi, 'category': category, 'trajectory_id': traj_id}
    for traj_id, trajectory in enumerate(trajectories)
    for time, poi, category in trajectory
])

# Save the trajectories to a CSV file
trajectories_df.to_csv('../data/generated_trajectories.csv', index=False)

# Function to parse and format the data into campus.dat format
def format_trajectory_data(trajectories, poi_coordinates):
    formatted_lines = []
    for traj_id, trajectory in enumerate(trajectories):
        formatted_lines.append(f"#{traj_id}:")
        points = [f"{poi_coordinates[poi][0]},{poi_coordinates[poi][1]}" for _, poi, _ in trajectory]
        formatted_lines.append(f">0: {'; '.join(points)};")
    return formatted_lines

# Generate formatted data for campus.dat
formatted_data = format_trajectory_data(trajectories, poi_coordinates)

# Write the formatted data to campus.dat file
with open('../data/campus.dat', 'w') as file:
    file.write("\n".join(formatted_data))
