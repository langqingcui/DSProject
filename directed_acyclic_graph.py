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
    
    def get_nodes(self):
        return self.dag.nodes
    
    def topological_division(self, max_credits_per_semester):
        if not self.is_dag():
            return None

        # List to store nodes at each division
        divisions = []
        
        semester = 1

        while True:
            # Find nodes with in-degrees of 0
            zero_in_degree_nodes = [node for node, in_degree in self.dag.in_degree() if in_degree == 0]

            # Break if there are no nodes with in-degree of 0
            # Indicating the process has completed
            if not zero_in_degree_nodes:
                break
            
            # Initialize variables to keep track of credits and courses in the current semester
            current_semester_credits = 0
            current_semester_courses = []
            
            max_credits = max_credits_per_semester[semester - 1]

            for node in zero_in_degree_nodes:
                # Calculate the total credits of courses in the current semester
                total_credits_in_semester = sum([course.credits for course in current_semester_courses])

                # Check if adding the next course will exceed the max credit limit
                if total_credits_in_semester + node.credits <= max_credits:
                    # Add the course to the current semester
                    current_semester_courses.append(node)
                    current_semester_credits += node.credits
                else:
                    break  # Break if the credit limit is reached
            

            # Remove the courses that are already planned for current semester
            self.dag.remove_nodes_from(current_semester_courses)

            # Store the current semester's courses in divisions
            divisions.append(current_semester_courses)
            
            semester += 1

        return divisions
       

    def topological_division_adjusting_courses(self, max_credits_per_semester):
        if not self.is_dag():
            return None

        divisions = [[] for _ in range(8)]
        current_semester_credits = [0 for _ in range(8)]

        # 先处理已经设置了学期的课程
        for course in list(self.dag.nodes):
            if course.semester is not None:
                divisions[course.semester - 1].append(course)
        
        courses_with_set_semesters = [course for course in self.dag.nodes if course.semester is not None]

        # 对剩余课程执行拓扑排序
        for semester, max_credits in enumerate(max_credits_per_semester, start=1):
            current_semester_credits[semester - 1] = sum(course.credits for course in divisions[semester - 1])

        semester = 1

        while semester <= 8:
            zero_in_degree_nodes = [node for node, in_degree in self.dag.in_degree() if in_degree == 0]

            print(f"Semester {semester} zero in-degree courses:")
            for node in zero_in_degree_nodes:
                print(node.course_name)
                
            if not zero_in_degree_nodes:
                break  # 退出条件: 没有可分配的课程
            
            max_credits = max_credits_per_semester[semester - 1]
            
            for course in courses_with_set_semesters:
                # if course.semester == semester:
                print(f"111, {course}")
                if course in zero_in_degree_nodes:
                    zero_in_degree_nodes.remove(course)
                    # self.dag.remove_node(course)
                    # courses_with_set_semesters.remove(course)
                    
                    


            for node in list(zero_in_degree_nodes):
                if current_semester_credits[semester - 1] + node.credits <= max_credits:
                    divisions[semester - 1].append(node)
                    current_semester_credits[semester - 1] += node.credits
                    self.dag.remove_node(node)
                else:
                    break
                
            for course in list(courses_with_set_semesters):
                if course.semester == semester:
                    self.dag.remove_node(course)
                    courses_with_set_semesters.remove(course)

            semester += 1
         
        return divisions


                
         
