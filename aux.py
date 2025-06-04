import pulp
import urllib.parse
import requests

def get_travel_time(origin, destination, travel_mode, api_key=""):
  url = (
    "https://maps.googleapis.com/maps/api/distancematrix/json?"
    f"origins={urllib.parse.quote_plus(origin)}"
    f"&destinations={urllib.parse.quote_plus(destination)}"
    f"&key={api_key}&mode={travel_mode}"
  )
  response = requests.get(url)
  data = response.json()
  try:
    return data['rows'][0]['elements'][0]['duration']['value']
  except (KeyError, IndexError):
    return float('inf')

def generate_distance_matrix(addresses, travel_mode, api_key=""):
  matrix = {}
  for i, origin in enumerate(addresses):
    for j, destination in enumerate(addresses):
      if i != j:
        matrix[(i, j)] = get_travel_time(origin, destination, travel_mode, api_key)
  return matrix

def calculate_best_route_by_time(addresses, start, end, travel_mode, api_key=""):
  if not addresses or len(addresses) < 2:
    return []

  n = len(addresses)
  start_idx = addresses.index(start)
  end_idx = addresses.index(end)
  D = generate_distance_matrix(addresses, travel_mode, api_key)

  for key, value in D.items():
    if value == float('inf') or value is None:
      raise ValueError(
        f"No valid route between {addresses[key[0]]} and {addresses[key[1]]}.  \n"
        "Check your addresses or API limits.  \n"
        "The transport mode may not be available for some addresses.")

  prob = pulp.LpProblem("TSP", pulp.LpMinimize)
  x = pulp.LpVariable.dicts("x", [(i, j) for (i, j) in D], cat='Binary')
  u = pulp.LpVariable.dicts("u", list(range(n)), lowBound=0, upBound=n-1, cat='Integer')

  # Objective: minimize total time
  prob += pulp.lpSum(D[i, j] * x[i, j] for (i, j) in D)

  # Circular route (start == end) → Classic TSP (closed circuit - Traveling Salesman Problem)
  # Open route (start != end) → route with fixed start and end (Miller-Tucker-Zemlin)
  is_circular = (start == end)

  for i in range(n):
    if is_circular:
      prob += pulp.lpSum(x[i, j] for j in range(n) if i != j) == 1
      prob += pulp.lpSum(x[j, i] for j in range(n) if i != j) == 1
    else:
      if i == end_idx:
        prob += pulp.lpSum(x[i, j] for j in range(n) if i != j) == 0
      else:
        prob += pulp.lpSum(x[i, j] for j in range(n) if i != j) == 1

      if i == start_idx:
        prob += pulp.lpSum(x[j, i] for j in range(n) if i != j) == 0
      else:
        prob += pulp.lpSum(x[j, i] for j in range(n) if i != j) == 1

  # Cycle Elimination (MTZ)
  for i in range(1, n):
    for j in range(1, n):
      if i != j and (i, j) in x:
        prob += u[i] - u[j] + n * x[i, j] <= n - 1

  prob.solve(pulp.PULP_CBC_CMD())

  # for i in range(len(addresses)):
  #   for j in range(len(addresses)):
  #     if i != j:
  #       print(i, j, x[(i, j)].value())

  # Extract solution
  route = [start_idx]
  current = start_idx
  visited = set()
  while True:
    visited.add(current)
    for j in range(n):
      if current != j and (current, j) in x and pulp.value(x[current, j]) == 1:
        route.append(j)
        current = j
        break
    if (is_circular and current == start_idx) or (not is_circular and current == end_idx):
      break

  return [addresses[i] for i in route]

def generate_google_maps_link(route, travel_mode="driving"):
  base_url = "https://www.google.com/maps/dir/?"
  query = {
    "api": 1,
    "travelmode": travel_mode,
    "origin": route[0],
    "destination": route[-1],
    "waypoints": "|".join(route[1:-1]) if len(route) > 2 else None
  }
  query = {k: v for k, v in query.items() if v is not None}

  return base_url + urllib.parse.urlencode(query, quote_via=urllib.parse.quote)

def generate_google_maps_embed_link(route, travel_mode="driving", api_key=""):
    base_url = "https://www.google.com/maps/embed/v1/directions?"
    
    query = {
        "key": api_key,
        "origin": route[0],
        "destination": route[-1],
        "waypoints": "|".join(route[1:-1]) if len(route) > 2 else None,
        "mode": travel_mode
    }

    if len(route) > 2:
        waypoints = "|".join(route[1:-1])
        query["waypoints"] = waypoints

    full_url = base_url + urllib.parse.urlencode(query, quote_via=urllib.parse.quote)
    return full_url