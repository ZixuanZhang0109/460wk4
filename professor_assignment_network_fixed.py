# professor_assignment_network.py
"""
Streamlit app: Minimum‑Cost Network Flow diagram
for the three‑professor, three‑course assignment problem.
"""

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# Page settings
# ------------------------------------------------------------------
st.set_page_config(page_title="Professor–Course Assignment Network",
                   layout="centered")
st.title("Professor–Course Assignment  –  Network‑Flow Diagram")

# ------------------------------------------------------------------
# 1. Data and parameters
# ------------------------------------------------------------------
professors = ["P1", "P2", "P3"]
courses    = ["M", "F", "P"]           # M = Marketing, F = Finance, P = Production
semesters  = ["Fall", "Spring"]

# Semester preferences (utility contribution) for each professor
semester_pref = {                      #   P1  P2  P3
    "Fall":   dict(zip(professors,  [ 3,  5,  4])),
    "Spring": dict(zip(professors,  [ 4,  3,  4])),
}

# Course preferences for each professor
course_pref = {                        #           M   F   P
    "P1": dict(zip(courses,        [ 6,  5,  4])),
    "P2": dict(zip(courses,        [ 4,  6,  5])),
    "P3": dict(zip(courses,        [ 5,  4,  6])),
}

# ------------------------------------------------------------------
# 2. Build the directed network
# ------------------------------------------------------------------
G = nx.DiGraph()

# (a) Source σ  →  course nodes (capacity 4)
G.add_node("σ")
for c in courses:
    G.add_edge("σ", c, capacity=4, label="cap 4")

# (b) Course node  →  (course, semester) nodes
#     capacity = 3, implicit lower bound = 1 (enforces ≥1 section each semester)
for c in courses:
    for s in semesters:
        node = f"{c}_{s[0]}"          # e.g.  M_F  = Marketing in Fall
        G.add_edge(c, node, capacity=3, label="cap 3\nlb 1")

# (c) (course, semester)  →  professor arcs
#     Arc cost = –(semester preference + course preference)
for c in courses:
    for s in semesters:
        src = f"{c}_{s[0]}"
        for p in professors:
            sat = semester_pref[s][p] + course_pref[p][c]
            G.add_edge(src, p, cost=-sat, label=f"{sat}")   # show *positive* utility on the plot

# (d) Professor  →  sink τ (capacity 4)
G.add_node("τ")
for p in professors:
    G.add_edge(p, "τ", capacity=4, label="cap 4")

# ------------------------------------------------------------------
# 3. Manual layout (makes a tidy layered picture)
# ------------------------------------------------------------------
pos = {
    "σ": (0, 0),
    "M": (1,  2), "F": (1, 0), "P": (1, -2),

    "M_F": (2,  2.6), "M_S": (2, 1.4),
    "F_F": (2,  0.6), "F_S": (2, -0.6),
    "P_F": (2, -1.4), "P_S": (2, -2.6),

    "P1": (3,  1.5), "P2": (3, 0), "P3": (3, -1.5),
    "τ":  (4, 0),
}

# ------------------------------------------------------------------
# 4. Draw the network
# ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_title("Minimum‑Cost Network Flow Representation", pad=15)

# Nodes
nx.draw_networkx_nodes(G, pos, node_color="#D4E6F1",
                       node_size=1400, edgecolors="k", ax=ax)
nx.draw_networkx_labels(G, pos, font_size=11, font_weight="bold", ax=ax)

# Directed edges
nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle="->", ax=ax)

# Edge labels (show utilities; offset every other label to avoid overlap)
edge_labels = {}
for (u, v, data) in G.edges(data=True):
    text = data.get("label", "")
    # Only display the satisfaction values; hide capacity text to keep the figure clean
    edge_labels[(u, v)] = text if text.isdigit() else ""

# Slight manual displacement for readability
label_pos = {}
for i, (u, v) in enumerate(edge_labels.keys()):
    x_mid = (pos[u][0] + pos[v][0]) / 2
    y_mid = (pos[u][1] + pos[v][1]) / 2
    offset = 0.1 if i % 2 == 0 else -0.1
    label_pos[(u, v)] = (x_mid + offset, y_mid + offset)

nx.draw_networkx_edge_labels(G, label_pos, edge_labels=edge_labels,
                             font_color="firebrick", font_size=9, ax=ax)

ax.set_axis_off()
st.pyplot(fig)

# ------------------------------------------------------------------
# 5. Sidebar description
# ------------------------------------------------------------------
with st.sidebar:
    st.header("ℹ️  Model notes")
    st.markdown(
        """
* **σ → course nodes**: 4 sections per course.  
* **course → (course, semester)**: capacity 3, implicit lower bound 1 implements  
  “each course offered ≥ 1 time per semester”.  
* **(course, semester) → professor**: arc **cost** = –(semester pref + course pref).  
  In the plot we show the **positive satisfaction** instead.  
* **professor → τ**: each professor teaches exactly 4 sections.  

The optimal solution yields a total satisfaction of **121**.
"""
    )
