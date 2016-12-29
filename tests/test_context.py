from .base_case import ChatBotTestCase
from chatterbot.conversation import Statement


class AdapterTests(ChatBotTestCase):

    def test_modify_chatbot(self):
        """
        When one adapter modifies its chatbot instance,
        the change should be the same in all other adapters.
        """

        session = self.chatbot.input.chatbot.conversation_sessions.new()
        self.chatbot.input.chatbot.conversation_sessions.update(
            session.id_string,
            Statement('A'), Statement('B')

        session = self.chatbot.output.chatbot.conversation_sessions.get(
            session.id_string
        )

        self.assertEqual(Statement('A'), session.statements.all()[0])
        self.assertEqual(Statement('B'), session.statements.all()[1])
