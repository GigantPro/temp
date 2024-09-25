import requests
from mistralai import Mistral
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

api_key = 'MQgygC1uHjcu76EvZBHeO13nqy7s0hYo'
model = "mistral-large-latest"

class ChatApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.message_input = TextInput(hint_text='Enter your message', size_hint=(1, 0.2))
        self.send_button = Button(text='Request', size_hint=(1, 0.2))
        self.response_label = Label(text='Response will be here', size_hint=(1, 0.6))
        self.send_button.bind(on_press=self.send_message)
        self.layout.add_widget(self.message_input)
        self.layout.add_widget(self.send_button)
        self.layout.add_widget(self.response_label)

        return self.layout

    def send_message(self, instance):
        client = Mistral(api_key=api_key)
        try:
            chat_response = client.chat.complete(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": self.message_input.text,
                    },
                ]
            )
            if chat_response.status_code == 200:
                result = chat_response.json()
                self.response_label.text = f'Response: {result["choices"][0]["message"]["content"]}'
            else:
                self.response_label.text = f'Error: {chat_response.status_code}\nResponse text: {chat_response.text}'
        except requests.exceptions.RequestException as e:
            self.response_label.text = f'Error: {e}'

if __name__ == '__main__':
    ChatApp().run()