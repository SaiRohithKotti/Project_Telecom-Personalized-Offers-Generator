import streamlit as st
import pandas as pd
from openai import OpenAI  # Import the new OpenAI client

# Initialize the OpenAI client
client = OpenAI(api_key=""
                
# Load customer data
@st.cache_data
def load_data():
    return pd.read_csv("customer_data.csv")

# Function to generate personalized offer using LLM
def generate_offer(customer_data):
    prompt = f"""
    Analyze the following customer data and generate a personalized offer:
    - Name: {customer_data['Name']}
    - Age: {customer_data['Age']}
    - Plan Type: {customer_data['PlanType']}
    - Monthly Spend: ${customer_data['MonthlySpend']}
    - Contract Length: {customer_data['ContractLength']} months
    - Data Usage: {customer_data['UsageGB']} GB
    - Complaints: {customer_data['Complaints']}

    Suggest a personalized offer to retain or upsell to this customer.
    """
    response = client.completions.create(
        model="text-davinci-003",  # Use GPT-3.5
        prompt=prompt,
        max_tokens=150,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

# Streamlit app
def main():
    st.title("Telecom Personalized Offers Generator")
    st.write("Upload customer data and generate personalized offers using LLM.")

    # Load customer data
    data = load_data()
    st.write("### Customer Data")
    st.write(data)

    # Select a customer
    customer_id = st.selectbox("Select Customer ID", data["CustomerID"].unique())
    customer_data = data[data["CustomerID"] == customer_id].iloc[0]

    st.write("### Selected Customer Details")
    st.write(customer_data)

    # Generate offer
    if st.button("Generate Personalized Offer"):
        offer = generate_offer(customer_data)
        st.write("### Personalized Offer")
        st.write(offer)

if __name__ == "__main__":
    main()
