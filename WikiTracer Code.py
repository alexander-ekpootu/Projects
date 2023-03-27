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
    queue = deque([(start, 0, None)])  # Add a third element for the parent node

    parent_map = {}  # Dictionary to store parent nodes

    while queue:
        current_url, depth, parent = queue.popleft()

        if depth > n:
            break

        if current_url not in visited:
            visited.add(current_url)
            possible_links = get_wiki_links(current_url)

            # Store the parent node for the current_url
            if parent is not None:
                parent_map[current_url] = parent
                Wikiholder.add_edge(parent, current_url, weight)

            for link in possible_links:
                if link == end:
                    # When the end node is found, reconstruct the path using the parent_map
                    path = [link]
                    current_node = current_url
                    while current_node != start:
                        path.append(current_node)
                        current_node = parent_map[current_node]
                    path.append(start)
                    path.reverse()
                    return Wikiholder, path

                if link not in visited:
                    queue.append((link, depth + 1, current_url))

    Wikiholder.add_edge(end, end, 1)
    return Wikiholder, None
          

def main(start, end):
    Wikiholder, path_result = find_path(start, end, 500, weight=1)
    if path_result:
        print(f'Path found: {path_result}')
    else:
        print('Path not found')

if __name__ == "__main__":
    main("https://en.wikipedia.org/wiki/World_War_II", "https://en.wikipedia.org/wiki/Luigi_Capello")


