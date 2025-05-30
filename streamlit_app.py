import streamlit as st
import pandas as pd
from hsn_data_loader import HSNDataLoader
from hsn_code_validator import HSNCodeValidator
from hsn_code_suggestor import HSNCodeSuggestor
import plotly.express as px

# Page config
st.set_page_config(
    page_title="HSN Code Validator & Suggestor",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #e6ffe6;
        border: 1px solid #b3ffb3;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #ffe6e6;
        border: 1px solid #ffb3b3;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'hsn_agent' not in st.session_state:
    try:
        loader = HSNDataLoader("HSN_SAC.xlsx")
        df = loader.get_dataframe()
        st.session_state.validator = HSNCodeValidator(df)
        st.session_state.suggestor = HSNCodeSuggestor(df)
        st.session_state.df = df
    except Exception as e:
        st.error(f"Error initializing the application: {str(e)}")
        st.stop()

# Title and description
st.title("🔍 HSN Code Validator & Suggestor")
st.markdown("""
This application helps you validate HSN (Harmonized System Nomenclature) codes and find relevant codes based on product descriptions.
Choose a mode below to get started.
""")

# Main tabs
tab1, tab2, tab3 = st.tabs(["HSN Code Validation", "Code Suggestion", "Browse Codes"])

# Tab 1: HSN Code Validation
with tab1:
    st.header("HSN Code Validator")
    hsn_code = st.text_input("Enter HSN Code", placeholder="e.g., 01011010")
    
    if st.button("Validate Code"):
        if hsn_code:
            is_valid, result = st.session_state.validator.validate_code(hsn_code)
            if is_valid:
                st.markdown(f'<div class="success-box">✅ {result}</div>', unsafe_allow_html=True)
                
                # Show hierarchy
                hierarchy = st.session_state.validator.validate_hierarchy(hsn_code)
                if hierarchy:
                    st.subheader("Code Hierarchy")
                    for parent in hierarchy:
                        parent_desc = st.session_state.validator.validate_code(parent)[1]
                        st.info(f"{parent}: {parent_desc}")
            else:
                st.markdown(f'<div class="error-box">❌ {result}</div>', unsafe_allow_html=True)

# Tab 2: Code Suggestion
with tab2:
    st.header("HSN Code Suggestor")
    description = st.text_area("Enter Product Description", placeholder="e.g., live horses")
    
    if st.button("Get Suggestions"):
        if description:
            suggestions = st.session_state.suggestor.suggest(description)
            if isinstance(suggestions, pd.DataFrame):
                st.success("Found the following suggestions:")
                for _, row in suggestions.iterrows():
                    st.info(f"**{row['HSNCode']}**: {row['Description']}")
            else:
                st.warning(suggestions)

# Tab 3: Browse Codes
with tab3:
    st.header("Browse HSN Codes")
    
    # Search and filter
    search_term = st.text_input("Search in descriptions", "")
    filtered_df = st.session_state.df
    
    if search_term:
        filtered_df = filtered_df[filtered_df['Description'].str.contains(search_term.lower(), na=False)]
    
    # Display data with pagination
    page_size = st.selectbox("Rows per page", [10, 25, 50, 100])
    total_pages = len(filtered_df) // page_size + (1 if len(filtered_df) % page_size > 0 else 0)
    page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
    
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    st.dataframe(
        filtered_df.iloc[start_idx:end_idx][['HSNCode', 'Description']],
        use_container_width=True
    )
    
    # Show statistics
    st.subheader("Code Length Distribution")
    code_lengths = filtered_df['HSNCode'].str.len()
    length_dist = code_lengths.value_counts().sort_index()
    fig = px.bar(
        x=length_dist.index,
        y=length_dist.values,
        labels={'x': 'Code Length', 'y': 'Count'},
        title='Distribution of HSN Code Lengths'
    )
    st.plotly_chart(fig)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center">
    <p>HSN Code Validator & Suggestor | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True) 