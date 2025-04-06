# Zuma Game Solver – AI Search Project

This project was implemented as part of a university Artificial Intelligence course.  
It explores classical search algorithms to solve a variant of the puzzle game Zuma.

![zuma](https://imgur.com/a/b6BBf4J)

---

## Problem Summary

You are given a row of colored balls and a sequence of additional balls (the "ammo") that can be inserted into the row. The objective is to eliminate all balls from the row by strategically inserting ammo so that groups of 3 or more of the same color are created and removed.

Each turn, the agent may:
- Insert the first ball from the ammo into any position in the row
- Discard the current ammo ball and move to the next one

Chain reactions can occur: inserting one ball may trigger multiple group eliminations.

The challenge is to find a minimal sequence of actions that clears the row, or determine that it's impossible.

---

## Problem Modeling

- State: A tuple of `(row, ammo)`
- Actions: Insert at position `i`, or `Discard`
- Successor Function: Generates all valid next states
- Goal: Row is empty (`len(row) == 0`)
- Heuristic: Number of remaining groups after best possible insertion

---

## Search Algorithms

The implementation supports:
- Greedy Best-First Search
- A* Search

---

## File Overview

| File | Description |
|------|-------------|
| `zuma_problem.py` | Main Zuma problem class: state, successor, goal, heuristic |
| `search.py` | General-purpose search algorithms (BFS, A*, etc.) |
| `utils.py` | Compatibility and helper functions |
| `check_zuma.py` | Test script to run and evaluate the solution |

---

## Run Instructions

```bash
python3 check_zuma.py
```
---

## Example

```python
create_zuma_problem((1,2,2,1,3,3,1,4,4), (2,3,4))
```

This function creates and returns a `ZumaProblem` instance using a given game configuration.

- The first argument `(1,2,2,1,3,3,1,4,4)` represents the **initial board**, a row of colored balls.  
  Each number corresponds to a color:
  - 1 = Red
  - 2 = Blue
  - 3 = Green
  - 4 = Yellow

- The second argument `(2,3,4)` represents the **ammo queue** — the sequence of balls available for insertion, from left to right.

The returned object is ready to be used with a search algorithm (such as A* or Greedy Best-First Search) to find a solution that removes all balls from the row.

