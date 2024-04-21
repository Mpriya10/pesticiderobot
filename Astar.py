from flask import Flask, request, jsonify
import heapq

app = Flask(__name__)

# A* algorithm function
def a_star_search(start, goal, obstacles):
    open_list = [(calculate_distance(start, goal), 0, start)]  # (f_score, g_score, node)
    came_from = {}
    g_score = {start: 0}

    while open_list:
        _, _, current = heapq.heappop(open_list)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for neighbor in get_neighbors(current, obstacles):
            tentative_g_score = g_score[current] + 1  # Assuming each move has a cost of 1
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + calculate_distance(neighbor, goal)
                heapq.heappush(open_list, (f_score, tentative_g_score, neighbor))

    return None

# Helper function to get neighbors
def get_neighbors(point, obstacles):
    x, y = point
    neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    return [neighbor for neighbor in neighbors if neighbor not in obstacles]

# Helper function to calculate distance
def calculate_distance(point1, point2):
    return abs(point2[0] - point1[0]) + abs(point2[1] - point1[1])  # Manhattan distance

# API endpoint to receive path calculation request
@app.route('/path', methods=['POST'])
def calculate_path():
    data = request.get_json()
    start = tuple(data['start'])
    goal = tuple(data['goal'])
    obstacles = set(map(tuple, data['obstacles']))
    path = a_star_search(start, goal, obstacles)
    if path:
        return jsonify({'path': path})
    else:
        return jsonify({'error': 'Failed to find a path'}),

if __name__ == '__main__':
    app.run(debug=True)
