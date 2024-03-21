from groq import Groq

class GroqAi:
    def __init__(self, apiKey, system_prompt, user):
        self.username = user['username']
        self.system_prompt = system_prompt
        
        self.messages = []

        self.api_key = apiKey

        # set up the model.
        self.Qclient = Groq(
            api_key= self.api_key
        )

        # setUp bot with instruction 
        self.messages.append(
            {
                "content": f"{self.system_prompt} \n Note, Do Not break character from the one set above. You are always evolving, whatever you don't know, ask to be taught. \nCurrent Logged in User is {self.username}",
                "role": "system"
            }
        )


    def Chat(self, message):
        chat_response = self.DeepChat(message)

        return chat_response
    
    def DeepChat(self, message):
        # add to the messages list.
        self.messages.append({
            "content":message,
            "role": 'user'
        })

        completion = self.Qclient.chat.completions.create(
            model='mixtral-8x7b-32768',
            messages = self.messages,
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            # stream=True,
            stop=None,
        )

        response = completion.choices[0].message.content

        # add to the messages list
        self.messages.append({
            "content":response,
            "role": 'assistant'
        })

        return (response)


# # test the model
# system_prompt = """
# You are a super AI assistant that helps user's understand their information much better.
# """
# user = {
#     "username": "Edmond Musiitwa"
# }

# chat = GroqAi("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", system_prompt, user)

# while True:
#     message = input("You: ")
#     print(chat.Chat(message))
