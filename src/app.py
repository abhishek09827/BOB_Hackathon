__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from ai_gen.crew import NewsletterGenCrew


class SmartGen:

    def load_html_template(self):
        with open("src/ai_gen/config/ai_template.html", "r") as file:
            html_template = file.read()

        return html_template

    def generate_report(self, topic, personal_message):
        inputs = {
            "topic": topic,
            "personal_message": personal_message,
            "html_template": self.load_html_template(),
        }
        return NewsletterGenCrew().crew().kickoff(inputs=inputs)

    def report_generation(self):

        if st.session_state.generating:
            st.session_state.report = self.generate_report(
                st.session_state.topic, st.session_state.personal_message
            )

        if st.session_state.report and st.session_state.report != "":
            with st.container():
                st.write("Report generated successfully!")
                st.download_button(
                    label="Download HTML file",
                    data=st.session_state.report,
                    file_name="report.html",
                    mime="text/html",
                )
            st.session_state.generating = False

    def sidebar(self):
        with st.sidebar:
            st.title("AI Market Researcher")

            st.write(
                """
                To generate a reaserch report, enter a topic and a text description. \n
                Your team of AI agents will generate a report for you!
                """
            )

            st.text_input("Topic", key="topic", placeholder="USA Stock Market")

            st.text_area(
                "Your text description (to include at the top of the report)",
                key="personal_message",
              
            )

            if st.button("Generate Report"):
                st.session_state.generating = True

    def render(self):
        st.set_page_config(page_title="AI Market Researcher", page_icon="🔍")

        if "topic" not in st.session_state:
            st.session_state.topic = ""

        if "personal_message" not in st.session_state:
            st.session_state.personal_message = ""

        if "report" not in st.session_state:
            st.session_state.report = ""

        if "generating" not in st.session_state:
            st.session_state.generating = False

        self.sidebar()

        self.report_generation()



SmartGen().render()
