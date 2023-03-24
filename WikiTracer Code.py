import os
import sys
import requests
from bs4 import BeautifulSoup
from typing import List, Tuple
from collections import Counter
from math import sqrt
from heapq import nlargest
from urllib.parse import urljoin
import concurrent.futures
from functools import lru_cache
import heapq
from collections import deque
import heapq

@lru_cache(maxsize=None)
def get_wiki_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    wiki_links = [link.get('href') for link in links
                  if link.get('href') and link.get('href').startswith('/wiki/')
                  and 'http' not in link.get('href')
                  and ':' not in link.get('href')]
    full_links = [urljoin(url, link) for link in wiki_links]
    return full_links

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, start, end, weight):
        if start not in self.graph:
            self.graph[start] = {}
        self.graph[start][end] = weight

    def __contains__(self, node):
        return node in self.graph

    def return_edges(self, node):
        return self.graph.get(node, {})

    def __iter__(self):
        return iter(self.graph)

    def print_graph(self):
        if not self.graph:
            print('Graph is empty')
            return
        for node, neighbors in self.graph.items():
            print(f'{node}:')
            for neighbor, weight in neighbors.items():
                print(f'  -> {neighbor}, weight: {weight}')

def find_path(start, end, n, weight=1, Wikiholder=None):
    if Wikiholder is None:
        Wikiholder = Graph()

    visited = set()
    queue = deque([(start, 0)])

    while queue:
        current_url, depth = queue.popleft()

        if depth > n:
            break

        if current_url not in visited:
            visited.add(current_url)
            possible_links = get_wiki_links(current_url)

            for link in possible_links:
                Wikiholder.add_edge(current_url, link, weight)

                if link == end:
                    visited.add(link)
                    return Wikiholder

                if link not in visited:
                    queue.append((link, depth + 1))

    Wikiholder.add_edge(end, end, 1)
    return Wikiholder
# use the return_edges method in order to get the neighbors of the node and find the shortest path from start to end node.
# Depth First Search Recursive Backtracking Solution to Find Path

def path(start, end, Wikiholder, current_path=None, visited=None):
    if visited is None:
        visited = set()

    if current_path is None:
        current_path = []

    if start not in visited:
        current_path.append(start)
        visited.add(start)

        if start == end:
            return list(current_path)
        else:
            neighbors = Wikiholder.return_edges(start)
            for neighbor in neighbors:
                if neighbor not in visited:
                    result = path(neighbor, end, Wikiholder, current_path, visited)
                    if result:
                        return result

        visited.remove(start)
        current_path.pop()

    return None

              

def main(start, end):
    Wikiholder = find_path(start, end, 500, weight=1)
    shortest_path_result = path(start, end, Wikiholder)
    print(f'Shortest path: {shortest_path_result}')

if __name__ == "__main__":
    main("https://en.wikipedia.org/wiki/World_War_II", "https://en.wikipedia.org/wiki/Philosophy")


