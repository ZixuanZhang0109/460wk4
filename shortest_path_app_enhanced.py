
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

edges_cost = [(u, v, w * 0.2) for u, v, w in edges_miles]  # Assume $0.2 per mile
edges_time = [(u, v, w / 0.5) for u, v, w in edges_miles]  # Assume 0.5 miles/min

# --- Streamlit App Interface ---
st.title("🚗 Shortest Route Finder")
st.markdown("This app finds the **shortest path** between towns using a road map.")

# Optimization criteria
optimize_by = st.sidebar.radio("Optimize by", ["Miles", "Cost", "Time"])
edges = edges_miles
if optimize_by == "Cost":
    edges = edges_cost
elif optimize_by == "Time":
    edges = edges_time

# Create the graph
G = nx.DiGraph()
G.add_weighted_edges_from(edges)

st.sidebar.header("Choose Towns")
origin = st.sidebar.selectbox("Select Origin Town", sorted(G.nodes), index=0)
destination = st.sidebar.selectbox("Select Destination Town", sorted(G.nodes), index=len(G.nodes) - 1)

# Compute shortest path
if origin != destination:
    try:
        path = nx.dijkstra_path(G, origin, destination, weight='weight')
        path_length = nx.dijkstra_path_length(G, origin, destination, weight='weight')
        st.success(f"🚦 Shortest path from **{origin}** to **{destination}** optimizing by *{optimize_by}* is:\n\n➡️ {' → '.join(path)}\n\n🧮 Total {optimize_by}: **{path_length:.2f}**")
    except nx.NetworkXNoPath:
        st.error(f"No available path from {origin} to {destination}.")
else:
    st.warning("Origin and destination cannot be the same.")

# Draw network graph
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(8, 6))
nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue')
nx.draw_networkx_edges(G, pos, width=2)
nx.draw_networkx_labels(G, pos)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels={k: f"{v:.1f}" for k, v in edge_labels.items()})
st.pyplot(plt)
