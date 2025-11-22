# pages/contact.py
import streamlit as st

def contact_page():
    # Page Config
    st.set_page_config(page_title="📞 Contact", layout="centered")

    # Header
    st.title("📬 Contact Information")
    st.markdown("Feel free to reach out — I’d love to connect or collaborate!")

    # Profile Section
    st.markdown("""
    ### 👩 Rahma Anggana Rarastyasa  
    📍 **Location:** Indonesia  
    ✉️ **Email:** [rahmaanggana04@gmail.com](mailto:rahmaanggana04@gmail.com)  
    🔗 **LinkedIn:** [www.linkedin.com/in/rahma-anggana-rarastyasa](https://www.linkedin.com/in/rahma-anggana-rarastyasa)  
    💻 **GitHub:** [github.com/rarastyasa](https://github.com/rarastyasa)
    """)

    st.markdown("---")

    # Closing Section
    st.success("💬 I’m always open to discussing new opportunities, projects, or research collaborations!")

# Run directly for local test
if __name__ == "__main__":
    contact_page()