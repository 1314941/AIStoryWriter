import Writer.Config

import ollama



def InitClient(_ClientHost:str = "http://10.1.65.4:11434"):
    return ollama.Client(host=_ClientHost)


def ChatAndStreamResponse(_Client, _Messages, _Model:str="llama3"):

    # Disallow empty garbage responses
    if (Writer.Config.DEBUG):
        print("--------- Message History START ---------")
        print(_Messages)
        print("--------- Message History END --------")

    while True:
        Stream = _Client.chat(
            model=_Model,
            messages=_Messages,
            stream=True,
            options=dict(seed=Writer.Config.SEED)
        )
        print(f"DEBUG: Using Model {_Model}")
        ThisMessage:str = StreamResponse(Stream)

        # Check if it's empty
        if not ThisMessage["content"].isspace():
            _Messages.append(ThisMessage)
            return _Messages
        else:
            print("WARNING: LLM RETURNED ONLY WHITESPACE!")
            _Messages.append(BuildUserQuery("Sorry, but you returned an empty string, please try again!"))

def StreamResponse(_Stream):
  
    Response:str = ""
    for chunk in _Stream:
        ChunkText = chunk['message']['content']
        Response += ChunkText

        print(ChunkText, end='', flush=True)
    print("\n\n\n")
    return {'role': 'assistant', 'content': Response}

def BuildUserQuery(_Query:str):
    return {'role': 'user', 'content': _Query}

def BuildSystemQuery(_Query:str):
    return {'role': 'system', 'content': _Query}

def BuildAssistantQuery(_Query:str):
    return {'role': 'assistant', 'content': _Query}

def GetLastMessageText(_Messages:list):
    return _Messages[-1]["content"]

