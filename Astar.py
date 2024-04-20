import requests
import json

# Define the URL for the NodeMCU
node_url = "http://your-nodemcu-url/path"

# Define the environment
start = (0, 0)  # Starting point (x, y)
goal = (5, 5)  # Goal point (x, y)
obstacles = {(1, 2), (2, 2), (3, 2)}  # Obstacles as a set of coordinates

# A* algorithm function
def a_star_search(start, goal, obstacles):
    open_list = [start]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: calculate_distance(start, goal)}

    while open_list:
        current = min(open_list, key=lambda x: f_score.get(x, float('inf')))
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        open_list.remove(current)
        for neighbor in get_neighbors(current, obstacles):
            tentative_g_score = g_score[current] + calculate_distance(current, neighbor)
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + calculate_distance(neighbor, goal)
                if neighbor not in open_list:
                    open_list.append(neighbor)

    return None

# Helper function to get neighbors
def get_neighbors(point, obstacles):
    x, y = point
    neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    return [neighbor for neighbor in neighbors if neighbor not in obstacles]

# Helper function to calculate distance
def calculate_distance(point1, point2):
    return abs(point2[0] - point1[0]) + abs(point2[1] - point1[1])  # Manhattan distance

# Calculate the optimal path
path = a_star_search(start, goal, obstacles)

# Convert path to JSON and send to NodeMCU
path_json = json.dumps(path)

response = requests.post(node_url, data=path_json, headers={"Content-Type": "application/json"})

# Check the response
if response.status_code == 200:
    print("Path successfully sent to NodeMCU")
else:
    print("Failed to send path to NodeMCU")
