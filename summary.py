import openai


def get_ai_response(question, doc, prompt, summary):
    global prompt_template
    prompt_template = prompt_template.format(document_data=doc, summary=summary)
    prompt = [{}]
    prompt[0] = {"role": "system", "content": prompt_template}

    # Add the question the user question
    prompt.append({"role": "user", "content": question})
    prompt.append(
        {
            "role": "system",
            "content": """create a summary for whole conversation and write it format 
                    The format for summary is given as following:
    #               <summary>Your generated summary here<summary>
         """,
        }
    )
    # prompt.append({
    #      'role' : 'system',
    #      'content' : """
    #             Also summarize the input message and ai response with the previously provided summary keeping all important point and information,
    #         keeping the summary in 4 to 5 lines.

    #         The format for summary is given as following:
    #         <summary>Your generated summary here<summary>
    #         """

    # })
    response = []
    result = ""
    # Ask the question and stream the response
    for chunk in openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k", messages=prompt, stream=True
    ):
        text = chunk.choices[0].get("delta", {}).get("content")
        if text is not None:

            response.append(text)

    result = "".join(response).strip()
    print("result --")
    # When we get an answer back we add that to the message history
    prompt.append({"role": "assistant", "content": result})

    return result
