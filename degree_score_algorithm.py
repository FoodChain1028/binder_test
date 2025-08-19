import random

def generate_random_graph(n, m):
    """
    Generates a graph using a Python dictionary (adjacency list).
    """
    if n < 0 or m < 0:
        raise ValueError("Number of vertices and edges must be non-negative.")
    max_edges = n * (n - 1) // 2
    if m > max_edges:
        raise ValueError(f"Edge count {m} exceeds the maximum possible of {max_edges}.")

    # The graph is an adjacency list: a dict of node -> set of neighbors
    graph = {i: set() for i in range(n)}
    
    possible_edges = []
    if n > 1:
        for i in range(n):
            for j in range(i + 1, n):
                possible_edges.append((i, j))
    
    random.shuffle(possible_edges)
    
    for u, v in possible_edges[:m]:
        graph[u].add(v)
        graph[v].add(u)
        
    return graph

# ---

def compute_next_scores(graph, current_scores=None):
    """
    Computes scores using the dictionary-based graph.
    """
    n = len(graph)
    
    if current_scores is None:
        x = [1.0] * n
    else:
        x = list(current_scores)
        
    y = [0.0] * n
    degrees = {node: len(neighbors) for node, neighbors in graph.items()}
    
    for i in graph.keys():
        for j in graph[i]:
            if degrees[j] > 0:
                y[i] += x[j] / degrees[j]
            
    return y

# ---

def display_graph_state(graph, scores, title):
    """
    Prints the graph's nodes, scores, and neighbors to the console.
    """
    print(f"\n--- {title} ---")
    if not graph:
        print("Graph is empty.")
        return
        
    for node in sorted(graph.keys()):
        score = scores[node]
        neighbors = sorted(list(graph[node]))
        print(f"Node {node:<2} | Score: {score:<7.4f} | Neighbors: {neighbors}")
    print("-" * (len(title) + 6))

# ---

def handle_user_edge_addition(graph, current_scores):
    """
    Prompts the user to add an edge and displays the new state.
    """
    n = len(graph)
    if n < 2:
        print("\nCannot add new edges to a graph with fewer than 2 vertices.")
        return graph, current_scores

    while True:
        try:
            prompt = f"\nEnter two distinct vertices to connect (from 0 to {n-1}), separated by a space: "
            user_input = input(prompt)
            i, j = map(int, user_input.split())

            if not (0 <= i < n and 0 <= j < n):
                print(f"Error: Vertices must be within the range [0, {n-1}].")
            elif i == j:
                print("Error: Vertices must be distinct.")
            elif j in graph[i]:
                print(f"Error: Edge ({i}, {j}) already exists.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter two integers separated by a space.")
    
    graph[i].add(j)
    graph[j].add(i)
    print(f"\nEdge ({i}, {j}) successfully added.")
    
    new_scores = compute_next_scores(graph, current_scores)
    
    display_graph_state(graph, new_scores, f"State After Adding Edge ({i}, {j})")
    
    return graph, new_scores

# ---

if __name__ == "__main__":
    # 1. Get graph parameters from the user with validation
    while True:
        try:
            n_input = input("Enter the number of vertices (e.g., 10): ")
            N_VERTICES = int(n_input)
            if N_VERTICES >= 0:
                break
            else:
                print("Error: Number of vertices cannot be negative.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            
    max_possible_edges = N_VERTICES * (N_VERTICES - 1) // 2
    
    while True:
        try:
            m_input = input(f"Enter the number of edges (0 to {max_possible_edges}): ")
            M_EDGES = int(m_input)
            if 0 <= M_EDGES <= max_possible_edges:
                break
            else:
                print(f"Error: Number of edges must be between 0 and {max_possible_edges}.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    # 2. Generate the graph based on user input
    G = generate_random_graph(N_VERTICES, M_EDGES)
    print(f"\n✅ Generated a random graph with {N_VERTICES} vertices and {M_EDGES} edges.")
    
    # 3. Proceed with the simulation
    initial_scores = [1.0] * N_VERTICES
    display_graph_state(G, initial_scores, "Initial State (All Scores 1.0)")

    updated_scores = compute_next_scores(G, initial_scores)
    display_graph_state(G, updated_scores, "Updated State (First Iteration)")
    
    handle_user_edge_addition(G, updated_scores)
    
    print("\nProcess finished. 👋")