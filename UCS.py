from collections import defaultdict



def generateDirectedGraph(edges):
    graph = defaultdict(dict)
    for u, v, dist in edges:
        graph[u][v] = dist
        graph[v][u] = dist
    return graph
def dijkstra(graph, src):
    # The only criterium of adding a node to queue is if its distance has changed at the current step.
    queue = [src]
    minDistances = {v: float("inf") for v in graph}
    minDistances[src] = 0
    predecessor = {}
    while queue:
        currentNode = queue.pop(0)
        for neighbor in graph[currentNode]:
            # get potential newDist from start to neighbor
            newDist = minDistances[currentNode] + graph[currentNode][neighbor]

            # if the newDist is shorter to reach neighbor updated to newDist
            if newDist < minDistances[neighbor]:
                minDistances[neighbor] = min(newDist, minDistances[neighbor])
                queue.append(neighbor)
                predecessor[neighbor] = currentNode
    return minDistances, predecessor
def UCS_code(graph, src, dest):
    minDistances, predecessor = dijkstra(graph, src)
    path = []
    currentNode = dest
    while currentNode != src:
        if currentNode not in predecessor:
            print("Path not reachable")
            break
        else:
            path.insert(0, currentNode)
            currentNode = predecessor[currentNode]
    path.insert(0, src)
    
    if dest in minDistances and minDistances[dest] != float("inf"):
        # print('Shortest distance is ' + str(minDistances[dest]))
        return '-'.join(path),str(minDistances[dest])+' km'


