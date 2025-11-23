# University Course Registration System - Assignment Solution

This folder contains the complete solution for the Metrics-Based Refactoring assignment.

## Files Included

1. **University_Course_Registration_System.py** - Original code (provided)
2. **University_Course_Registration_System_Refactored.py** - Refactored code with improvements
3. **Assignment_Analysis.md** - Complete analysis document (Parts A, B, and C)
4. **metric_analyzer.py** - Python script to calculate metrics automatically
5. **Manual_Metrics_Calculation.md** - Guide for manual metric calculation
6. **test_refactored.py** - Test script to verify refactored code functionality
7. **README.md** - This file

## Quick Start

### Running the Original Code
```bash
python University_Course_Registration_System.py
```

### Running the Refactored Code
```bash
python University_Course_Registration_System_Refactored.py
```

### Calculating Metrics
```bash
# Using the custom analyzer
python metric_analyzer.py University_Course_Registration_System.py

# Or using radon (recommended)
pip install radon
radon cc University_Course_Registration_System.py
radon cc University_Course_Registration_System_Refactored.py
```

### Testing the Refactored Code
```bash
python test_refactored.py
```

## Assignment Structure

### Part A: Metric Analysis (8 Marks)
- Cyclomatic Complexity (CC) calculations
- Lines of Code (LOC) analysis
- Coupling Between Objects (CBO)
- Depth of Inheritance Tree (DIT)
- Lack of Cohesion of Methods (LCOM)
- Problem area identification

**See:** `Assignment_Analysis.md` - Part A section

### Part B: Diagnosis (6 Marks)
- Explanation of why metrics indicate problems
- Discussion of coupling and cohesion effects
- Impact on reusability, testability, maintainability

**See:** `Assignment_Analysis.md` - Part B section

### Part C: Refactoring (6 Marks)
- Refactored code with improvements
- Before and after metrics comparison
- Explanation of refactoring techniques

**See:** `Assignment_Analysis.md` - Part C section and `University_Course_Registration_System_Refactored.py`

## Key Improvements Made

1. **Reduced Cyclomatic Complexity**
   - Split `calculate_performance()` (CC=8) into smaller methods (CC=1-3)
   - Created `GradeCalculator`, `AttendanceCalculator`, `PerformanceEvaluator`

2. **Reduced Coupling**
   - Encapsulated attributes with getters/setters
   - Removed direct attribute access
   - Reduced CBO from 3 to 1-2

3. **Improved Cohesion**
   - Separated concerns into dedicated classes
   - Each class has single responsibility
   - Better method organization

4. **Enhanced Encapsulation**
   - Private attributes (`_attribute`)
   - Public getters/setters
   - Controlled access to internal state

## Metrics Summary

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Max CC | 8 | 3 | 62.5% ↓ |
| Avg CC | 1.6 | 1.2 | 25% ↓ |
| Max LOC | 24 | 12 | 50% ↓ |
| CBO (Lecturer) | 3 | 2 | 33% ↓ |
| CBO (Registrar) | 3 | 1 | 67% ↓ |
| Encapsulation | None | Full | ✅ |

## Submission Checklist

- [x] Part A: Metric Analysis completed
- [x] Part B: Diagnosis completed
- [x] Part C: Refactoring completed
- [x] Before/after metrics comparison
- [x] Code comments and documentation
- [ ] Add group members list (to be filled)
- [ ] Add GitHub link (to be filled)

## Notes

- The analysis document (`Assignment_Analysis.md`) contains all required information
- The refactored code maintains the same functionality as the original
- All metrics have been calculated and documented
- Code follows Python best practices and SOLID principles



