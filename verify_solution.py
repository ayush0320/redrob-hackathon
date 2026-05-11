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
    "android": "android",
    "firebase": "firebase",
    "algorithms": "algorithms",
    "algoritms": "algorithms",
    "data structure": "data_structures",
    "data structures": "data_structures",
    "competitive programming": "competitive_programming",
    "ui/ux": "ui_ux",
    "ui ux": "ui_ux",
    "figma": "figma",
}

# Define the resume dataset
RESUME_DATASET = [
    {"id": "01", "candidate": "Arjun Sharma", "raw_skills": "Pyhton, MachineLearning, SQL, pandas, numpy, Deep-learning"},
    {"id": "02", "candidate": "Priya Nair", "raw_skills": "JavaScrpit, Reacts, Node.JS, MongoDb, REST api, HTML/CSS"},
    {"id": "03", "candidate": "Rahul Gupta", "raw_skills": "Java, Spring Boot, MySql, Microservices, Docker, kubernates"},
    {"id": "04", "candidate": "Sneha Patel", "raw_skills": "Python, TensorFlow, Keras, NLP, BERT, data-viz, matplotlib"},
    {"id": "05", "candidate": "Vikram Singh", "raw_skills": "C++, Algoritms, Data Structure, competitive programming, python"},
    {"id": "06", "candidate": "Ananya Krishnan", "raw_skills": "javascript, vue.js, python, flask, PostgreSQL, AWS, CI/CD"},
    {"id": "07", "candidate": "Karan Mehta", "raw_skills": "Python, Sklearn, XGboost, feature engineering, SQL, tableau"},
    {"id": "08", "candidate": "Deepika Rao", "raw_skills": "Java, Android, Kotlin, Firebase, REST, UI/UX, figma"},
    {"id": "09", "candidate": "Aditya Kumar", "raw_skills": "Reactjs, TypeScrpit, GraphQL, redux, tailwind, nodejs, jest"},
    {"id": "10", "candidate": "Meera Iyer", "raw_skills": "python, R, statistics, ML, regression, clustering, Power-BI"},
]

# Define the job description dataset
JOB_DESCRIPTION_DATASET = [
    {"id": "JD-1", "company": "Kakao", "role": "ML Engineer", "required_skills": "Python, Machine Learning, Deep Learning, TensorFlow, PyTorch, SQL, Data Visualization", "preferred_skills": "NLP, BERT, Feature Engineering, Statistics"},
    {"id": "JD-2", "company": "Naver", "role": "Backend Engineer", "required_skills": "Java, Spring Boot, MySQL, PostgreSQL, Microservices, Docker, Kubernetes", "preferred_skills": "REST API, CI/CD, Redis"},
    {"id": "JD-3", "company": "Line", "role": "Frontend Engineer", "required_skills": "JavaScript, React, Vue, TypeScript, REST API, HTML/CSS", "preferred_skills": "Node.js, GraphQL, Redux, Jest, AWS"},
]

def normalize_skills(raw_skills):
    skills = raw_skills.split(", ")
    normalized_skills = []
    for skill in skills:
        skill = skill.lower()
        if skill in SKILL_ALIASES:
            normalized_skills.append(SKILL_ALIASES[skill])
        elif " " in skill:
            for alias, value in SKILL_ALIASES.items():
                if alias in skill:
                    normalized_skills.append(value)
                    break
    return list(set(normalized_skills))

def compute_tf_idf(resume_skills):
    tf_idf = {}
    for skill in resume_skills:
        tf = 1 / len(resume_skills)
        df = sum(1 for resume in RESUME_DATASET if skill in normalize_skills(resume["raw_skills"]))
        idf = math.log(10 / df)
        tf_idf[skill] = tf * idf
    return tf_idf

def compute_cosine_similarity(resume_skills, job_description_skills):
    resume_vector = compute_tf_idf(resume_skills)
    job_description_vector = {skill: 1 for skill in job_description_skills}
    dot_product = sum(resume_vector.get(skill, 0) * job_description_vector.get(skill, 0) for skill in set(resume_vector) | set(job_description_vector))
    resume_magnitude = math.sqrt(sum(value ** 2 for value in resume_vector.values()))
    job_description_magnitude = math.sqrt(sum(value ** 2 for value in job_description_vector.values()))
    return dot_product / (resume_magnitude * job_description_magnitude)

def rank_candidates(job_description):
    required_skills = normalize_skills(job_description["required_skills"])
    preferred_skills = normalize_skills(job_description["preferred_skills"])
    job_description_skills = required_skills + preferred_skills
    candidate_scores = {}
    for resume in RESUME_DATASET:
        resume_skills = normalize_skills(resume["raw_skills"])
        score = compute_cosine_similarity(resume_skills, job_description_skills)
        candidate_scores[resume["candidate"]] = score
    return sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)

def main():
    for job_description in JOB_DESCRIPTION_DATASET:
        print(f"{job_description['id']} — {job_description['company']} ({job_description['role']})")
        ranked_candidates = rank_candidates(job_description)
        for candidate, score in ranked_candidates[:3]:
            print(f"{candidate}({score:.2f})")

if __name__ == "__main__":
    main()