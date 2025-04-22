import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Define data
professors = ['Prof1', 'Prof2', 'Prof3']
semesters = ['Fall', 'Spring']
courses = ['Marketing', 'Finance', 'Production']

semester_pref = {
    'Prof1': {'Fall': 3, 'Spring': 4},
    'Prof2': {'Fall': 5, 'Spring': 3},
    'Prof3': {'Fall': 4, 'Spring': 4},
}

course_pref = {
    'Prof1': {'Marketing': 6, 'Finance': 5, 'Production': 4},
    'Prof2': {'Marketing': 4, 'Finance': 6, 'Production': 5},
    'Prof3': {'Marketing': 5, 'Finance': 4, 'Production': 6},
}

# Compute satisfaction
assignments = []
for p in professors:
    for s in semesters:
        for c in courses:
            satisfaction = semester_pref[p][s] + course_pref[p][c]
            assignments.append((p, s, c, satisfaction))

# Build graph
G = nx.DiGraph()

# Source and sink
G.add_node('Source')
G.add_node('Sink')

# Add professor nodes and edges from Source
for p in professors:
    G.add_edge('Source', p, capacity=4, weight=0)

# Add assignment nodes and edges from professors
for p, s, c, sat in assignments:
    node = f"{p}_{s}_{c}"
    G.add_node(node)
    G.add_edge(p, node, capacity=1, weight=-sat)

# Add course-semester nodes and connect assignment nodes to them
for s in semesters:
    for c in courses:
        sem_node = f"{s}_{c}"
        G.add_node(sem_node)
        for p in professors:
            assign_node = f"{p}_{s}_{c}"
            G.add_edge(assign_node, sem_node, capacity=1, weight=0)

# Add course nodes and connect course-semester nodes to course nodes
for c in courses:
    G.add_node(c)
    for s in semesters:
        sem_node = f"{s}_{c}"
        G.add_edge(sem_node, c, capacity=4, weight=0)

# Connect courses to Sink
for c in courses:
    G.add_edge(c, 'Sink', capacity=4, weight=0)

# Display graph
st.title("Professor-Course Assignment Network")
fig, ax = plt.subplots(figsize=(14, 10))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=8, ax=ax)
edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6, ax=ax)
st.pyplot(fig)

st.markdown("""
**Instructions:**
- This network model assigns professors to semester-course combinations to maximize satisfaction.
- Edges from professors to assignments have weights as the **negative satisfaction** (to minimize cost).
- Flow capacities reflect constraints like course demands and teaching load.
""")
