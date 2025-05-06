
import streamlit as st
import pandas as pd
import random
from io import BytesIO

st.title("📊 Student Marks Distributor")

# File Upload
uploaded_file = st.file_uploader("📁 Upload Excel File (with 'Total' column)", type=["xlsx"])
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully!")
        st.write("Preview of uploaded file:")
        st.dataframe(df.head())

        def distribute_marks(total_marks):
            if not (0 <= total_marks <= 20):
                return None

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

        # Apply Distribution
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

        output_df = pd.DataFrame(output_rows, columns=[
            'Total', 's1', 's2', 's3', 's4', 's5', 'Total_partA',
            'l1', 'l2', 'l3', 'l4', 'l5', 'Total_partB'
        ])

        st.subheader("✅ Processed Data")
        st.dataframe(output_df)

        # Create downloadable Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            output_df.to_excel(writer, index=False, sheet_name='Distributed Marks')
        st.download_button(
            label="📥 Download Excel File",
            data=output.getvalue(),
            file_name="distributed_marks.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")
else:
    st.info("Upload an Excel file to begin. The file should contain a column named 'Total'.")

