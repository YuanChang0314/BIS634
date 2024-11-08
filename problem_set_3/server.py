from flask import Flask, render_template, request
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

data = pd.read_csv(r"C:\Users\jackchang\Desktop\regular_python_work\Yale\BIS634\problem_set_3\ddi_training.csv")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    interaction_type = request.form["interaction_type"]
    analysis_type = request.form["analysis_type"]
    #  error handling
    if analysis_type == "count":
        try:
            count = data['type'].value_counts().get(int(interaction_type), 0)
        except:
            result = 'invalid number'
            return render_template("analyze.html", analysis=result, interaction_type=interaction_type)

        if count == 0:
            result = f"The interaction type '{interaction_type}' was not found in the dataset."
        else:
            result = f"The interaction type '{interaction_type}' appears {count} times."

    elif analysis_type == "list_top":
        top_interactions = data['type'].value_counts().head(5)
        result = "Top 5 interaction types:\n" + "\n".join([f"{item}: {count}" for item, count in top_interactions.items()])

    counts = data['type'].value_counts()
    colors = ['blue' if item != int(interaction_type) else 'red' for item in counts.index]
    print(colors)
    plt.figure(figsize=(10, 6))
    counts.plot(kind='bar', color=colors)
    plt.title('Interaction Type Counts')
    plt.xlabel('Interaction Type')
    plt.ylabel('Count')
    plt.savefig(r'C:\Users\jackchang\Desktop\regular_python_work\Yale\BIS634\problem_set_3\static\interaction_plot.png')
    plt.close()
    return render_template("analyze.html", analysis=result, interaction_type=interaction_type)


if __name__ == "__main__":
    app.run(debug=True)
