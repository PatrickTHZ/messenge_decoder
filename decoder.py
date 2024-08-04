import requests
from bs4 import BeautifulSoup

def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_data(data):
    soup = BeautifulSoup(data, 'html.parser')
    table = soup.find('table')
    grid_data = []

    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skip the header row
            cols = row.find_all('td')
            if len(cols) == 3:
                try:
                    x = int(cols[0].get_text().strip())
                    char = cols[1].get_text().strip()
                    y = int(cols[2].get_text().strip())
                    grid_data.append((x, char, y))
                except ValueError:
                    print(f"Skipping line with non-integer coordinates: {cols[0].get_text().strip()}, {cols[2].get_text().strip()}")
            else:
                print(f"Skipping malformed row: {row}")

    return grid_data

def create_grid(grid_data):
    if not grid_data:
        return ""

    # Determine the size of the grid
    max_x = max(item[0] for item in grid_data)
    max_y = max(item[2] for item in grid_data)

    # Initialize the grid with spaces
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # Place characters in the grid
    for x, char, y in grid_data:
        grid[y][x] = char

    return grid

def print_grid(grid):
    for row in grid:
        print(''.join(row))

def decode_secret_message(url):
    data = fetch_data(url)
    grid_data = parse_data(data)
    grid = create_grid(grid_data)
    print_grid(grid)

# Example usage:
url = 'https://docs.google.com/document/d/e/2PACX-1vSHesOf9hv2sPOntssYrEdubmMQm8lwjfwv6NPjjmIRYs_FOYXtqrYgjh85jBUebK9swPXh_a5TJ5Kl/pub'
decode_secret_message(url)
