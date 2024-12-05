import streamlit as st
#The app
# Apply the same custom CSS for the entire app
st.markdown("""
<style>
    /* Base styling */
    body {
        background-color: #121212;
        color: #e0e0e0;
        font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1E1E1E;
        color: #e0e0e0;
        border-right: 2px solid #2C2C2C;
    }

    /* Sidebar header */
    .sidebar-header {
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
        border-radius: 0 0 15px 15px;
    }

    .sidebar-header h1 {
        color: white;
        margin: 0;
        font-size: 1.5em;
        font-weight: 700;
    }

    /* Section headers */
    h1, h2, h3, h4, h5, h6 {
        color: #4CAF50;
        font-weight: 700;
    }

    .stMarkdown {
        color: #e0e0e0;
    }

    /* For the main body */
    .main-title {
        text-align: center;
        color: #4CAF50;
        margin-bottom: 30px;
        font-weight: 700;
    }

    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: #2C2C2C !important;
        color: #e0e0e0 !important;
        border-radius: 10px;
        border: 1px solid #404040 !important;
        padding: 10px;
        transition: all 0.3s ease;
    }

    .stSelectbox > div > div:hover {
        border-color: #4CAF50 !important;
        box-shadow: 0 0 10px rgba(76, 175, 80, 0.3);
    }

    /* Selectbox label styling */
    .stSelectbox label {
        color: #4CAF50;
        font-weight: 600;
        margin-bottom: 5px;
    }

    /* Sidebar input box (like selectbox) */
    .stSelectbox div > div input {
        color: #e0e0e0 !important;
        background-color: #2C2C2C !important;
        border-color: #404040 !important;
    }

    /* Sidebar input box focus */
    .stSelectbox div > div input:focus {
        color: #e0e0e0 !important;
        background-color: #2C2C2C !important;
        border-color: #4CAF50 !important;
    }

    /* Sidebar dropdown options styling */
    .stSelectbox div[role="listbox"] div[role="option"] {
        color: #e0e0e0 !important;
        background-color: #1E1E1E !important;
    }

    .stSelectbox div[role="listbox"] {
        color: #e0e0e0 !important;
        background-color: #1E1E1E !important;
    }

    /* Custom styling for sidebar buttons */
    .stButton > button {
        background-color: #4CAF50 !important;
        color: #ffffff !important;
        border-radius: 10px;
        border: none !important;
        padding: 10px;
        font-size: 1.1em;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #388E3C !important;
    }

</style>
""", unsafe_allow_html=True)

# Issues Faced Section
st.markdown("<h2 style='color:#4CAF50;'>Issues Faced</h2>", unsafe_allow_html=True)

st.subheader("Download Cap ons Backblaze")
st.write("Backblaze imposes a download limit, restricting frequent access to the dataset, which hinders running the Streamlit app repeatedly on the cloud.")

st.subheader("Large Dataset Size")
st.write("The size of the dataset exacerbates the download cap issue, limiting our ability to work with it efficiently.")

# Next Steps Section
st.markdown("<h2 style='color:#4CAF50;'>Next Steps</h2>", unsafe_allow_html=True)

st.subheader("Expand EDA Functionality")
st.write("Incorporate additional functions from the exploratory data analysis (EDA) conducted by each group member in their individual Jupyter notebooks.")

st.subheader("Enhance EDA Content in the App")
st.write("Integrating the diverse EDA approaches will enrich the app’s EDA section, making it more comprehensive and informative.")
