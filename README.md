# Snake-and-Ladder-Data-Structure-Problem
# 🎲 Snake and Ladder Game (Graph-Based Solver)

This is a Python implementation of the **Snake and Ladder game** using **graph theory algorithms** like **Breadth-First Search (BFS)**, **Depth-First Search (DFS)**, and **Priority Queue (Dijkstra-style)** to find the **minimum number of dice rolls** required to win the game.

> 🔍 Ideal for Data Structures & Algorithms (DSA) learning, game modeling, and graph traversal concepts.

---

## 📌 Problem Statement

The goal is to reach the last cell (typically square 100) from the first square using the fewest number of dice rolls, while accounting for:
- **Snakes** (take you down)
- **Ladders** (lift you up)

Each cell on the board is treated as a node in a graph. Moving from one cell to another (dice roll) is treated as an edge. We explore the shortest path from source to destination using graph traversal algorithms.

---

## 🚀 Features

- Board modeled as a **graph** with 100 nodes
- Supports **Snakes** and **Ladders**
- Implements:
  - ✅ **BFS** (shortest path in unweighted graph)
  - ✅ **DFS** (for exhaustive path exploration)
  - ✅ **Priority Queue** (Dijkstra-style shortest path)
- Clean modular Python code
- Detailed output with minimum dice rolls required

---

## 📦 Tech Stack

- 🐍 Python 3
- 📚 Data Structures: Queue, PriorityQueue, Graph (Adjacency List)
- 🧠 Algorithms: BFS, DFS, Min-Heap

---

## ⚙️ How it Works

1. Define snakes and ladders as a dictionary of positions.
2. Model the board as a graph of 100 nodes.
3. For each algorithm:
   - Simulate dice rolls (1 to 6)
   - Adjust for snakes/ladders
   - Find path from position 1 → 100

---

## 🧪 Sample Snakes & Ladders Input and Output

```python
ladders = {
    1: 38, 4: 14, 9: 30, 21: 42, 28: 76, 71: 67, 80: 99
}
snakes = {
    36: 6, 32: 10, 48: 26, 62: 18, 88: 24, 95: 56, 97: 78
}

output
Shortest path using BFS:
Minimum dice rolls needed: 5
Path: 1 → 2 → 3 → 4 → 14 → 15 → ... → 100
