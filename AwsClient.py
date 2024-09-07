import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
import dotenv

creds = dotenv.dotenv_values()

class AwsClient():
  def __init__(self) -> None:
    self.client = boto3.client("bedrock-runtime",
                               aws_access_key_id=creds["AWS_SDK_KEY"],
                               aws_secret_access_key=creds["AWS_SDK_VALUE"],
              region_name=creds["REGION_NAME"])
    self.model_id = creds["MODEL_ID"]
     
  def get_bedrock_response(self, prompt: str, max_tokens: int = 100) -> str:
    """
    Calls the Amazon Bedrock service to generate a response from a foundation model.

    Parameters:
        prompt (str): The input prompt to send to the model.
        max_tokens (int): The maximum number of tokens to generate in the response.

    Returns:
        str: The generated response from the Bedrock model.
    """
    # Create a Bedrock client

    # Start a conversation with the user message.
    conversation = [
        {
            "role": "user",
            "content": [{"text": prompt}],
        }
    ]

    try:
      # Send the message to the model, using a basic inference configuration.
      response = self.client.converse(
          modelId=self.model_id,
          messages=conversation,
          inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
      )

      # Extract and print the response text.
      response_text = response["output"]["message"]["content"][0]["text"]
      print(response_text)

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{self.model_id}'. Reason: {e}")
        exit(1)


    except (NoCredentialsError, PartialCredentialsError):
        return "Error: AWS credentials not found or incomplete."
    except Exception as e:
        return f"Error calling Bedrock: {e}"


if __name__ == "__main__":
  # Example usage
  prompt = "What is the capital of France"
  response = AwsClient().get_bedrock_response(prompt)
  print(response)
