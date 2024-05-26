# -*- coding: utf-8 -*-
import argparse
import json
from scoring_prompts import TEXT_EVAL_GENERAL_PROMPT_PATTERN
from tmp_utils import set_logger
from llms.remote.ChatGPT import ChatGPTLLM,RemoteLLMs

class ScoringAgent:
    def __init__(self, logger, llm_model: RemoteLLMs, metrics: dict,
                 language, in_context_examples=[],
                 more_guidance=[], more_task_definition=[]):

        self.logger = logger
        self.llm_model = llm_model
        self.prompt_pattern = TEXT_EVAL_GENERAL_PROMPT_PATTERN
        self.result_pattern = metrics

        # 处理额外的输入
        more_task_definition = '\n'.join(more_task_definition)

        # 评价的指标
        metric_dict = dict()
        data_type=None
        for metric, score_format in metrics.items():
            metric_dict[metric] = "[Your result]"
            items = score_format.split('_')

            if data_type is None:
                data_type = items[0]

            else:
                assert data_type == items[0]


        output_pattern = json.dumps(metric_dict, ensure_ascii=False, indent=4)

        # In-Context Examples 的设置
        if len(in_context_examples) > 0:
            more_guidance.append('To help your judgment, some examples are provided in [Examples].')
            in_context_prompt = ["[Examples]", "'''"]
            in_context_prompt.append(json.dumps(in_context_examples, ensure_ascii=False, indent=4))
            in_context_prompt.append("'''")
            in_context_prompt = '\n'.join(in_context_prompt)
        else:
            in_context_prompt = ""

        # 是否有更多需要补充的指南
        tmp = []
        for idx, guidance in enumerate(more_guidance):
            tmp.append('%s. %s' % (idx + 3, guidance))
        more_guidance = '\n'.join(tmp)

        # 根据评价指标设置评价的标准
        input_format = {}
        criteria = []

        criteria = '\n'.join(criteria)

        # 给定输入的模板格式
        input_format = json.dumps(input_format, ensure_ascii=False, indent=4)

        self.meta_dict = {
            "{{Language}}": language,
            "{{Output}}": output_pattern,
            "{{Input}}": input_format,
            "{{Criteria}}": criteria,
            "{{MORE_GUIDANCE}}": more_guidance,
            "{{MORE_TASK_DEFINITION}}": more_task_definition,
            "{{In-Context Examples}}": in_context_prompt
        }

    def judge_a_case(self, case_data):
        llm_model = self.llm_model
        repeat_times = -1

        while True:
            repeat_times += 1
            if repeat_times >= llm_model.max_retries:
                break
            # 首先构造prompt
            prompt = llm_model.fit_case(pattern=self.prompt_pattern, data=case_data, meta_dict=self.meta_dict)
            contexts = llm_model.create_prompt(prompt)
            results = llm_model.request_llm(contexts, repeat_times=repeat_times)

            return prompt, results[-1]

        return None




if __name__ == '__main__':
    # https://platform.openai.com/docs/api-reference

    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path", type=str,  default="../remote/configs/wsx_gpt35.json")
    args = parser.parse_args()

    # 定义一个Logger
    logger = set_logger("tmp.log")

    # 定义一个Agent
    chat_gpt = ChatGPTLLM(args.config_path)

    # 定义参数

    language = "Chinese"

    result_pattern = {
        "Answer": "str",
        "Reason": "str",
    }

    more_guidance = ['Each score should have two digits.']

    in_context_examples = [
        {
            "Input": {
                "Background materials": "春节，即农历新年，是一年之岁首、传统意义上的年节。俗称新春、新年、新岁、岁旦、年禧、大年等，口头上又称度岁、庆岁、过年、过大年。春节历史悠久，由上古时代岁首祈岁祭祀演变而来。万物本乎天、人本乎祖，祈岁祭祀、敬天法祖，报本反始也。春节的起源蕴含着深邃的文化内涵，在传承发展中承载了丰厚的历史文化底蕴。在春节期间，全国各地均有举行各种庆贺新春活动，带有浓郁的各地域特色。这些活动以除旧布新、驱邪攘灾、拜神祭祖、纳福祈年为主要内容，形式丰富多彩，凝聚着中华传统文化精华。",
                "question": "春节是中国的传统节日吗？",
            },
            "Output": {
                "Answer": "是",
                "Reason": "因为春节由上古时代岁首祈岁祭祀演变而来， 是中华民族最隆重的传统佳节。",
            }
        }
    ]

    score_agent = ScoringAgent(logger, chat_gpt,metrics=result_pattern,
                               language=language, more_guidance=more_guidance, in_context_examples=in_context_examples)
    data = {
        "{{BACKGROUND MATERIALS}}": "一家知名电子产品公司发布了一款新型智能手表，该手表配备了多项健康监测功能，包括心率监测、睡眠监测、运动追踪等，并且能够自动识别用户的活动状态和健康异常。",
        "{{QUESTION}}": "你认为这款智能手表对用户的健康管理是否有重要意义？",
    }
    prompt, res = score_agent.judge_a_case(data)
    print("本次请求的Prompt是", prompt)
    print("本次请求的结果是", res)
