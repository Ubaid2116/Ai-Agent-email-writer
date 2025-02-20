from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@CrewBase
class Myproject():
    """Myproject crew"""

    def __init__(self):
        # Initialize the agent first
        self.email_specialist_agent = Agent(
            role="Professional Email Specialist",
            goal="Write perfect, professional emails for any situation",
            backstory="""You are an expert email writer with years of experience crafting professional
                communications. You understand proper email etiquette, tone, and structure
                for various business and personal situations.""",
            verbose=True,
            llm_config={
                "provider": "google",
                "api_key": os.getenv('GEMINI_API_KEY'),
                "model": os.getenv('MODEL'),
                "temperature": 0.7
            }
        )

    @agent
    def email_specialist(self) -> Agent:
        return self.email_specialist_agent

    @task
    def write_email_task(self) -> Task:
        return Task(
            description="""Write a professional email for the following context:
                Topic: {email_topic}
                Recipient: {recipient}
                Tone: {tone}
                Additional Context: {context}""",
            expected_output="""A professional email with subject line and body text, formatted appropriately.
                Include a clear subject line, professional greeting, well-structured body, and appropriate closing.""",
            agent=self.email_specialist_agent
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.email_specialist()],  # Call the method to get the Agent instance
            tasks=[self.write_email_task()],     # Call the method to get the Task instance
            process=Process.sequential,
            verbose=True,
        )

######################################
# Streamlit UI for AI Agent Email WRITER
######################################
import streamlit as st
from myproject.crew import Myproject

def main():
    # Dark mode custom CSS styling with an attractive header
    st.markdown("""
    <style>
    body {
        background-color: #2d2d2d;
        color: #f0f0f0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .header {
        background-color: #424242;
        padding: 30px;
        border-radius: 8px;
        color: #ffffff;
        text-align: center;
        margin-bottom: 20px;
        font-size: 2.5em;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .card {
        background-color: #424242;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #333;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    .footer {
        text-align: center;
        font-size: 0.9em;
        color: #ccc;
        margin-top: 30px;
        padding-top: 10px;
        border-top: 1px solid #444;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header Section with attractive styling
    st.markdown("<div class='header'>AI AGENT EMAIL WRITER 🚀</div>", unsafe_allow_html=True)
    st.write("Let me help you craft the perfect professional email that you can copy and send through your preferred email service!")

    # Example use cases
    with st.expander("📝 Example Use Cases"):
        st.write("""
        - Job Application Emails
        - Meeting Request Emails
        - Thank You Notes
        - Follow-up Emails
        - Business Proposals
        - Customer Service Responses
        - And more!
        """)

    # Input fields
    col1, col2 = st.columns(2)
    with col1:
        email_topic = st.text_input("Email Subject/Topic:", help="What is this email about?")
    with col2:
        recipient = st.text_input("Recipient Name:", help="Who are you writing to?")

    tone = st.select_slider(
        "Email Tone:",
        options=["Very Formal", "Professional", "Neutral", "Friendly", "Casual"],
        value="Professional",
        help="Select the tone of your email"
    )

    context = st.text_area(
        "Email Context:",
        help="Provide details about what you want to communicate in this email",
        placeholder="Example: I want to request a meeting to discuss the Q1 project progress..."
    )

    if st.button("✨ Generate Email", type="primary"):
        if email_topic and recipient:
            with st.spinner("Crafting your professional email..."):
                try:
                    # Prepare inputs for the crew
                    inputs = {
                        "email_topic": email_topic,
                        "recipient": recipient,
                        "tone": tone,
                        "context": context or "No additional context provided."
                    }
                    
                    # Run the crew and get the email result
                    result = Myproject().crew().kickoff(inputs=inputs)
                    
                    # Convert the result to a string (or use a dedicated attribute if available)
                    result_str = result.content if hasattr(result, "content") else str(result)
                    if not result_str:
                        result_str = "No content generated. Please try again."
                    
                    st.success("✅ Email Generated Successfully!")
                    
                    # Create tabs for Email Preview and Raw Text
                    tab1, tab2 = st.tabs(["📧 Email Preview", "📝 Raw Text"])
                    
                    with tab1:
                        st.header("Email Preview")
                        replaced_result = result_str.replace('\n', '<br>')
                        st.markdown(f"<div class='card'>{replaced_result}</div>", unsafe_allow_html=True)
                    
                    with tab2:
                        st.text_area("", value=result_str, height=300, key="email_content")
                    
                    # Action buttons
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        st.button("📋 Copy to Clipboard", on_click=lambda: st.write("Email copied!"))
                    with col_btn2:
                        st.markdown("""
                        <div style='text-align: right;'>
                            <a href='https://mail.google.com/mail/?view=cm&fs=1' target='_blank'>
                                <button style='padding: 5px 10px; background-color:#1a73e8; color:white; border:none; border-radius:4px;'>Open Gmail</button>
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Display tips for sending
                    with st.expander("📌 Tips for Sending"):
                        st.write("""
                        1. Copy the generated email from the 'Raw Text' tab.
                        2. Open your preferred email service (Gmail, Outlook, etc.).
                        3. Create a new email.
                        4. Paste the copied content.
                        5. Add the recipient's email address.
                        6. Review one final time.
                        7. Send!
                        """)
                        
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("⚠️ Please provide at least the email topic and recipient name.")
    
    # Footer Section
    st.markdown("<div class='footer'>Developed by Muhammad Ubaid Hussain - AI Agent Developer</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
