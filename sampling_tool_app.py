import math
import random
import streamlit as st

def calculate_sample_size(population_size, confidence_level, expected_error_rate, tolerable_error_rate, business_risk, audit_risk):
    # Adjust tolerable error rate based on risk levels
    risk_factor = 1 - ((business_risk + audit_risk) / 200)
    adjusted_tolerable_error = tolerable_error_rate * risk_factor

    # Z-values for confidence levels
    z_values = {90: 1.645, 95: 1.96, 99: 2.576}
    z = z_values.get(confidence_level, 1.96)

    # Sample size calculation
    p = expected_error_rate / 100
    e = adjusted_tolerable_error / 100
    sample_size = ((z ** 2) * p * (1 - p)) / (e ** 2)
    adjusted_sample_size = (population_size * sample_size) / (sample_size + (population_size - 1))

    return math.ceil(adjusted_sample_size), adjusted_tolerable_error

def generate_sample_sequence(population_size, sample_size, start_range, end_range):
    # Create a range for sampling
    population_range = range(max(1, start_range), min(population_size + 1, end_range + 1))
    return random.sample(population_range, sample_size)

# Streamlit App
st.title("Enhanced Sample Size and Sequence Calculator")

# Inputs
population_size = st.number_input("Population Size:", min_value=1, step=1)
confidence_level = st.selectbox("Confidence Level (90, 95, 99):", options=[90, 95, 99])
expected_error_rate = st.number_input("Expected Error Rate (%):", min_value=0.0, max_value=100.0, step=0.1)
tolerable_error_rate = st.number_input("Tolerable Error Rate (%):", min_value=0.0, max_value=100.0, step=0.1)
business_risk = st.slider("Business Risk (0-100):", 0, 100)
audit_risk = st.slider("Audit Risk (0-100):", 0, 100)
start_range = st.number_input("Sample Start Range:", min_value=1, step=1)
end_range = st.number_input("Sample End Range:", min_value=1, step=1)

if st.button("Calculate Sample Size"):
    # Calculate sample size and tolerable error
    sample_size, adjusted_tolerable_error = calculate_sample_size(
        population_size, confidence_level, expected_error_rate, tolerable_error_rate, business_risk, audit_risk
    )
    st.write(f"Calculated Sample Size: {sample_size}")
    st.write(f"Adjusted Tolerable Error Rate: {adjusted_tolerable_error:.2f}%")

    # Generate and display the sample sequence
    sample_sequence = generate_sample_sequence(population_size, sample_size, start_range, end_range)
    st.write(f"Sample Sequence: {sample_sequence}")
