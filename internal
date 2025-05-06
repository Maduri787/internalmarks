
import pandas as pd

# Load the uploaded Excel file
input_path = "/content/sample.xlsx"
df = pd.read_excel(input_path)

# Show the first few rows to understand the structure
df.head()


import random

def distribute_marks(total_marks):
    if not (0 <= total_marks <= 20):
        return None  # Skip invalid total marks

    for _ in range(1000):
        max_short = min(5, total_marks)
        num_short_ones = random.randint(0, max_short)
        short_questions = {f's{i+1}': 0 for i in range(5)}
        for key in random.sample(list(short_questions.keys()), num_short_ones):
            short_questions[key] = 1
        short_total = sum(short_questions.values())
        remaining = total_marks - short_total
        if remaining < 0:
            continue

        possible_keys = [f'l{i+1}' for i in range(5)]
        for _ in range(1000):
            selected_keys = random.sample(possible_keys, 3)
            values = [random.randint(0, 5) for _ in range(3)]
            if sum(values) <= min(15, remaining):
                long_questions = {k: 0 for k in possible_keys}
                for i, key in enumerate(selected_keys):
                    long_questions[key] = values[i]
                if short_total + sum(values) == total_marks:
                    result = {
                        'Total': total_marks,
                        **{k: (v if v > 0 else '') for k, v in short_questions.items()},
                        'Total_partA': short_total,
                        **{k: (v if v > 0 else '') for k, v in long_questions.items()},
                        'Total_partB': sum(values)
                    }
                    return result
    return None

# Distribute marks for each student
output_rows = []
for _, row in df.iterrows():
    total = row.get('Total', 0)
    try:
        total = int(total)
    except ValueError:
        total = 0
    result = distribute_marks(total)
    if result:
        output_rows.append(result)
    else:
        output_rows.append({
            'Total': total,
            **{f's{i+1}': '' for i in range(5)},
            'Total_partA': '',
            **{f'l{i+1}': '' for i in range(5)},
            'Total_partB': ''
        })

# Create output DataFrame
output_df = pd.DataFrame(output_rows, columns=[
    'Total', 's1', 's2', 's3', 's4', 's5', 'Total_partA',
    'l1', 'l2', 'l3', 'l4', 'l5', 'Total_partB'
])

# Save to new Excel file
output_path = "/content/distributed_marks.xlsx"
output_df.to_excel(output_path, index=False)

 
