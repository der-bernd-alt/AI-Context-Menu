from openai import OpenAI
import dotenv
dotenv.load_dotenv('.env')

class OpenAiClient():
    def __init__(self) -> None:
        self.client = OpenAI()


    def get_openai_response(self, prompt: str, model: str = "gpt-3.5-turbo", max_tokens: int = 100) -> tuple[str, int]:
        """
        Makes a call to the OpenAI API with the provided prompt.

        Parameters:
            prompt (str): The input prompt to send to the OpenAI API.
            model (str): The model to use for the OpenAI API. Default is "gpt-3.5-turbo".
            max_tokens (int): The maximum number of tokens to generate in the response.

        Returns:
            str: The generated response from the OpenAI API.
        """
        try:
            # Create a completion using the OpenAI API
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens
            )
            
            # Extract and return the content of the response
            return response.choices[0].message.content.strip(), response.usage.total_tokens
        
        except Exception as e:
            raise Exception(e)

if __name__ == "__main__":
# Example usage
    prompt = "What is the capital of France?"
    chatbot = OpenAiClient()
    response, tokens_used = chatbot.get_openai_response(prompt)
    print(response, "Total tokens used: " + str(tokens_used))
