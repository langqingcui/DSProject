class Course:    
    def __init__(self, course_name=None, credits=None, prerequisites=None, semester=None):
        self.course_name = course_name
        self.credits = credits
        self.prerequisites = prerequisites
        self.semester = semester
        
    def set_course_name(self, course_name):
        self.course_name = course_name
        
    def set_course_credits(self, credits):
        self.credits = credits
    
    def set_semester(self, semester):
        self.semester = semester
        
    def set_prerequisites(self, prerequisites):
        self.prerequisites = prerequisites
        
    def __str__(self):
        return f"Course Name: {self.course_name}\nPrerequisites: {self.prerequisites}\nSemester: {self.semester}\n"
    