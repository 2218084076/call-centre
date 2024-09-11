import logging

from openai import AsyncOpenAI

from call_centre.config import settings
from call_centre.utils.constant import PROMPT_WORDS

client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY
)

_res = [
    '''1. Greeting: Yes\n
2. Self-introduction: No\n
3. Closing phrase: No\n
4. Statement before verifying information: No\n
5. Re-verification of registrant's identity before registration: No\n
6. Verification of the mobile phone number for registration: No\n
7. Verification of personal details of the customer: No\n
8. Inquiry about whether IDD roaming service is needed: No\n
9. Remind the customer to take a survey - NPS: No\n
10. Provide the customer with ways to inquire and contact: No
'''.strip(),
'''
1. Greeting: Yes\n
2. Self-introduction: Yes\n
3. Closing phrase: No\n
4. Statement before verifying information: No\n
5. Re-verification of registrant's identity before registration: No\n
6. Verification of the mobile phone number for registration: Yes\n
7. Verification of personal details of the customer: Yes\n
8. Inquiry about whether IDD roaming service is needed: No\n
9. Remind the customer to take a survey - NPS: No\n
10. Provide the customer with ways to inquire and contact: Yes
'''.strip()
]


class GPTS:
    def __init__(self):
        self.temperature = 1
        self.prompts: str = PROMPT_WORDS
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
        self.messages = [
            {"role": "system", "content": self.prompts},
        ]

    async def ask(
            self,
            question: str,
            temperature: float = 1
    ):
        """
        ask question
        :param temperature:
        :param question:
        :return:
        """
        new_msg = {
            'role': 'user',
            'content': question
        }
        self.logger.info('New message: %s', new_msg)
        # merge messages
        self.messages.append(new_msg)
        # send message to gpt
        respo = await client.chat.completions.create(
            model=settings.MODEL,
            messages=self.messages,
            temperature=temperature
        )
        _answer = respo.choices[0].message.content
        self.messages.append({'role': 'assistant', 'content': _answer})
        return self.messages

    def update_prompts(self, prompts: str):
        self.prompts = prompts
        self.messages = [
            {"role": "system", "content": self.prompts},
        ]
        return self.prompts

    def update_temperature(self, temperature: float = 1):
        """
        update temperature
        :param temperature:
        :return:
        """
        self.temperature = temperature
        return self.temperature

    async def custom_chat_completions(
            self,
            question: str,
            audio_content: str,
    ):
        """
        custom chat completions
        :param audio_content:
        :param question:
        :return:
        """
        question = f"""{question}. 
        New transcript content is as follows: {audio_content}
                """
        new_msg = {
            'role': 'user',
            'content': question.strip()
        }
        # merge messages
        self.messages.append(new_msg)
        try:
            respo = await client.chat.completions.create(
                model=settings.MODEL,
                messages=self.messages,
            )
            _answer = respo.choices[0].message.content
        except Exception as ex:
            _answer = _res
            logging.warning(ex)
        self.messages.append({'role': 'assistant', 'content': _answer})
        return self.messages

    def init_messages_context(self):
        """
        init messages context
        :return:
        """
        self.messages = [
            {"role": "system", "content": self.prompts},
        ]
