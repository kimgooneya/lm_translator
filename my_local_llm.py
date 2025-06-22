import lmstudio as lms

class MyLocalLLM:
    def __init__(self, model_name):
        self.model = lms.llm(model_name)

    def respond(self, prompt):
        return self.model.respond(prompt)