from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Myproject():
	"""Myproject crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended

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

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def email_specialist(self) -> Agent:
		return self.email_specialist_agent

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
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
		"""Creates the Myproject crew"""
		return Crew(
			agents=[self.email_specialist()],  # Call the method to get the Agent instance
			tasks=[self.write_email_task()],   # Call the method to get the Task instance
			process=Process.sequential,
			verbose=True,
		)

