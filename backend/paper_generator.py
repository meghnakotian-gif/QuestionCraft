import random

easy_questions = ["Q1", "Q2", "Q3"]
medium_questions = ["Q4", "Q5", "Q6"]
hard_questions = ["Q7", "Q8"]

paper = []

paper.extend(random.sample(easy_questions, 2))
paper.extend(random.sample(medium_questions, 2))
paper.extend(random.sample(hard_questions, 1))

print("Generated Question Paper:")
for q in paper:
    print(q)
    