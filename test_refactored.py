"""
Test script to verify refactored code works correctly
"""
from University_Course_Registration_System_Refactored import (
    Student, Course, Lecturer, Registrar
)

def test_basic_functionality():
    """Test that refactored code maintains original functionality"""
    print("Testing refactored code...")
    
    # Create instances
    student = Student("S001", "Alice", "alice@uni.com")
    course = Course("CS101", "Intro to Programming", 3)
    lecturer = Lecturer("L001", "Dr. Smith", "smith@uni.com", "CS")
    registrar = Registrar()
    
    # Test registration
    assert not student.is_registered_for("CS101"), "Student should not be registered initially"
    course.enroll_student(student)
    assert student.is_registered_for("CS101"), "Student should be registered after enrollment"
    
    # Test grade assignment
    student.add_grade("CS101", "A")
    assert student.grades["CS101"] == "A", "Grade should be assigned"
    
    # Test attendance
    student.add_attendance("CS101", [True, True, False, True])
    assert "CS101" in student._attendance, "Attendance should be recorded"
    
    # Test lecturer assignment
    lecturer.assign_course(course)
    assert course.lecturer == lecturer, "Lecturer should be assigned to course"
    
    # Test registrar
    registrar.add_student(student)
    registrar.add_course(course)
    registrar.add_lecturer(lecturer)
    
    assert len(registrar.get_students()) == 1, "Registrar should have 1 student"
    assert len(registrar.get_courses()) == 1, "Registrar should have 1 course"
    assert len(registrar.get_lecturers()) == 1, "Registrar should have 1 lecturer"
    
    print("✅ All tests passed!")

if __name__ == "__main__":
    test_basic_functionality()

