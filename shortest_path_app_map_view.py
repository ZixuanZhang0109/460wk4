
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# --- Define weighted edge sets ---
edges_miles = [
    ('Origin', 'A', 40),
    ('Origin', 'B', 60),
    ('Origin', 'C', 50),
    ('A', 'B', 10),
    ('A', 'D', 70),
    ('B', 'C', 20),
    ('B', 'D', 55),
    ('B', 'E', 40),
    ('C', 'E', 50),
    ('D', 'E', 10),
    ('D', 'Destination', 60),
    ('E', 'Destination', 80),
]

edges_cost = [(u, v, w * 0.2) for u, v, w in edges_miles]
edges_time = [(u, v, w / 0.5) for u, v, w in edges_miles]

# Fixed "map-like" coordinates for each town
fixed_pos = {
    'Origin': (0, 2),
    'A': (1, 4),
    'B': (2, 3),
    'C': (3, 5),
    'D': (3, 2),
    'E': (4, 3),
    'Destination': (5, 2)
}

# --- Streamlit App Interface ---
st.set_page_config(page_title="Shortest Path Finder", layout="wide")
st.title("🗺️ Map-Based Route Finder")
st.markdown("Find the shortest path using fixed map coordinates.")

st.sidebar.header("Settings")
optimize_by = st.sidebar.radio("Optimize by", ["Miles", "Cost", "Time"])
origin = st.sidebar.selectbox("Select Origin Town", list(fixed_pos.keys()), index=0)
destination = st.sidebar.selectbox("Select Destination Town", list(fixed_pos.keys()), index=-1)

# Choose edge weights
if optimize_by == "Miles":
    edges = edges_miles
    unit = "mi"
elif optimize_by == "Cost":
    edges = edges_cost
    unit = "$"
else:
    edges = edges_time
    unit = "min"

# Create graph
G = nx.DiGraph()
G.add_weighted_edges_from(edges)

# Calculate path
st.subheader("📍 Shortest Route")
if origin != destination:
    try:
        path = nx.dijkstra_path(G, origin, destination, weight='weight')
        path_length = nx.dijkstra_path_length(G, origin, destination, weight='weight')
        st.success(f"**Best route ({optimize_by})**: {' → '.join(path)}")
        st.info(f"**Total {optimize_by}**: {path_length:.2f} {unit}")
    except nx.NetworkXNoPath:
        st.error("No valid path.")
        path = []
else:
    st.warning("Origin and destination must differ.")
    path = []

# Draw the map-style network
st.subheader("📌 Map View")
plt.figure(figsize=(10, 6))
nx.draw_networkx_nodes(G, fixed_pos, node_size=700, node_color='lightgreen')
nx.draw_networkx_labels(G, fixed_pos, font_size=10)
nx.draw_networkx_edges(G, fixed_pos, edgelist=G.edges, width=2, alpha=0.3)

# Edge labels
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, fixed_pos, edge_labels={k: f"{v:.1f} {unit}" for k, v in edge_labels.items()})

# Highlight path
if path:
    path_edges = list(zip(path[:-1], path[1:]))
    nx.draw_networkx_edges(G, fixed_pos, edgelist=path_edges, edge_color='red', width=3)

st.pyplot(plt)
