#!/usr/bin/python3

import sys
import fileinput
import os.path
from collections import namedtuple
import time
import collections

class Graph:
	# Graph class is implemented as a dictionary with vertices as keys and a list of neighbor nodes as values
	def __init__(self, graph_dict):
		# Constructor takes a dictionary as argument, builds a dictionary without disconnected vertices
		# and assigns it to the underlying dict of the class
		self.__graph_dict = graph_dict
		g = {}
		for v in self.__graph_dict:
			if self.__graph_dict[v]: #vertex has neighbors, ie, not disconnected
				g[v] = self.__graph_dict[v]
		self.__graph_dict = g
	def vertices(self):
		# Returns a list of connected vertices in the graph
		return list(self.__graph_dict.keys())
	def edges(self):
		# Returns a list of edges (pairs of vertices) in the graph
		edges = []
		for vertex in self.__graph_dict:
			for n in self.__graph_dict[vertex]:
				if {vertex, n} not in edges:
					edges.append({vertex, n})
	'''
	# Used for debugging
	def print_graph(self):
		# Prints the underlying dict of the class
		print (self.__graph_dict)'''		
	def __str__(self):
		# Prints a list of vertices and edges in the graph
		s = "V: "
		for vertex in self.vertices():
			s += str(vertex) + " "
		s += "\nE: "
		for edge in self.edges():
			s += str(edge) + " "
		return s
	def calc_avg_degree(self, opfile):
		# Returns a formatted string of the average degree of the graph
		n = 0
		deg = 0
		x = "0.00"
		for v in self.__graph_dict:
			n +=1 
			deg += len(self.__graph_dict[v])
			f = deg/n
			x = "%.2f" % f
		return x

def build_graph(dict_tweets):
	# Returns a Graph object by building a dictionary with vertices as keys and neighbor nodes as values
	# from the input dictionary of NT_tweet named tuples and timestamps
	vertices = set()
	g = {}
	for key, nt in dict_tweets.items():
		if len(nt.hashtags) >1:
			vertices.update(nt.hashtags)
	for v in list(vertices):
		neighbors = set()
		for key, nt in dict_tweets.items():
			if v in nt.hashtags:
				neighbors.update(set(nt.hashtags))
		neighbors.discard(v)
		g[v] = list(neighbors)
	graph = Graph(g)
	return graph

def evict_old_tweets(dict_tweets, new_ts):
	# Returns a tuple with two values in it
	# The first is a dictionary from which tweets older than 60 seconds have been removed
	# The second contains the oldest timestamp value in the result dictioanry
	result = {}
	i  = 0
	oldest = new_ts
	for k, nt in dict_tweets.items():
		if new_ts - nt.ts <= 60:
			result[i] = NT_tweet(nt.hashtags, nt.ts)
			i += 1
			if nt.ts <= oldest:
				oldest = nt.ts
	return (result, oldest)

# First function to be executed - Will possibly run faster when last print statement is removed/commented
def main():
	# Reads input file and writes feauture 2 into output file as specified in cmd arguments
	if(os.path.isfile(sys.argv[1])):
		ipfile = open(sys.argv[1], "r")
	else:
		# Terminates if input file path is invalid
		print("Invalid input path: ", sys.argv[1])
		exit(0)
	opfile = open(sys.argv[2], "w+")
	dict_tweets = {}
	counter = 0
	oldest_ts = None
	output_str = ""
	for line in ipfile:
		tags = []
		for word in line.split():
			# Hashtag case sensitivity - convert all characters to uppercase
			if word.startswith("#"):
				word = word.upper()
				tags.append(word)
		p = line.find("(timestamp: ")
		if p != -1:
			# A line with valid tweet and timestamp has been found
			newest_ts = (time.mktime(time.strptime(line[p+len("(timestamp: "):-2],"%a %b %d %H:%M:%S +0000 %Y")))
			if oldest_ts is None:
				# First tweet/line to be read from the file
				oldest_ts = newest_ts
			# Save hashtags and timestamp in dictionary using NT_tweet (named tuple has list of hashtags and timestamp)
			dict_tweets[counter] = NT_tweet(set(tags), newest_ts)
			(dict_tweets, oldest_ts) = evict_old_tweets(dict_tweets, newest_ts)
			graph = build_graph(dict_tweets)
			# Build the output string to be written into file
			output_str += graph.calc_avg_degree(opfile) + "\n"
			counter += 1
			print("Feature file 2: Processed ", counter, " tweets")
	opfile.write(output_str)
	ipfile.close()
	opfile.close()

# Execution starts here
NT_tweet = namedtuple ("NT_tweet","hashtags ts")
main()
