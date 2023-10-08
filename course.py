import json

class Course:    
    def __init__(self, course_name=None, prerequisites=None, semester=None):
        self.course_name = course_name
        self.prerequisites = prerequisites
        self.semester = semester
        
    def set_course_name(self, course_name):
        self.course_name = course_name
    
    def set_semester(self, semester):
        self.semester = semester
        
    def set_prerequisites(self, prerequisites):
        self.prerequisites = prerequisites
        
    def __str__(self):
        return f"Course Name: {self.course_name}\nPrerequisites: {self.prerequisites}\nSemester: {self.semester}\n"

def create_course_object_from_json(json_file):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
            
            course_objects = []
            for course_info in data["computer_science_courses"]:
                course = Course()
                course.set_course_name(course_info["course_name"])
                course.set_prerequisites(course_info["prerequisites"])
                course_objects.append(course)
                
            return course_objects
    except FileNotFoundError:
        print(f"File '{json_file} not found!")
        return []
    