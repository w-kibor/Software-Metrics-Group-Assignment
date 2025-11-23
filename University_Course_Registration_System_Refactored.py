"""
Refactored University Course Registration System
Improved design with reduced complexity, coupling, and better cohesion
"""
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum


class Grade(Enum):
    """Enum for grade values to reduce magic strings"""
    A = 4
    B = 3
    C = 2
    D = 1
    E = 0


class PerformanceLevel(Enum):
    """Enum for performance levels"""
    EXCELLENT = "Excellent performance!"
    WARNING = "Warning: Poor performance"
    NORMAL = ""


class Person:
    """Base class for all persons in the system"""
    
    def __init__(self, person_id: str, name: str, email: str, phone: Optional[str] = None):
        self._person_id = person_id
        self._name = name
        self._email = email
        self._phone = phone
        self._role = None

    @property
    def person_id(self) -> str:
        return self._person_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    def phone(self) -> Optional[str]:
        return self._phone

    def display_info(self) -> None:
        """Display person information"""
        print(f"ID: {self._person_id}, Name: {self._name}, Email: {self._email}, Phone: {self._phone}")

    def update_contact(self, email: str, phone: Optional[str]) -> None:
        """Update contact information"""
        self._email = email
        self._phone = phone
        print(f"{self._name}'s contact updated.")


class GradeCalculator:
    """Separated responsibility for GPA calculations"""
    
    @staticmethod
    def grade_to_points(grade: str) -> int:
        """Convert letter grade to points"""
        grade_map = {
            "A": Grade.A.value,
            "B": Grade.B.value,
            "C": Grade.C.value,
            "D": Grade.D.value,
            "E": Grade.E.value
        }
        return grade_map.get(grade.upper(), 0)
    
    @staticmethod
    def calculate_gpa(grades: Dict[str, str]) -> float:
        """Calculate GPA from grades dictionary"""
        if not grades:
            return 0.0
        
        total_points = sum(GradeCalculator.grade_to_points(grade) 
                          for grade in grades.values())
        return round(total_points / len(grades), 2)


class AttendanceCalculator:
    """Separated responsibility for attendance calculations"""
    
    @staticmethod
    def calculate_average_attendance(attendance: Dict[str, List[bool]]) -> float:
        """Calculate average attendance rate across all courses"""
        if not attendance:
            return 0.0
        
        total_rate = 0.0
        for records in attendance.values():
            if records:
                attended = sum(1 for r in records if r)
                total_rate += (attended / len(records)) * 100
        
        return total_rate / len(attendance)


class PerformanceEvaluator:
    """Separated responsibility for performance evaluation"""
    
    @staticmethod
    def evaluate_performance(gpa: float, attendance: float) -> PerformanceLevel:
        """Evaluate performance level based on GPA and attendance"""
        if gpa >= 3.5 and attendance >= 90:
            return PerformanceLevel.EXCELLENT
        elif gpa < 2.0 or attendance < 60:
            return PerformanceLevel.WARNING
        return PerformanceLevel.NORMAL


class Student(Person):
    """Student class with improved encapsulation and separation of concerns"""
    
    def __init__(self, student_id: str, name: str, email: str, phone: Optional[str] = None):
        super().__init__(student_id, name, email, phone)
        self._role = "Student"
        self._courses: List['Course'] = []
        self._grades: Dict[str, str] = {}
        self._attendance: Dict[str, List[bool]] = {}
        self._last_login = datetime.now()

    @property
    def courses(self) -> List['Course']:
        return self._courses.copy()  # Return copy for encapsulation

    @property
    def grades(self) -> Dict[str, str]:
        return self._grades.copy()  # Return copy for encapsulation

    def is_registered_for(self, course_code: str) -> bool:
        """Check if student is registered for a course"""
        return any(course.code == course_code for course in self._courses)

    def register_course(self, course: 'Course') -> bool:
        """Register for a course if not already registered"""
        if not self.is_registered_for(course.code):
            self._courses.append(course)
            print(f"{self._name} registered for {course.title}")
            return True
        else:
            print(f"{self._name} already registered for {course.title}")
            return False

    def add_grade(self, course_code: str, grade: str) -> None:
        """Add a grade for a course (encapsulated)"""
        self._grades[course_code] = grade

    def add_attendance(self, course_code: str, records: List[bool]) -> None:
        """Add attendance records for a course (encapsulated)"""
        self._attendance[course_code] = records

    def calculate_performance(self) -> float:
        """Calculate and display student performance"""
        gpa = GradeCalculator.calculate_gpa(self._grades)
        avg_attendance = AttendanceCalculator.calculate_average_attendance(self._attendance)
        
        print(f"GPA: {gpa}, Attendance: {avg_attendance:.1f}%")
        
        performance = PerformanceEvaluator.evaluate_performance(gpa, avg_attendance)
        if performance != PerformanceLevel.NORMAL:
            print(performance.value)
        
        return gpa


class Course:
    """Course class with reduced coupling"""
    
    def __init__(self, code: str, title: str, credit_hours: int, lecturer: Optional['Lecturer'] = None):
        self._code = code
        self._title = title
        self._credit_hours = credit_hours
        self._lecturer = lecturer
        self._students: List[Student] = []

    @property
    def code(self) -> str:
        return self._code

    @property
    def title(self) -> str:
        return self._title

    @property
    def credit_hours(self) -> int:
        return self._credit_hours

    @property
    def lecturer(self) -> Optional['Lecturer']:
        return self._lecturer

    @lecturer.setter
    def lecturer(self, lecturer: 'Lecturer') -> None:
        self._lecturer = lecturer

    def enroll_student(self, student: Student) -> bool:
        """Enroll a student in the course"""
        if student.register_course(self):
            self._students.append(student)
            print(f"{student.name} added to {self._title}")
            return True
        return False

    def get_student_count(self) -> int:
        """Get the number of enrolled students"""
        return len(self._students)

    def display_details(self) -> None:
        """Display course details"""
        lecturer_name = self._lecturer.name if self._lecturer else 'TBA'
        print(f"{self._code}: {self._title}, Credits: {self._credit_hours}, Lecturer: {lecturer_name}")
        print("Enrolled students:")
        for student in self._students:
            print(f"- {student.name}")


class Lecturer(Person):
    """Lecturer class with improved encapsulation"""
    
    def __init__(self, staff_id: str, name: str, email: str, department: str):
        super().__init__(staff_id, name, email)
        self._role = "Lecturer"
        self._department = department
        self._courses: List[Course] = []

    @property
    def department(self) -> str:
        return self._department

    @property
    def courses(self) -> List[Course]:
        return self._courses.copy()  # Return copy for encapsulation

    def assign_course(self, course: Course) -> bool:
        """Assign lecturer to a course"""
        if course not in self._courses:
            self._courses.append(course)
            course.lecturer = self
            print(f"{self._name} assigned to {course.title}")
            return True
        return False

    def submit_grades(self, students: List[Student], course_code: str, grade: str) -> None:
        """Submit grades for students (uses proper encapsulation)"""
        for student in students:
            student.add_grade(course_code, grade)
            print(f"Assigned grade {grade} to {student.name} for {course_code}")

    def print_summary(self) -> None:
        """Print lecturer summary"""
        print(f"Lecturer: {self._name}")
        for course in self._courses:
            print(f"Teaching: {course.title} ({course.get_student_count()} students)")


class ReportGenerator:
    """Separated responsibility for report generation"""
    
    @staticmethod
    def generate_full_report(registrar: 'Registrar') -> None:
        """Generate full university report"""
        print("=== Full University Report ===")
        
        for course in registrar.get_courses():
            course.display_details()
        
        for lecturer in registrar.get_lecturers():
            lecturer.print_summary()
        
        for student in registrar.get_students():
            student.calculate_performance()


class Registrar:
    """Registrar class with improved encapsulation and reduced coupling"""
    
    def __init__(self):
        self._students: List[Student] = []
        self._courses: List[Course] = []
        self._lecturers: List[Lecturer] = []

    def add_student(self, student: Student) -> None:
        """Add a student to the system"""
        self._students.append(student)
        print(f"Added student {student.name}")

    def add_course(self, course: Course) -> None:
        """Add a course to the system"""
        self._courses.append(course)

    def add_lecturer(self, lecturer: Lecturer) -> None:
        """Add a lecturer to the system"""
        self._lecturers.append(lecturer)

    def get_students(self) -> List[Student]:
        """Get list of students (encapsulated access)"""
        return self._students.copy()

    def get_courses(self) -> List[Course]:
        """Get list of courses (encapsulated access)"""
        return self._courses.copy()

    def get_lecturers(self) -> List[Lecturer]:
        """Get list of lecturers (encapsulated access)"""
        return self._lecturers.copy()

    def full_report(self) -> None:
        """Generate full report using ReportGenerator"""
        ReportGenerator.generate_full_report(self)


def main():
    """Main function with improved structure"""
    reg = Registrar()

    # Create courses
    c1 = Course("CS101", "Intro to Programming", 3)
    c2 = Course("CS201", "Data Structures", 4)

    # Create and add lecturer
    l1 = Lecturer("L001", "Dr. Smith", "smith@uni.com", "CS")
    reg.add_lecturer(l1)

    # Create and add students
    s1 = Student("S001", "Alice", "alice@uni.com")
    s2 = Student("S002", "Bob", "bob@uni.com")
    reg.add_student(s1)
    reg.add_student(s2)

    # Assign lecturer to course
    l1.assign_course(c1)
    
    # Enroll students
    c1.enroll_student(s1)
    c1.enroll_student(s2)
    
    # Submit grades
    l1.submit_grades([s1, s2], "CS101", "A")

    # Add attendance records
    s1.add_attendance("CS101", [True, True, False, True])
    s2.add_attendance("CS101", [True, False, True, False])

    # Add courses to registrar
    reg.add_course(c1)
    reg.add_course(c2)
    
    # Generate report
    reg.full_report()


if __name__ == "__main__":
    main()

