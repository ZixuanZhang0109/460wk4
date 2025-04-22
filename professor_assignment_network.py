
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Professor-Course Assignment Network Flow Diagram")

# Initialize graph
G = nx.DiGraph()

# Define nodes
source = "Source"
sink = "Sink"
professors = ["P1", "P2", "P3"]
courses = ["Marketing", "Finance", "Production"]
semesters = ["Fall", "Spring"]

course_semesters = [f"{c}_{s}" for c in courses for s in semesters]

# Add edges from Source to Professors
for p in professors:
    G.add_edge(source, p, capacity=4, weight=0)

# Satisfaction scores (negated for min cost)
semester_pref = {
    "P1": {"Fall": 3, "Spring": 4},
    "P2": {"Fall": 5, "Spring": 3},
    "P3": {"Fall": 4, "Spring": 4},
}

course_pref = {
    "P1": {"Marketing": 6, "Finance": 5, "Production": 4},
    "P2": {"Marketing": 4, "Finance": 6, "Production": 5},
    "P3": {"Marketing": 5, "Finance": 4, "Production": 6},
}

# Add edges from Professors to Course-Semester nodes
for p in professors:
    for c in courses:
        for s in semesters:
            sat = semester_pref[p][s] + course_pref[p][c]
            cost = -sat  # negate for min cost flow
            node = f"{c}_{s}"
            G.add_edge(p, node, capacity=1, weight=cost)

# Add edges from Course-Semester nodes to Sink
for cs in course_semesters:
    G.add_edge(cs, sink, capacity=2, weight=0)

# Draw the graph
pos = {}

# Manual positions for a clean layout
pos[source] = (-2, 0)
for i, p in enumerate(professors):
    pos[p] = (-1, 2 - i)

for i, cs in enumerate(course_semesters):
    pos[cs] = (1, 3 - 0.6 * i)

pos[sink] = (2, 0)

fig, ax = plt.subplots(figsize=(14, 8))
nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=2000, font_size=10, arrowsize=20)

# Draw edge labels (capacities and costs)
edge_labels = {
    (u, v): f"{d['capacity']}, {d['weight']}" for u, v, d in G.edges(data=True)
}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

st.pyplot(fig)
