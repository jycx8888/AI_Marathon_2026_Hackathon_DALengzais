

import pandas as pd

people     = pd.read_csv("hf://datasets/Suriyaganesh/54k-resume/01_people.csv")
abilities  = pd.read_csv("hf://datasets/Suriyaganesh/54k-resume/02_abilities.csv")
education  = pd.read_csv("hf://datasets/Suriyaganesh/54k-resume/03_education.csv")
experience = pd.read_csv("hf://datasets/Suriyaganesh/54k-resume/04_experience.csv")
person_skills = pd.read_csv("hf://datasets/Suriyaganesh/54k-resume/05_person_skills.csv")
skills     = pd.read_csv("hf://datasets/Suriyaganesh/54k-resume/06_skills.csv")

print("=== 01_people.csv ===")
print(people.columns.tolist())
print(people.head(3))

print("\n=== 02_abilities.csv ===")
print(abilities.columns.tolist())
print(abilities.head(3))

print("\n=== 03_education.csv ===")
print(education.columns.tolist())
print(education.head(3))

print("\n=== 04_experience.csv ===")
print(experience.columns.tolist())
print(experience.head(3))

print("\n=== 05_person_skills.csv ===")
print(person_skills.columns.tolist())
print(person_skills.head(3))

print("\n=== 06_skills.csv ===")
print(skills.columns.tolist())
print(skills.head(3))