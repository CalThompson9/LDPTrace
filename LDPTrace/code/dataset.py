from typing import List, Tuple
import numpy as np
import json
import pickle
import trajectory


def read_brinkhoff(dataset='brinkhoff'):
    """
    Brinkhoff dataset:
    #n:
    >0: x1,y1;x2,y2;...:
    """
    db = []
    file_name = f'../data/{dataset}.dat'
    parse_oldenburg(file_name)
    file_name = file_name.replace('.dat', '_formatted.dat')
    with open(file_name, 'r') as f:
        row = f.readline()
        while row:
            if row[0] == '#':
                row = f.readline()
                continue
            if not row[0] == '>':
                print(row)
                exit()
            # Skip '>0:' and ';\n' in the end
            row = row[3:-2].split(';')  # row: ['x1,y1', 'x2,y2', ...]

            t = [x.split(',') for x in row]  # t: [['x1','y1'], ['x2','y2'], ...]

            t = [(eval(x[0]), eval(x[1])) for x in t]  # t: [(x1,y1), (x2,y2), ...]

            db.append(t)
            row = f.readline()

    return db


def dataset_stats(db: List[List[Tuple[float, float]]], db_name: str):
    lengths = np.asarray([len(t) for t in db])

    xs = [[p[0] for p in t] for t in db]
    ys = [[p[1] for p in t] for t in db]

    min_xs = [min(x) for x in xs]
    min_ys = [min(y) for y in ys]
    max_xs = [max(x) for x in xs]
    max_ys = [max(y) for y in ys]

    stats = {
        'num': len(db),
        'min_len': int(min(lengths)),
        'max_len': int(max(lengths)),
        'mean_len': float(np.mean(lengths)),
        'min_x': min(min_xs),
        'min_y': min(min_ys),
        'max_x': max(max_xs),
        'max_y': max(max_ys)
    }

    print(stats)

    with open(db_name, 'w') as f:
        json.dump(stats, f)

    return stats



# ----- CODE TO PARSE OLDENBURG DATASET -----
   
def parse_line(line):
    parts = line.split()
    if len(parts) == 10:
        label, point_id, seq_num, obj_class, timestamp, x_coord, y_coord, speed, next_x, next_y = parts
        return {
            "label": label,
            "point_id": int(point_id),
            "seq_num": int(seq_num),
            "obj_class": int(obj_class),
            "timestamp": int(timestamp),
            "x_coord": float(x_coord),
            "y_coord": float(y_coord),
            "speed": float(speed),
            "next_x": int(next_x),
            "next_y": int(next_y)
        }
    else:
        return None

def transform_data(lines):
    data = {}
    for line in lines:
        parsed = parse_line(line)
        if parsed:
            point_id = parsed["point_id"]
            if point_id not in data:
                data[point_id] = []
            data[point_id].append(f"{parsed['x_coord']},{parsed['y_coord']}")
    return data

def format_transformed_data(data):
    formatted_lines = []
    for point_id, coords in data.items():
        formatted_lines.append(f"#{point_id}:")
        formatted_lines.append(f">0: {'; '.join(coords)}")
    return formatted_lines

def parse_oldenburg(input_file: str):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    data = transform_data(lines)
    formatted_lines = format_transformed_data(data)
    
    with open(output_file, 'w') as file:
        file.write("\n".join(formatted_lines))

output_file = '../data/oldenburg_formatted.dat'

# ----- CODE TO READ PORTO DATASET -----
def read_porto(dataset='porto'):
    """
    Porto dataset:
    #n:
    >0: x1,y1;x2,y2;...:
    """
    db = []
    file_name = f'../data/{dataset}.dat'
    with open(file_name, 'r') as f:
        row = f.readline()
        while row:
            if row[0] == '#':
                row = f.readline()
                continue
            if not row[0] == '>':
                print(row)
                exit()
            # Skip '>0:' and ';\n' in the end
            row = row[3:-2].split(';')  # row: ['x1,y1', 'x2,y2', ...]

            t = [x.split(',') for x in row]  # t: [['x1','y1'], ['x2','y2'], ...]

            t = [(eval(x[0]), eval(x[1])) for x in t]  # t: [(x1,y1), (x2,y2), ...]

            db.append(t)
            row = f.readline()

    return db