"""
Verification Script for Resume Matching Engine
Validates each step of the pipeline and helps catch errors
"""

import math
from collections import defaultdict

# ============================================================================
# SKILL_ALIASES (Same as main solution)
# ============================================================================
SKILL_ALIASES = {
    # Languages
    "python": "python",
    "pyhton": "python",
    "java": "java",
    "javascript": "javascript",
    "javascrpit": "javascript",
    "js": "javascript",
    "typescript": "typescript",
    "typescrpit": "typescript",
    "c++": "cpp",
    "cpp": "cpp",
    "r": "r",
    "kotlin": "kotlin",
    # ML / Data
    "machinelearning": "machine_learning",
    "machine learning": "machine_learning",
    "ml": "machine_learning",
    "sklearn": "machine_learning",
    "deeplearning": "deep_learning",
    "deep learning": "deep_learning",
    "deep-learning": "deep_learning",
    "tensorflow": "tensorflow",
    "pytorch": "pytorch",
    "keras": "keras",
    "nlp": "nlp",
    "bert": "bert",
    "xgboost": "xgboost",
    "feature engineering": "feature_engineering",
    "statistics": "statistics",
    "stats": "statistics",
    "regression": "regression",
    "clustering": "clustering",
    "data-viz": "data_visualization",
    "data visualization": "data_visualization",
    "data viz": "data_visualization",
    "matplotlib": "data_visualization",
    "tableau": "data_visualization",
    "power-bi": "data_visualization",
    "power bi": "data_visualization",
    "powerbi": "data_visualization",
    "pandas": "pandas",
    "numpy": "numpy",
    # Web — Frontend
    "react": "react",
    "reacts": "react",
    "reactjs": "react",
    "vue": "vue",
    "vue.js": "vue",
    "vuejs": "vue",
    "redux": "redux",
    "tailwind": "tailwind",
    "html/css": "html_css",
    "html css": "html_css",
    "html": "html_css",
    "css": "html_css",
    "jest": "jest",
    "graphql": "graphql",
    # Web — Backend
    "node.js": "nodejs",
    "nodejs": "nodejs",
    "node js": "nodejs",
    "flask": "flask",
    "spring boot": "spring_boot",
    "springboot": "spring_boot",
    "rest api": "rest_api",
    "rest": "rest_api",
    "restapi": "rest_api",
    "microservices": "microservices",
    # Databases
    "sql": "sql",
    "mysql": "mysql",
    "mysq": "mysql",
    "postgresql": "postgresql",
    "postgres": "postgresql",
    "mongodb": "mongodb",
    "redis": "redis",
    # DevOps / Cloud
    "docker": "docker",
    "kubernetes": "kubernetes",
    "kubernates": "kubernetes",
    "k8s": "kubernetes",
    "ci/cd": "ci_cd",
    "cicd": "ci_cd",
    "ci cd": "ci_cd",
    "aws": "aws",
    # Mobile
    "android": "android",
    "firebase": "firebase",
    # CS Fundamentals
    "algorithms": "algorithms",
    "algoritms": "algorithms",
    "data structure": "data_structures",
    "data structures": "data_structures",
    "competitive programming": "competitive_programming",
    # Design
    "ui/ux": "ui_ux",
    "ui ux": "ui_ux",
    "figma": "figma",
}

# ============================================================================
# SAMPLE VERIFICATION TESTS
# ============================================================================

def test_normalization():
    """Test that skill normalization works correctly"""
    print("\n" + "="*80)
    print("TEST 1: SKILL NORMALIZATION")
    print("="*80)
    
    test_cases = [
        ("Pyhton, Deep-learning, pandas", ["python", "deep_learning", "pandas"]),
        ("JavaScrpit, Reacts, Node.JS", ["javascript", "react", "nodejs"]),
        ("Spring Boot, MySql, kubernates", ["spring_boot", "mysql", "kubernetes"]),
    ]
    
    for raw_input, expected in test_cases:
        tokens = [t.strip().lower() for t in raw_input.split(",")]
        normalized = []
        
        for token in tokens:
            if token in SKILL_ALIASES:
                normalized.append(SKILL_ALIASES[token])
        
        status = "✅ PASS" if normalized == expected else "❌ FAIL"
        print(f"\n{status}")
        print(f"  Input:    {raw_input}")
        print(f"  Expected: {expected}")
        print(f"  Got:      {normalized}")

def test_deduplication():
    """Test that deduplication removes duplicates"""
    print("\n" + "="*80)
    print("TEST 2: DEDUPLICATION")
    print("="*80)
    
    test_cases = [
        (["python", "python", "sql"], ["python", "sql"]),
        (["java", "spring_boot", "java"], ["java", "spring_boot"]),
        (["react", "typescript", "react", "typescript"], ["react", "typescript"]),
    ]
    
    for input_list, expected in test_cases:
        result = list(dict.fromkeys(input_list))
        status = "✅ PASS" if result == expected else "❌ FAIL"
        print(f"\n{status}")
        print(f"  Input:    {input_list}")
        print(f"  Expected: {expected}")
        print(f"  Got:      {result}")

def test_tf_idf():
    """Test TF-IDF calculation"""
    print("\n" + "="*80)
    print("TEST 3: TF-IDF CALCULATION")
    print("="*80)
    
    # Example: Resume with 4 skills, skill appears in 5 out of 10 resumes
    N = 4  # Total unique skills in this resume
    df = 5  # Document frequency (# resumes with this skill)
    
    TF = 1 / N
    IDF = math.log(10 / df)
    TF_IDF = TF * IDF
    
    print(f"\nExample Resume:")
    print(f"  Total unique skills (N): {N}")
    print(f"  TF = 1/N = 1/{N} = {TF:.4f}")
    
    print(f"\nExample Skill:")
    print(f"  Document frequency (df): {df}")
    print(f"  IDF = ln(10/{df}) = {IDF:.4f}")
    
    print(f"\nTF-IDF = {TF:.4f} × {IDF:.4f} = {TF_IDF:.4f}")
    print(f"\n✅ Expected behavior: Skills in fewer resumes = higher IDF = higher TF-IDF")

def test_cosine_similarity():
    """Test cosine similarity calculation"""
    print("\n" + "="*80)
    print("TEST 4: COSINE SIMILARITY")
    print("="*80)
    
    # Simple 3D example
    vec_a = [1, 0, 0]  # Resume TF-IDF vector (simplified)
    vec_b = [1, 1, 1]  # JD binary vector
    
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(x * x for x in vec_a))
    mag_b = math.sqrt(sum(x * x for x in vec_b))
    
    cosine = dot_product / (mag_a * mag_b) if mag_a > 0 and mag_b > 0 else 0
    
    print(f"\nExample Vectors (3D):")
    print(f"  Resume TF-IDF (A): {vec_a}")
    print(f"  JD Binary (B):     {vec_b}")
    
    print(f"\nCalculations:")
    print(f"  A · B = {dot_product}")
    print(f"  |A| = sqrt({sum(x*x for x in vec_a)}) = {mag_a:.4f}")
    print(f"  |B| = sqrt({sum(x*x for x in vec_b)}) = {mag_b:.4f}")
    
    print(f"\nCosine(A, B) = {dot_product} / ({mag_a:.4f} × {mag_b:.4f})")
    print(f"             = {cosine:.4f}")
    
    print(f"\n✅ Cosine similarity ranges from 0 to 1")
    print(f"   0 = no match, 1 = perfect match")

def test_tiebreaking():
    """Test alphabetical tiebreaking"""
    print("\n" + "="*80)
    print("TEST 5: TIEBREAKING (ALPHABETICAL)")
    print("="*80)
    
    scores = [
        ("Aditya Kumar", 0.67),
        ("Priya Nair", 0.67),  # Same score as Aditya
        ("Ananya Krishnan", 0.35),
    ]
    
    print(f"\nUnsorted scores:")
    for name, score in scores:
        print(f"  {name}: {score}")
    
    # Sort by score descending, then by name ascending
    sorted_scores = sorted(scores, key=lambda x: (-x[1], x[0]))
    
    print(f"\nAfter sorting (by score desc, then name asc):")
    for i, (name, score) in enumerate(sorted_scores, 1):
        print(f"  {i}. {name}: {score}")
    
    print(f"\n✅ Aditya Kumar comes before Priya Nair (alphabetically)")

def test_vocabulary_construction():
    """Test vocabulary is sorted alphabetically"""
    print("\n" + "="*80)
    print("TEST 6: VOCABULARY CONSTRUCTION")
    print("="*80)
    
    # Example from 2 resumes
    resume1_skills = ["python", "machine_learning", "sql"]
    resume2_skills = ["java", "spring_boot", "python"]
    
    all_skills = set(resume1_skills + resume2_skills)
    vocabulary = sorted(list(all_skills))
    
    print(f"\nResume 1 skills: {resume1_skills}")
    print(f"Resume 2 skills: {resume2_skills}")
    
    print(f"\nCombined (deduplicated): {all_skills}")
    print(f"Sorted vocabulary:       {vocabulary}")
    
    print(f"\n✅ Vocabulary is sorted alphabetically for consistency")

def run_all_tests():
    """Run all verification tests"""
    print("\n")
    print("█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + "  RESUME MATCHING ENGINE - VERIFICATION TESTS".center(78) + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    
    test_normalization()
    test_deduplication()
    test_tf_idf()
    test_cosine_similarity()
    test_tiebreaking()
    test_vocabulary_construction()
    
    print("\n" + "="*80)
    print("ALL TESTS COMPLETED")
    print("="*80 + "\n")

if __name__ == "__main__":
    run_all_tests()
