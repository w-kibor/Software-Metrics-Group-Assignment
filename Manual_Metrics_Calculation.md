# Manual Metrics Calculation Guide

## How to Calculate Metrics

### Using Python Tools

#### Option 1: Using Radon (Recommended)
```bash
pip install radon

# Calculate Cyclomatic Complexity
radon cc University_Course_Registration_System.py

# Calculate Maintainability Index
radon mi University_Course_Registration_System.py

# Calculate Raw Metrics (LOC, LLOC, etc.)
radon raw University_Course_Registration_System.py
```

#### Option 2: Using Lizard
```bash
pip install lizard

# Comprehensive analysis
lizard University_Course_Registration_System.py
```

#### Option 3: Using Pylint
```bash
pip install pylint

# Full analysis with complexity
pylint --reports=yes University_Course_Registration_System.py
```

### Manual Calculation Examples

#### Cyclomatic Complexity Formula:
CC = 1 + number of decision points

Decision points include:
- `if` statements
- `elif` statements  
- `while` loops
- `for` loops
- `except` clauses
- Boolean operators (`and`, `or`)

**Example for `calculate_performance()`:**
- Base: 1
- 5 `elif` statements: +5
- 1 `if` statement: +1
- 1 `elif` statement: +1
- **Total CC = 8**

#### Coupling Between Objects (CBO):
Count the number of other classes a class directly uses or is used by.

**Example for `Lecturer`:**
- Uses `Person` (inheritance)
- Uses `Course` (assign_course method)
- Uses `Student` (submit_grades method)
- **CBO = 3**

#### Depth of Inheritance Tree (DIT):
Count the number of classes from the current class to the root.

**Example for `Student`:**
- `Student` → `Person` → root
- **DIT = 1**

#### Lack of Cohesion of Methods (LCOM):
LCOM = 1 - (average method cohesion)

Where cohesion is measured by shared instance variables.

**Simplified calculation:**
- If methods share many attributes: Low LCOM (good)
- If methods share few attributes: High LCOM (bad)

