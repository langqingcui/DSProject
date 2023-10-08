class course:    
    def __init__(self, course_code=None, course_name=None, prerequisites=None, semester=None):
        self.course_code = course_code
        self.course_name = course_name
        self.prerequisites = prerequisites
        self.semester = semester
        
    def set_course_code(self, course_code):
        self.course_code = course_code
        
    def set_course_name(self, course_name):
        self.course_name = course_name
    
    def set_semester(self, semester):
        self.semester = semester
        
    def set_prerequisites(self, prerequisites):
        self.prerequisites = prerequisites
        