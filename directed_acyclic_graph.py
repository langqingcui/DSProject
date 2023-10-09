import networkx as nx
import json
from course import Course

class DAG:
    def __init__(self):
        self.dag = nx.DiGraph()
        
    def add_course(self, course):
        self.dag.add_node(course)
        
    def add_prerequisite(self, source_course, target_course):
        self.dag.add_edge(source_course, target_course)
        
    def add_courses_from_json(self, json_file):
        try:
            with open(json_file, 'r') as file:
                data = json.load(file)
                for course_info in data["computer_science_courses"]:
                    course = Course()
                    course.set_course_name(course_info["course_name"])
                    course.set_course_credits(course_info["course_credits"])
                    course.set_prerequisites(course_info["prerequisites"])
                    self.add_course(course)
                    for prereq_name in course.prerequisites:
                        prereq = next((c for c in self.dag.nodes if c.course_name == prereq_name), None)
                        if prereq:
                            self.add_prerequisite(prereq, course)
        except FileNotFoundError:
            print(f"File '{json_file} not found!")

    def is_dag(self):
        return nx.is_directed_acyclic_graph(self.dag)
    
    def topological_division(self):
        if not self.is_dag():
            return None

        # List to store nodes at each division
        divisions = []

        # Initialize variables to keep track of credits and courses in the current semester
        current_semester_credits = 0
        current_semester_courses = []

        while True:
            # Find nodes with in-degrees of 0
            zero_in_degree_nodes = [node for node, in_degree in self.dag.in_degree() if in_degree == 0]

            # Break if there are no nodes with in-degree of 0
            # Indicating the process has completed
            if not zero_in_degree_nodes:
                break

            # Calculate the total credits of courses in the current semester
            total_credits_in_semester = sum([course.credits for course in current_semester_courses])

            # Check if adding the next course will exceed the 20-credit limit
            if total_credits_in_semester + zero_in_degree_nodes[0].credits <= 20:
                # Add the course to the current semester
                current_semester_courses.append(zero_in_degree_nodes[0])
                current_semester_credits += zero_in_degree_nodes[0].credits
            else:
                # If adding the course would exceed the credit limit, start a new semester
                divisions.append(current_semester_courses)
                current_semester_courses = [zero_in_degree_nodes[0]]
                current_semester_credits = zero_in_degree_nodes[0].credits

            # Remove the course from the graph
            self.dag.remove_node(zero_in_degree_nodes[0])

        # Add the last semester's courses to the divisions
        if current_semester_courses:
            divisions.append(current_semester_courses)

        return divisions
