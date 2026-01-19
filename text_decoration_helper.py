from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console(
    force_terminal=True,
    emoji=True,
)

def __get_intro_text():
    intro_message = Text()
    intro_message.append("Powered by Gemini 2.5 Flash & LangChain v1\n")
    intro_message.append("I can help you browse and edit files!\n", style="bold")
    intro_message.append("Type ", style="none")
    intro_message.append("q, ", style="bold yellow")
    intro_message.append("quit", style="bold yellow")
    intro_message.append(" or ", style="none")
    intro_message.append("exit", style="bold yellow")
    intro_message.append(" to end the session.", style="none")

    return intro_message

def decorate_text(
        title="🤖Code Assistant",
        message=__get_intro_text()):
    """ Use rich library to decorate and display the decorated text """
    panel = Panel(
        message,
        title=title,
        border_style="cyan",
        box=box.ROUNDED,
        padding=(1, 2),
    )

    console.print(panel)

def flatten_ai_response(response):
    """ Filter the AI response and return a flattened version of the response."""
    if isinstance(response, list):
        return ''.join(item.get('text') for item in response if item.get('type') == 'text')
    elif isinstance(response, dict):
        return response.get('text')
    else:
        return response