import os
from dotenv import load_dotenv
from agents import Agent, Runner, trace, function_tool
import asyncio

load_dotenv(override=True)


import resend

resend.api_key = os.environ["RESEND_API_KEY"]


@function_tool()
def send_email(subject: str, body: str):
    """
    Send an email with the given body to me.
    """
    print(f"Sending email: {body}")
    resend.Emails.send(
        {
            "from": "onboarding@resend.dev",
            "to": "me@phillippbertram.de",
            "subject": subject,
            "html": body,
        }
    )


async def joke_agent():
    agent = Agent(
        name="Jokester", instructions="You are a joke teller", model="gpt-4o-mini"
    )
    # print(agent)

    # this will print the trace of the agent on openai https://platform.openai.com/traces
    with trace("Telling a joke"):
        result = await Runner.run(agent, "Tell a joke about Chuck Norris")
        print(result.final_output)


async def main():
    print("Starting the agent")

    # await joke_agent()

    instructions1 = """
    You are a sales agent working for a company that sells a product called "AskLance" which is a platform for freelancers to find work.
    You write professional, serious cold emails.
    """

    instructions2 = """
    You are a sales agent working for a company that sells a product called "AskLance" which is a platform for freelancers to find work.
    You write witty, engaging cold emails that are likely to get a response.
    """

    instructions3 = """
    You are a sales agent working for a company that sells a product called "AskLance" which is a platform for freelancers to find work.
    You write concise, to th epoint cold emails.
    """

    sales_agent_1 = Agent(
        name="ProfessionalSales Agent", instructions=instructions1, model="gpt-4o-mini"
    )
    sales_agent_2 = Agent(
        name="Engaging Sales Agent", instructions=instructions2, model="gpt-4o-mini"
    )
    sales_agent_3 = Agent(
        name="Busy Sales Agent", instructions=instructions3, model="gpt-4o-mini"
    )

    subject_writer = Agent(
        name="Email subject writer",
        instructions="You write a subject for the email. You are given a text email body which might contain markdown or other formatting and you need to write a subject for the email. The subject should be a single line and should be a single sentence. The subject should be a single line and should be a single sentence.",
        model="gpt-4o-mini",
    )
    html_converter = Agent(
        name="HTML email body Converter",
        instructions="You convert the given text into HTML email Body. You are given a text email body which might contain markdown or other formatting and you need to convert it into HTML email body with simplert, clear, compelling layout and design",
        model="gpt-4o-mini",
    )
    email_manager_instructions = """
    You are an email formatter and sender. You receive the body of an email to be sent.
    you first use the subject_writer tool to write a subject for the email, then use the html_conevrter tool to convert the body to HRML.
    Finally, you use the send_email tool to send the email with the subject and HTML body.
    """
    email_manager = Agent(
        name="Email Manager",
        instructions=email_manager_instructions,
        tools=[
            subject_writer.as_tool(
                tool_name="subject_writer",
                tool_description="Write a subject for the email",
            ),
            html_converter.as_tool(
                tool_name="html_converter",
                tool_description="Convert the given text into HTML email Body",
            ),
            send_email,
        ],
        handoff_description="Convert an email to HTML and send it",
    )

    # sales_picker = Agent(name="Sales Picker", instructions="You pick the best sales agent to send the email from the given options. Imagine  are a customer and pick the one you are most likely to respond to. Do not give an explanation; reply with the selected email only.", model="gpt-4o-mini")
    # message = "Send a cold email"
    # with trace("Parallel cold emails"):
    #     results = await asyncio.gather(
    #         Runner.run(sales_agent_1, message),
    #         Runner.run(sales_agent_2, message),
    #         Runner.run(sales_agent_3, message),
    #     )

    #     outputs = [result.final_output for result in results]
    #     # for output in outputs:
    #     #     print(output)

    #     emails = "Cold sales emails:\n\n".join(outputs)

    #     best = await Runner.run(sales_picker, emails)
    #     print(f"Best sales agent: \n{best.final_output}")

    sales_manager_instructions = """
    You are a sales manager working for a company that sells a product called 'AskLance'. 
    You are given a list of cold sales emails and you need to pick the best one to send to the customer.
    You never generate sales emails yourself; use always the tools.
    You try all 3 sales_agent tools once before choosing the best one.
    You can use the tools multiple times if you're not satisfied with the results from the first try.
    You pick the single best email (and only the best email) and send it to the customer using the send_email tool.
    After picking the best email, you handoff to the Email Manager agent to format and send the email.
    """

    tools = [
        sales_agent_1.as_tool(
            tool_name="sales_agent1", tool_description="Write a cold sales email"
        ),
        sales_agent_2.as_tool(
            tool_name="sales_agent2", tool_description="Write a cold sales email"
        ),
        sales_agent_3.as_tool(
            tool_name="sales_agent3", tool_description="Write a cold sales email"
        ),
    ]
    sales_manager = Agent(
        name="Sales Manager",
        instructions=sales_manager_instructions,
        model="gpt-4o-mini",
        tools=tools,
        handoffs=[email_manager],
    )
    message = "Send a cold email addressed to 'Dear CEO'"

    with trace("Sales Manager with Handoff Email Manager"):
        result = await Runner.run(sales_manager, message)
        print(result.final_output)


if __name__ == "__main__":

    asyncio.run(main())
