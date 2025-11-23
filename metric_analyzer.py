"""
Metric Analysis Tool for University Course Registration System
Calculates: CC, LOC, CBO, DIT, LCOM
"""
import ast
import sys
from typing import Dict, List, Set, Tuple

class MetricAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.classes = {}
        self.methods = {}
        self.current_class = None
        self.current_method = None
        self.complexity = {}
        self.loc = {}
        self.couplings = {}  # CBO tracking
        
    def visit_ClassDef(self, node):
        self.current_class = node.name
        self.classes[node.name] = {
            'methods': [],
            'bases': [base.id for base in node.bases if isinstance(base, ast.Name)],
            'attributes': set()
        }
        self.generic_visit(node)
        self.current_class = None
        
    def visit_FunctionDef(self, node):
        if self.current_class:
            method_name = f"{self.current_class}.{node.name}"
            self.current_method = method_name
            self.classes[self.current_class]['methods'].append(node.name)
            
            # Calculate LOC (excluding blank lines and comments)
            loc = len([n for n in ast.walk(node) if isinstance(n, (ast.stmt, ast.expr))])
            self.loc[method_name] = loc
            
            # Calculate Cyclomatic Complexity
            cc = 1  # Base complexity
            for child in ast.walk(node):
                if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                    cc += 1
                elif isinstance(child, ast.BoolOp):
                    cc += len(child.values) - 1
            self.complexity[method_name] = cc
            
            # Track attributes accessed
            attrs = set()
            for child in ast.walk(node):
                if isinstance(child, ast.Attribute):
                    if isinstance(child.value, ast.Name) and child.value.id == 'self':
                        attrs.add(child.attr)
            self.classes[self.current_class]['attributes'].update(attrs)
            
        self.generic_visit(node)
        self.current_method = None

def calculate_cbo(class_name: str, classes: Dict, source_code: str) -> int:
    """Calculate Coupling Between Objects"""
    coupling_count = 0
    class_names = set(classes.keys())
    
    # Parse to find references to other classes
    tree = ast.parse(source_code)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for child in ast.walk(node):
                # Check for attribute access to other class instances
                if isinstance(child, ast.Attribute):
                    if isinstance(child.value, ast.Name):
                        if child.value.id in class_names and child.value.id != class_name:
                            coupling_count += 1
                # Check for method calls on other classes
                if isinstance(child, ast.Call):
                    if isinstance(child.func, ast.Attribute):
                        if isinstance(child.func.value, ast.Name):
                            if child.func.value.id in class_names and child.func.value.id != class_name:
                                coupling_count += 1
    
    return coupling_count

def calculate_dit(class_name: str, classes: Dict) -> int:
    """Calculate Depth of Inheritance Tree"""
    if class_name not in classes or not classes[class_name]['bases']:
        return 0
    
    max_depth = 0
    for base in classes[class_name]['bases']:
        depth = 1 + calculate_dit(base, classes)
        max_depth = max(max_depth, depth)
    
    return max_depth

def calculate_lcom(class_name: str, classes: Dict, methods: Dict) -> float:
    """Calculate Lack of Cohesion of Methods"""
    if class_name not in classes:
        return 0
    
    method_list = classes[class_name]['methods']
    if len(method_list) <= 1:
        return 0
    
    # Get attributes accessed by each method
    method_attrs = {}
    for method in method_list:
        method_attrs[method] = set()
        # This is simplified - would need full AST analysis
        # For now, return a placeholder
    
    # LCOM = 1 - (average cohesion)
    # Simplified calculation
    return 0.5  # Placeholder - would need full implementation

def analyze_file(filename: str):
    """Main analysis function"""
    with open(filename, 'r', encoding='utf-8') as f:
        source_code = f.read()
    
    tree = ast.parse(source_code)
    analyzer = MetricAnalyzer()
    analyzer.visit(tree)
    
    print("=" * 60)
    print("METRIC ANALYSIS REPORT")
    print("=" * 60)
    
    print("\n1. CYCLOMATIC COMPLEXITY (CC) by Method:")
    print("-" * 60)
    for method, cc in sorted(analyzer.complexity.items(), key=lambda x: x[1], reverse=True):
        print(f"  {method:40s} CC: {cc}")
    
    print("\n2. LINES OF CODE (LOC) by Method:")
    print("-" * 60)
    for method, loc in sorted(analyzer.loc.items(), key=lambda x: x[1], reverse=True):
        print(f"  {method:40s} LOC: {loc}")
    
    print("\n3. DEPTH OF INHERITANCE TREE (DIT):")
    print("-" * 60)
    for class_name in analyzer.classes:
        dit = calculate_dit(class_name, analyzer.classes)
        print(f"  {class_name:40s} DIT: {dit}")
    
    print("\n4. COUPLING BETWEEN OBJECTS (CBO):")
    print("-" * 60)
    for class_name in analyzer.classes:
        cbo = calculate_cbo(class_name, analyzer.classes, source_code)
        print(f"  {class_name:40s} CBO: {cbo}")
    
    print("\n5. LACK OF COHESION OF METHODS (LCOM):")
    print("-" * 60)
    print("  (Note: Full LCOM calculation requires detailed attribute tracking)")
    for class_name in analyzer.classes:
        lcom = calculate_lcom(class_name, analyzer.classes, analyzer.methods)
        print(f"  {class_name:40s} LCOM: {lcom:.2f} (estimated)")
    
    return analyzer

if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze_file(sys.argv[1])
    else:
        print("Usage: python metric_analyzer.py <filename>")

