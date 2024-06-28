import pandas as pd

# Load the CSV file
df = pd.read_csv('../data/porto_trajectories_all.csv')

# Initialize a dictionary to store the trajectories
trajectories = {}

# Iterate through each row and accumulate points for each trajectory
for index, row in df.iterrows():
    trajectory_id = row['trajectory_id']
    source_point = row['source_point']
    target_point = row['target_point']
    
    # Extract coordinates from POINT(x y) format
    source_coords = source_point.lstrip('POINT(').rstrip(')').replace(' ', ',')
    target_coords = target_point.lstrip('POINT(').rstrip(')').replace(' ', ',')
    
    if trajectory_id not in trajectories:
        trajectories[trajectory_id] = []
    
    trajectories[trajectory_id].append(source_coords)
    trajectories[trajectory_id].append(target_coords)

# Remove duplicate points within each trajectory
for trajectory_id in trajectories:
    trajectories[trajectory_id] = list(dict.fromkeys(trajectories[trajectory_id]))

# Write the transformed data to a new file
with open('../data/porto.dat', 'w') as file:
    for i, (trajectory_id, points) in enumerate(trajectories.items()):
        file.write(f"#{i}:\n")
        file.write(f">0: {'; '.join(points)}\n")
