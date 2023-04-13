import openai

class OpenAi():
    
    def gpt_completion_response(prompt, completion_config, model="text-ada-001"):
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            temperature=completion_config["temperature"],
            max_tokens=completion_config["max_tokens"],
            top_p=completion_config["top_p"],
            frequency_penalty=completion_config["frequency_penalty"],
            presence_penalty=completion_config["presence_penalty"]
        )
        return response

    def gpt_embeddings_response(input, model="text-embedding-ada-002"):
        response = openai.Embedding.create(
            model=model,
            input=input,
        )
        embeddings = response['data'][0]['embedding']
        return embeddings