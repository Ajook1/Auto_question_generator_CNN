import streamlit as st
import random
import re

# Define the concepts and question templates
concepts = {
    "CNN": [
        "Convolution", "Pooling", "Backpropagation", "Activation Functions", "Stride", "Padding",
        "Filters", "Feature Maps", "ReLU", "Batch Normalization", "Dropout", "Fully Connected Layers",
        "Max Pooling", "Average Pooling", "Flattening", "Receptive Field", "Weight Sharing",
        "Translation Invariance", "Zero Padding", "Valid Padding", "Same Padding", "Stride Variants",
        "Parameter Efficiency", "Filter Size Selection", "Depthwise Convolution", "Dilated Convolution",
        "Deconvolution", "Transposed Convolution", "CNN Architectures"
    ],
    "LeNet": [
        "Architecture", "Layers", "Training Process", "Applications", "Limitations",
        "LeNet-5 Architecture", "Input Size", "Convolution Layers in LeNet", "Pooling in LeNet",
        "Activation in LeNet", "FC Layers in LeNet", "Training Data Used", "Use in Digit Recognition",
        "Limitations for Modern Tasks", "LeNet vs Modern CNNs"
    ],
    "GoogLeNet": [
        "Inception Module", "Efficiency", "Performance", "Feature Extraction", "Depth Reduction",
        "Inception v1", "Auxiliary Classifiers", "1x1 Convolutions", "GoogLeNet vs LeNet",
        "Parallel Convolutions", "Concatenation", "Dimensionality Reduction",
        "Computational Optimization", "Training Challenges"
    ]
}

question_templates = [
    # Level 1 (short)
    ("What is {concept} in {topic}?", "short", "theory"),
    ("Briefly explain {concept} used in {topic}.", "short", "conceptual"),
    ("Define {concept} as applied to {topic}.", "short", "theory"),
    ("List one application of {concept} in {topic}.", "short", "theory"),
    ("State a limitation of using {concept} in {topic}.", "short", "theory"),
    ("Mention a key feature of {concept} within {topic}.", "short", "conceptual"),
    ("Identify where {concept} appears in {topic} architecture.", "short", "conceptual"),

    # Level 2 (medium)
    ("Explain the role of {concept} in {topic} with an example.", "medium", "conceptual"),
    ("Compare {concept1} and {concept2} in the context of {topic}.", "medium", "conceptual"),
    ("What are the advantages of using {concept} in {topic}?", "medium", "theory"),
    ("Describe how {concept} improves performance in {topic}.", "medium", "conceptual"),
    ("Evaluate the impact of {concept1} on {concept2} in {topic}.", "medium", "conceptual"),
    ("Write the steps involved in applying {concept} to {topic}.", "medium", "theory"),

    # Level 3 (long)
    ("Describe how {concept1} and {concept2} interact in {topic}.", "long", "conceptual"),
    ("Discuss the implementation challenges of {concept} in {topic} systems.", "long", "conceptual"),
    ("Perform a complexity analysis for {concept} layer used in {topic}.", "long", "numerical"),
    ("Analyze accuracy changes in {topic} if {concept} is altered significantly.", "long", "numerical"),
    ("Compare results obtained when using {concept1} vs {concept2} in a {topic} application.", "long", "conceptual"),
    ("How does parameter tuning affect {concept} in {topic}?", "long", "numerical"),

    # Level 4 (very long)
    ("Estimate the FLOPs (floating point operations) needed for a {topic} model with input {num1}x{num1} and kernel size {num2}x{num2} for {num3} filters.", "very_long", "numerical"),
    ("Analyze the memory consumption and runtime if the {topic} uses {num1} layers each with {num2} filters of size {num3}x{num3}.", "very_long", "numerical"),
    ("Calculate the parameter size and storage requirements of a full {topic} pipeline using {num1} layers, each with {num2} filters sized {num3}x{num3}.", "very_long", "numerical"),
    ("Given a {topic} model with {num1}x{num1} input, {num2} convolution layers, and {num3} filters each, what is the computational complexity in terms of FLOPs and memory?", "very_long", "numerical"),
    ("Discuss trade-offs in runtime vs accuracy when using {num1}x{num1} vs {num2}x{num2} kernel sizes in {topic}.", "very_long", "numerical"),
    ("Compute and analyze the output size, memory usage, and parameter count for a {topic} model with stride {num1}, padding {num2}, and {num3}x{num3} kernel.", "very_long", "numerical"),
    ("How would changes in filter size from {num1} to {num2} affect accuracy and computational cost in {topic} models? Provide detailed analysis.", "very_long", "numerical"),
    ("If {concept1} fails in a {topic} system while {concept2} is optimized, what degradation or improvement should be expected? Provide full analysis.", "very_long", "conceptual"),
    ("Construct a detailed pipeline where {concept1} and {concept2} jointly contribute to {topic}'s performance.", "very_long", "conceptual"),
    ("Critically analyze a case where {concept1} in CNNs is replaced with {concept2} from GoogLeNet in a hybrid architecture.", "very_long", "conceptual"),
    ("Illustrate a high-level application scenario where {concept1} and {concept2} in {topic} could conflict or synergize. Explain in depth.", "very_long", "conceptual"),
    ("What would happen if both {concept1} and {concept2} are minimized in {topic}? Explore edge cases in design.", "very_long", "conceptual")
]

complexity_to_level = {
    "short": 1,
    "medium": 2,
    "long": 3,
    "very_long": 4,
}

def generate_questions(num_questions, user_level, selected_topic):
    templates = [tpl for tpl in question_templates if complexity_to_level[tpl[1]] == user_level]
    random.shuffle(templates)

    used_templates = set()
    questions = []
    attempts = 0
    max_attempts = num_questions * 50

    while len(questions) < num_questions and attempts < max_attempts:
        if len(used_templates) == len(templates):
            used_templates.clear()
            random.shuffle(templates)

        for tpl in templates:
            if tpl in used_templates:
                continue

            template, _, _ = tpl

            try:
                if "{concept1}" in template and "{concept2}" in template:
                    c1, c2 = random.sample(concepts[selected_topic], 2)
                    question = template.format(concept1=c1, concept2=c2, topic=selected_topic)
                elif any(kw in template for kw in ["{num1}", "{num2}", "{num3}", "{num4}"]):
                    numbers = {
                        'num1': random.randint(1, 5),
                        'num2': random.randint(1, 5),
                        'num3': random.randint(10, 64),
                        'num4': random.randint(10, 64),
                    }
                    placeholders = re.findall(r"{(num\d)}", template)
                    format_args = {ph: numbers[ph] for ph in placeholders}
                    format_args['topic'] = selected_topic
                    question = template.format(**format_args)
                elif "{concept}" in template:
                    c = random.choice(concepts[selected_topic])
                    question = template.format(concept=c, topic=selected_topic)
                else:
                    question = template.format(topic=selected_topic)
            except KeyError:
                continue

            if question not in questions:
                questions.append(question)
                used_templates.add(tpl)
                break
        attempts += 1

    return questions

def main():
    # Custom CSS for styling
    st.markdown("""
        <style>
        /* General styling */
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f8f9fa;
            color: #333;
        }
        .main {
            max-width: 800px;
            margin: auto;
            padding: 20px;
        }
        /* Header styling */
        h1 {
            color: #007bff;
            text-align: center;
            margin-bottom: 20px;
        }
        /* Button styling */
        .stButton>button {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
            transition: background-color 0.3s, transform 0.3s;
        }
        .stButton>button:hover {
            background-color: #0056b3;
            transform: scale(1.05);
        }
        /* Input styling */
        .stNumberInput, .stSelectbox {
            margin-bottom: 20px;
        }
        /* Card styling */
        .card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 20px;
            margin-bottom: 20px;
            color: #333; /* Ensure text is visible */
        }
        </style>
        """, unsafe_allow_html=True)

    st.title("Question Generator")
    st.header("Generate Questions Based on Difficulty Level")
    st.write("Select the number of questions, the difficulty level, and the topic to generate questions.")

    num_questions = st.number_input("Enter number of questions:", min_value=1, max_value=100, value=5)
    level = st.selectbox("Select difficulty level:", [1, 2, 3, 4])
    selected_topic = st.selectbox("Select topic:", list(concepts.keys()))

    if st.button("Generate Questions"):
        questions = generate_questions(num_questions, level, selected_topic)
        for i, question in enumerate(questions, 1):
            st.markdown(f"<div class='card'><strong>{i}. {question}</strong></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()