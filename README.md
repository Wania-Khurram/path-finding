# Dynamic Pathfinding Agent - FAST CFD

A real-time visualization tool built with **Pygame** to demonstrate **A*** and **Greedy Best-First Search** algorithms. This agent navigates a grid-based environment that can change dynamically, forcing the agent to recalculate paths on the fly.



## 🚀 Key Features
* **Dual Algorithms:** Switch between **A*** (optimal) and **Greedy BFS** (speed-focused).
* **Distance Metrics:** Toggle between **Manhattan** and **Euclidean** heuristics.
* **Dynamic Obstacles:** Spawns random walls during the agent's movement, triggering an immediate re-pathing sequence.
* **Real-time Metrics:** Sidebar tracking for nodes visited, path cost, and execution time in milliseconds.
* **Map Generation:** Instant 30% density random map generation.

---

## 🛠️ Controls

| Key | Action |
| :--- | :--- |
| **Left Click** | Place Start (1st), Goal (2nd), and Walls (Subsequent) |
| **SPACE** | Execute search and start agent movement |
| **G** | Toggle Algorithm (A* / Greedy) |
| **M** | Toggle Heuristic (Manhattan / Euclidean) |
| **R** | Generate Random Map (30% density) |
| **C** | Clear Grid and Reset Metrics |

---

## 🧪 Technical Details

The agent uses a **Priority Queue** to manage the frontier. In "Dynamic Mode," if an obstacle is spawned on the current calculated path, the agent halts and runs the search algorithm again from its current position to the goal.

### Heuristics Used:

* **Manhattan Distance:** $d = |x_1 - x_2| + |y_1 - y_2|$
* **Euclidean Distance:** $d = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$

## 🧠 Core Algorithms
The agent evaluates the "best" next step using a Priority Queue. The distinction between the two modes lies in the **Cost Function $f(n)$**:

1.  **A* Search:** $f(n) = g(n) + h(n)$. 
    * $g(n)$ is the actual cost from start to node $n$.
    * $h(n)$ is the heuristic estimate to the goal.
    * *Result:* Guarantees the shortest path.
2.  **Greedy Best-First Search:** $f(n) = h(n)$.
    * Ignores the path cost $g(n)$ and only looks at the heuristic.
    * *Result:* Faster execution, but often results in sub-optimal paths.



### ⚡ Dynamic Re-routing Logic
The agent doesn't just follow a static line. During the traversal phase:
1.  **Step-by-Step Movement:** The agent moves one node at a time along the `path` list.
2.  **Environmental Flux:** There is a 10% probability per step that a new wall spawns randomly on the grid.
3.  **Path Validation:** After a wall spawns, the agent checks if that wall occupies a node in the current `path`.
4.  **Instant Re-calculation:** If the path is blocked, the `search_algorithm` is re-invoked from the agent's current coordinates to the original goal, ensuring the agent adapts to the new landscape.

### 📊 Performance Metrics
The UI Sidebar provides real-time telemetry:
* **Nodes Visited:** Measures the exploration efficiency (lower is usually better).
* **Path Cost:** The number of steps from start to finish.
* **Time:** Execution time of the search in milliseconds (ms), highlighting the performance gap between Manhattan and Euclidean heuristics.

---

### 🎨 Visual Language
* 🟦 **Blue:** Start Point / Agent
* 🟪 **Purple:** Target Goal
* ⬛ **Black:** Impassable Obstacles
* 🟨 **Yellow:** Frontier (Open Set)
* 🟥 **Red:** Visited Nodes (Closed Set)
* 🟩 **Green:** Calculated Optimal Path
### Output
<img width="900" height="564" alt="image" src="https://github.com/user-attachments/assets/62f083b0-263b-450d-a5f8-8c66b6565a68" />

## 📦 Requirements

* Python 3.x
* Pygame

```bash
pip install pygame
