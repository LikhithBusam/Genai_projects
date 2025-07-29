import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="Gemini 2.5 Flash Summarizer", page_icon="📝", layout="wide")

# Session State Init
defaults = {
    "logged_in": False,
    "user_email": None,
    "api_key": "",
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Manual Login Only
if not st.session_state.logged_in:
    with st.sidebar.form("manual_login_form"):
        st.markdown("### Manual Login")
        manual_email = st.text_input("Email")
        manual_password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if manual_email and manual_password:
                st.session_state.logged_in = True
                st.session_state.user_email = manual_email
                st.rerun()
            else:
                st.sidebar.error("Please enter both email and password.")

# Sidebar Navigation
st.sidebar.title("Navigation")

if st.session_state.logged_in:
    st.sidebar.markdown(f"**Logged in as:** {st.session_state.user_email}")
    if st.sidebar.button("Logout"):
        for key, val in defaults.items():
            st.session_state[key] = val
        st.rerun()

    menu = st.sidebar.radio("Go to", ["API Key Management", "Text Summarization"])

    # API Key Page
    if menu == "API Key Management":
        st.sidebar.subheader("Enter your Gemini API Key")
        input_key = st.sidebar.text_input("Gemini API Key (required)", type="password", value=st.session_state.api_key)
        if st.sidebar.button("Save API Key"):
            if input_key.strip():
                st.session_state.api_key = input_key.strip()
                st.sidebar.success("API Key saved successfully!")
            else:
                st.sidebar.error("Please enter a valid API Key.")

    # Text Summarization Page
    elif menu == "Text Summarization":
        if not st.session_state.api_key:
            st.warning("Please enter your Gemini API Key in API Key Management.")
            st.stop()

        genai.configure(api_key=st.session_state.api_key)
        model = genai.GenerativeModel(model_name="gemini-2.5-flash")

        st.title("📝 Gemini 2.5 Flash Text Summarizer")
        input_text = st.text_area("Paste the text you want to summarize", height=300)

        if st.button("Summarize"):
            if input_text.strip():
                with st.spinner("Summarizing..."):
                    try:
                        prompt = f"Summarize the following text clearly and concisely:\n\n{input_text}"
                        response = model.generate_content(prompt)
                        summary = response.text
                        st.subheader("Summary")
                        st.write(summary)

                        st.download_button(
                            label="Download Summary as TXT",
                            data=summary,
                            file_name="summary.txt",
                            mime="text/plain"
                        )
                    except Exception as e:
                        st.error(f"Summarization failed: {e}")
            else:
                st.warning("Please enter some text to summarize.")
else:
    st.sidebar.info("Please log in with your email and password to continue.")

# Footer
st.caption("🔗 Powered by Google's Gemini 2.5 Flash LLM")
