import zuma_problem
import search


def run_problem(func, targs=(), kwargs=None):
    if kwargs is None:
        kwargs = {}
    result = (-3, "default")
    try:
        result = func(*targs, **kwargs)

    except Exception as e:
        result = (-3, e)
    return result


# check_problem: problem, search_method, timeout
# timeout_exec: search_method, targs=[problem], timeout_duration=timeout
def solve_problems(problem, algorithm):
    for row in problem:
        print(row)

    try:
        p = zuma_problem.create_zuma_problem(problem)
    except Exception as e:
        print("Error creating problem: ", e)
        return None

    if algorithm == "gbfs":
        result = run_problem((lambda p: search.greedy_best_first_graph_search(p, p.h)),targs=[p])
    else:
        result = run_problem((lambda p: search.astar_search(p, p.h)), targs=[p])

    if result and isinstance(result[0], search.Node):
        solve = result[0].path()[::-1]
        solution = [pi.action for pi in solve][1:]
        print(len(solution), solution)
    else:
        print("no solution")


problem1 = ((1, 1, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1), (1, 2, 3, 4, 1, 2, 3, 4))
problem2 = ((3, 3, 1, 4, 2, 4, 4, 1, 2, 4, 3), (2, 2, 2, 2, 4, 4, 1, 3))


def main():
    algorithm1 = "gbfs"  
    algorithm2 = "astar" 

    print("Algorithm 1: Greedy Best First Search")
    solve_problems(problem1, algorithm1)
    print("Algorithm 2: A* Search")
    solve_problems(problem1, algorithm2)
    print("Algorithm 1: Greedy Best First Search")
    solve_problems(problem2, algorithm1)
    print("Algorithm 2: A* Search")
    solve_problems(problem2, algorithm2)



if __name__ == '__main__':
    main()
