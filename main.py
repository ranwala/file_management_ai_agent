import uuid
from text_decoration_helper import decorate_text

from ai_service import AIService

def main():
    msg_id = str(uuid.uuid4())
    end_session_set = {'q', 'quit', 'exit'}
    try:
        # Generate instance for AI Service
        ai_service = AIService(msg_id)

        # Display the introduction text
        decorate_text()

        while True:
            user_in = input('\nYou: ')

            if user_in.lower() in end_session_set:
                break

            response = ai_service.ask_ai(user_in)

            decorate_text('Assistant', f'{response}')

    except FileNotFoundError as fe:
        print(f'File not found: {fe}')
    except PermissionError as pe:
        print(f'Permission Error: {pe}')
    except OSError as oe:
        print(f'Os Error: {oe}')
    except AttributeError as ae:
        print(f'Attribute Error: {ae}')
    except ValueError as ve:
        print(f'ValueError: {ve}')
    except Exception as e:
        print(f'Somthing went wrong: {e}')


if __name__ == '__main__':
    main()