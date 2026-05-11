
import re
import math
from collections import Counter

# Define the SKILL_ALIASES dictionary
SKILL_ALIASES = {
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
    "sql": "sql",
    "mysql": "mysql",
    "mysq": "mysql",
    "postgresql": "postgresql",
    "postgres": "postgresql",
    "mongodb": "mongodb",
    "redis": "redis",
    "docker": "docker",
    "kubernetes": "kubernetes",
    "kubernates": "kubernetes",
    "k8s": "kubernetes",
    "ci/cd": "ci_cd",
    "cicd": "ci_cd",
    "ci cd": "ci_cd",
    "aws": "aws",
}

def normalize_skills(raw_skills):
    """
    Normalize the raw skills string by splitting on commas, lowercasing tokens,
    applying alias mapping, and discarding unknown tokens.
    """
    skills = []
    for token in raw_skills.split(','):
        token = token.strip().lower()
        if token in SKILL_ALIASES:
            skills.append(SKILL_ALIASES[token])
    return skills

def deduplicate_skills(skills):
    """
    Remove duplicate canonical skills from the list.
    """
    return list(set(skills))

def build_vocabulary(resumes):
    """
    Create a shared vocabulary from all normalized + deduplicated resume skills.
    """
    vocabulary = set()
    for resume in resumes:
        skills = normalize_skills(resume['raw_skills'])
        skills = deduplicate_skills(skills)
        vocabulary.update(skills)
    return sorted(list(vocabulary))

def compute_tf_idf(resumes, vocabulary):
    """
    Compute TF-IDF vectors for resumes using the exact formulas.
    """
    tf_idf_vectors = []
    for resume in resumes:
        skills = normalize_skills(resume['raw_skills'])
        skills = deduplicate_skills(skills)
        tf = Counter(skills)
        idf = {}
        for skill in vocabulary:
            idf[skill] = math.log(10 / sum(1 for r in resumes if skill in normalize_skills(r['raw_skills'])))
        tf_idf = {skill: tf[skill] * idf[skill] for skill in vocabulary}
        tf_idf_vectors.append(tf_idf)
    return tf_idf_vectors

def build_jd_vectors(job_descriptions, vocabulary):
    """
    Create binary vectors for job descriptions over the same vocabulary.
    """
    jd_vectors = []
    for jd in job_descriptions:
        skills = jd['required_skills'] + jd['preferred_skills']
        skills = [skill.lower() for skill in skills]
        jd_vector = {skill: 1 if skill in skills else 0 for skill in vocabulary}
        jd_vectors.append(jd_vector)
    return jd_vectors

def compute_cosine_similarity(tf_idf_vectors, jd_vectors):
    """
    Compute cosine similarity between resumes and JDs.
    """
    similarities = []
    for tf_idf_vector in tf_idf_vectors:
        for jd_vector in jd_vectors:
            dot_product = sum(tf_idf_vector[skill] * jd_vector[skill] for skill in tf_idf_vector)
            magnitude_tf_idf = math.sqrt(sum(tf_idf_vector[skill] ** 2 for skill in tf_idf_vector))
            magnitude_jd = math.sqrt(sum(jd_vector[skill] ** 2 for skill in jd_vector))
            similarity = dot_product / (magnitude_tf_idf * magnitude_jd)
            similarities.append(similarity)
    return similarities

def rank_candidates(similarities, resumes, job_descriptions):
    """
    Rank the Top 3 candidates per JD based on cosine similarity.
    """
    ranked_candidates = []
    for i, jd in enumerate(job_descriptions):
        jd_similarities = similarities[i::len(job_descriptions)]
        top_3_indices = sorted(range(len(jd_similarities)), key=lambda i: jd_similarities[i], reverse=True)[:3]
        top_3_candidates = [resumes[j] for j in top_3_indices]
        ranked_candidates.append(top_3_candidates)
    return ranked_candidates

# Load the resume and job description data
resumes = [
    {"name": "Arjun Sharma", "raw_skills": "Pyhton, MachineLearning, SQL, pandas, numpy, Deep-learning"},
    {"name": "Priya Nair", "raw_skills": "JavaScrpit, Reacts, Node.JS, MongoDb, REST api, HTML/CSS"},
    {"name": "Rahul Gupta", "raw_skills": "Java, Spring Boot, MySql, Microservices, Docker, kubernates"},
    {"name": "Sneha Patel", "raw_skills": "Python, TensorFlow, Keras, NLP, BERT, data-viz, matplotlib"},
    {"name": "Vikram Singh", "raw_skills": "C++, Algoritms, Data Structure, competitive programming, python"},
    {"name": "Ananya Krishnan", "raw_skills": "javascript, vue.js, python, flask, PostgreSQL, AWS, CI/CD"},
    {"name": "Karan Mehta", "raw_skills": "Python, Sklearn, XGboost, feature engineering, SQL, tableau"},
    {"name": "Deepika Rao", "raw_skills": "Java, Android, Kotlin, Firebase, REST, UI/UX, figma"},
    {"name": "Aditya Kumar", "raw_skills": "Reactjs, TypeScrpit, GraphQL, redux, tailwind, nodejs, jest"},
    {"name": "Meera Iyer", "raw_skills": "python, R, statistics, ML, regression, clustering, Power-BI"},
]

job_descriptions = [
    {"company": "Kakao", "role": "ML Engineer", "required_skills": ["Python", "Machine Learning", "Deep Learning"], "preferred_skills": ["NLP", "BERT"]},
    {"company": "Naver", "role": "Backend Engineer", "required_skills": ["Java", "Spring Boot"], "preferred_skills": ["REST API", "CI/CD"]},
    {"company": "Line", "role": "Frontend Engineer", "required_skills": ["JavaScript", "React"], "preferred_skills": ["Node.js", "GraphQL"]},
]

# Compute the TF-IDF vectors for resumes
vocabulary = build_vocabulary(resumes)
tf_idf_vectors = compute_tf_idf(resumes, vocabulary)

# Compute the binary vectors for job descriptions
jd_vectors = build_jd_vectors(job_descriptions, vocabulary)

# Compute the cosine similarity between resumes and JDs
similarities = compute_cosine_similarity(tf_idf_vectors, jd_vectors)

# Rank the Top 3 candidates per JD
ranked_candidates = rank_candidates(similarities, resumes, job_descriptions)