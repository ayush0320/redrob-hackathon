import math
from collections import defaultdict

# ============================================================================
# SKILL_ALIASES - Exact mapping from problem statement
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
# RESUME DATA
# ============================================================================
RESUMES = [
    {"id": "01", "name": "Arjun Sharma", "skills": "Pyhton, MachineLearning, SQL, pandas, numpy, Deep-learning"},
    {"id": "02", "name": "Priya Nair", "skills": "JavaScrpit, Reacts, Node.JS, MongoDb, REST api, HTML/CSS"},
    {"id": "03", "name": "Rahul Gupta", "skills": "Java, Spring Boot, MySql, Microservices, Docker, kubernates"},
    {"id": "04", "name": "Sneha Patel", "skills": "Python, TensorFlow, Keras, NLP, BERT, data-viz, matplotlib"},
    {"id": "05", "name": "Vikram Singh", "skills": "C++, Algoritms, Data Structure, competitive programming, python"},
    {"id": "06", "name": "Ananya Krishnan", "skills": "javascript, vue.js, python, flask, PostgreSQL, AWS, CI/CD"},
    {"id": "07", "name": "Karan Mehta", "skills": "Python, Sklearn, XGboost, feature engineering, SQL, tableau"},
    {"id": "08", "name": "Deepika Rao", "skills": "Java, Android, Kotlin, Firebase, REST, UI/UX, figma"},
    {"id": "09", "name": "Aditya Kumar", "skills": "Reactjs, TypeScrpit, GraphQL, redux, tailwind, nodejs, jest"},
    {"id": "10", "name": "Meera Iyer", "skills": "python, R, statistics, ML, regression, clustering, Power-BI"},
]

JOB_DESCRIPTIONS = [
    {
        "id": "JD-1",
        "company": "Kakao (Seoul)",
        "role": "ML Engineer",
        "skills": "Python, Machine Learning, Deep Learning, TensorFlow, PyTorch, SQL, Data Visualization, NLP, BERT, Feature Engineering, Statistics"
    },
    {
        "id": "JD-2",
        "company": "Naver (Seongnam)",
        "role": "Backend Engineer",
        "skills": "Java, Spring Boot, MySQL, PostgreSQL, Microservices, Docker, Kubernetes, REST API, CI/CD, Redis"
    },
    {
        "id": "JD-3",
        "company": "Line (Seoul)",
        "role": "Frontend Engineer",
        "skills": "JavaScript, React, Vue, TypeScript, REST API, HTML/CSS, Node.js, GraphQL, Redux, Jest, AWS"
    },
]

# ============================================================================
# STEP 1: NORMALIZE SKILLS
# ============================================================================
def normalize_skills(raw_skills_str):
    """
    Normalize a comma-separated skill string:
    1. Split by comma
    2. Lowercase each token
    3. Match multi-word phrases first, then single tokens
    4. Apply alias mapping
    5. Discard unknown tokens
    """
    raw_tokens = [token.strip() for token in raw_skills_str.split(",")]
    normalized = []
    
    for token in raw_tokens:
        token_lower = token.lower()
        
        # Try exact match in SKILL_ALIASES
        if token_lower in SKILL_ALIASES:
            normalized.append(SKILL_ALIASES[token_lower])
        # Try matching as part of a multi-word phrase
        else:
            matched = False
            # Check if this token is part of any multi-word alias key
            for alias_key in SKILL_ALIASES:
                if " " in alias_key and token_lower == alias_key.lower():
                    normalized.append(SKILL_ALIASES[alias_key])
                    matched = True
                    break
            
            # If no match, discard (unknown token)
            if not matched:
                pass  # Discard unknown tokens
    
    return normalized

# ============================================================================
# STEP 2: DEDUPLICATE SKILLS
# ============================================================================
def deduplicate_skills(normalized_skills):
    """Remove duplicate canonical skills from list"""
    return list(dict.fromkeys(normalized_skills))  # Preserves order, removes duplicates

# ============================================================================
# STEP 3: BUILD VOCABULARY
# ============================================================================
def build_vocabulary(all_resumes):
    """Create sorted vocabulary from all normalized & deduplicated resume skills"""
    vocab_set = set()
    
    for resume in all_resumes:
        normalized = normalize_skills(resume["skills"])
        deduplicated = deduplicate_skills(normalized)
        vocab_set.update(deduplicated)
    
    # Sort alphabetically
    vocabulary = sorted(list(vocab_set))
    return vocabulary

# ============================================================================
# STEP 4: COMPUTE TF-IDF VECTORS
# ============================================================================
def compute_tfidf_vectors(all_resumes, vocabulary):
    """
    Compute TF-IDF vectors for all resumes.
    TF = 1/N (where N = unique skills in resume)
    IDF = ln(10 / df) where df = number of resumes containing skill
    """
    # First, get normalized & deduplicated skills for each resume
    normalized_resumes = []
    for resume in all_resumes:
        normalized = normalize_skills(resume["skills"])
        deduplicated = deduplicate_skills(normalized)
        normalized_resumes.append(deduplicated)
    
    # Compute document frequency for each skill
    df = defaultdict(int)
    for skills in normalized_resumes:
        for skill in set(skills):  # Use set to count unique skills per resume
            df[skill] += 1
    
    # Compute IDF for each skill
    idf = {}
    for skill in vocabulary:
        if df[skill] > 0:
            idf[skill] = math.log(10 / df[skill])
        else:
            idf[skill] = 0
    
    # Compute TF-IDF vectors
    tfidf_vectors = []
    for i, skills in enumerate(normalized_resumes):
        N = len(skills)
        vector = []
        
        for skill in vocabulary:
            if N > 0 and skill in skills:
                tf = 1 / N
                tfidf = tf * idf[skill]
            else:
                tfidf = 0
            vector.append(tfidf)
        
        tfidf_vectors.append(vector)
    
    return tfidf_vectors, idf, normalized_resumes

# ============================================================================
# STEP 5: BUILD JD BINARY VECTORS
# ============================================================================
def build_jd_vectors(job_descriptions, vocabulary):
    """
    Build binary vectors for JDs.
    For each skill in vocabulary, put 1 if present in JD, 0 otherwise.
    """
    jd_vectors = []
    
    for jd in job_descriptions:
        # Combine required and preferred skills
        all_jd_skills = jd["skills"]
        
        # Parse skills from JD (they're comma-separated or space-separated in the description)
        # We need to normalize them the same way as resume skills
        jd_skill_tokens = [s.strip().lower() for s in all_jd_skills.replace(",", " ").split()]
        
        # Normalize JD skills
        jd_normalized = []
        for token in jd_skill_tokens:
            if token in SKILL_ALIASES:
                jd_normalized.append(SKILL_ALIASES[token])
            else:
                # Try to match multi-word phrases
                matched = False
                for alias_key in SKILL_ALIASES:
                    if " " in alias_key and token in alias_key.lower().split():
                        # This is a partial match; we need full phrase matching
                        pass
                if not matched:
                    pass  # Discard unknown
        
        # Better approach: parse JD skills more carefully
        # Split by comma first to get individual skills
        jd_skills_raw = [s.strip() for s in all_jd_skills.split(",")]
        jd_normalized = []
        
        for skill_raw in jd_skills_raw:
            skill_lower = skill_raw.lower()
            if skill_lower in SKILL_ALIASES:
                jd_normalized.append(SKILL_ALIASES[skill_lower])
            else:
                # Check multi-word matches
                matched = False
                for alias_key in SKILL_ALIASES:
                    if " " in alias_key and skill_lower == alias_key.lower():
                        jd_normalized.append(SKILL_ALIASES[alias_key])
                        matched = True
                        break
        
        # Deduplicate
        jd_dedup = deduplicate_skills(jd_normalized)
        
        # Build binary vector
        vector = [1 if skill in jd_dedup else 0 for skill in vocabulary]
        jd_vectors.append(vector)
    
    return jd_vectors

# ============================================================================
# STEP 6: COSINE SIMILARITY & RANKING
# ============================================================================
def cosine_similarity(vec_a, vec_b):
    """
    Cosine(A, B) = (A · B) / (|A| × |B|)
    """
    # Dot product
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    
    # Magnitude of A
    magnitude_a = math.sqrt(sum(a * a for a in vec_a))
    
    # Magnitude of B
    magnitude_b = math.sqrt(sum(b * b for b in vec_b))
    
    if magnitude_a == 0 or magnitude_b == 0:
        return 0
    
    return dot_product / (magnitude_a * magnitude_b)

def rank_candidates(tfidf_vectors, jd_vector, candidate_names):
    """
    Rank candidates by cosine similarity to JD.
    Returns top 3 with scores rounded to 2 decimal places.
    Ties broken alphabetically by candidate name.
    """
    scores = []
    for i, resume_vec in enumerate(tfidf_vectors):
        score = cosine_similarity(resume_vec, jd_vector)
        scores.append((candidate_names[i], score))
    
    # Sort by score (descending), then by name (ascending) for tiebreaking
    scores.sort(key=lambda x: (-x[1], x[0]))
    
    # Return top 3 with scores rounded to 2 decimal places
    top_3 = [(name, round(score, 2)) for name, score in scores[:3]]
    return top_3

# ============================================================================
# MAIN EXECUTION
# ============================================================================
def main():
    print("=" * 80)
    print("RESUME MATCHING ENGINE - REDROB HACKATHON")
    print("=" * 80)
    
    # Get candidate names
    candidate_names = [resume["name"] for resume in RESUMES]
    
    # Step 1-2: Normalize and deduplicate
    print("\n[STEP 1-2] Normalizing and deduplicating skills...")
    normalized_all = []
    for resume in RESUMES:
        normalized = normalize_skills(resume["skills"])
        deduplicated = deduplicate_skills(normalized)
        normalized_all.append(deduplicated)
        print(f"  {resume['name']}: {deduplicated}")
    
    # Step 3: Build vocabulary
    print("\n[STEP 3] Building vocabulary...")
    vocabulary = build_vocabulary(RESUMES)
    print(f"  Vocabulary size: {len(vocabulary)}")
    print(f"  Vocabulary: {vocabulary}")
    
    # Step 4: Compute TF-IDF vectors
    print("\n[STEP 4] Computing TF-IDF vectors...")
    tfidf_vectors, idf, normalized_resumes = compute_tfidf_vectors(RESUMES, vocabulary)
    
    # Step 5: Build JD vectors
    print("\n[STEP 5] Building JD binary vectors...")
    jd_vectors = build_jd_vectors(JOB_DESCRIPTIONS, vocabulary)
    
    # Step 6: Compute similarity and rank
    print("\n[STEP 6] Computing cosine similarity and ranking...")
    
    results = {}
    for jd_idx, (jd, jd_vector) in enumerate(zip(JOB_DESCRIPTIONS, jd_vectors)):
        jd_id = jd["id"]
        company = jd["company"]
        role = jd["role"]
        
        top_3 = rank_candidates(tfidf_vectors, jd_vector, candidate_names)
        results[jd_id] = top_3
        
        print(f"\n{jd_id} — {company} ({role})")
        for rank, (name, score) in enumerate(top_3, 1):
            print(f"  {rank}. {name}({score})")
    
    # ========================================================================
    # FINAL OUTPUT
    # ========================================================================
    print("\n" + "=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)
    
    for jd_idx, jd in enumerate(JOB_DESCRIPTIONS):
        jd_id = jd["id"]
        company = jd["company"]
        role = jd["role"]
        top_3 = results[jd_id]
        
        # Format: Name(score), Name(score), Name(score)
        output = ", ".join([f"{name}({score})" for name, score in top_3])
        print(f"\n{jd_id} — {company} ({role})")
        print(output)
    
    return results

if __name__ == "__main__":
    main()
