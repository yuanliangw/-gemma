TEXT_EVAL_GENERAL_PROMPT_PATTERN = """
[Task Description] 
Here is a task called question-answering. All [Input] are in {{Language}}.
{{MORE_TASK_DEFINITION}}
I will provide a background material and a question. Please write the answer to the question based on the background material, along with a justification. The justification should be reasonable and logically clear, the answer should be concise, and it should be specific to the question.
Your evaluation should follow the [Criteria] and  [Guidance]. 
The output format should follow the [Output Format].

[Guidance]
You should strictly follow my guidance:
1. Your answer to the question should be based on the background material, along with a justification. The justification should be reasonable and logically clear, the answer should be concise, and it should be specific to the question.
2. You should strictly follow the given output format and can't output other information.
{{MORE_GUIDANCE}}
If you break my guidance, you will be penalized.

[Criteria]
{{Criteria}}

{{In-Context Examples}}

[Output Format]
Your output should strictly follow this format and can be directly decoded by Python:
'''
{{Output}}
'''

[Input]
'''
{
    "background materials": {{BACKGROUND MATERIALS}},
    "question": {{QUESTION}}
}
'''

"""