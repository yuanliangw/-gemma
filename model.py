import ollama


class ChatModel:
    def __init__(self, model_name='gemma:2b'):
        self.model_name = model_name
        self.context = []

    def generate(self, prompt):
        c = ollama.generate(model=self.model_name, prompt=prompt)
        # print(c)
        return c

    def chat(self, user_inputs):
        """
        使用 Ollama 模型进行对话

        Args:
        - user_inputs (list of str): 用户输入的文本列表


        Returns:
        - list of str: 模型生成的回复列表
        """
        try:
            # 构造用户输入的消息列表，加上之前的上下文
            messages = [{'role': 'user', 'content': input_text} for input_text in user_inputs]
            responses = []
            for message in messages:
                self.context.append(message)
                response = ollama.chat(model=self.model_name, messages=self.context)
                self.context.append(response['message'])
                print(response['message']['content'])
                responses.append(response['message']['content'])
            # 提取模型生成的回复内容并返回
            return responses
        except Exception as e:
            # 如果出现异常，返回错误消息
            return [str(e) for _ in user_inputs]

    def new_chat(self, user_inputs):
        self.clear_context()
        self.chat(user_inputs=user_inputs)

    def print_context(self):
        print('打印上下文')
        for conversation in self.context:
            print(f'{conversation["role"]}: {conversation["content"]}')

    def clear_context(self):
        """
        清空上下文
        """
        self.context = []

    def list(self):
        l = ollama.list()
        print(l)
        return l

    def show(self):
        s = ollama.show(self.model_name)
        print(s)
        return s

    def embeddings(self, prompt):
        e = ollama.embeddings(model='gemma:2b', prompt=prompt)
        print(e)
        return e

    def generate_answer(self, background, question, language=1):

        """
        根据背景材料和问题生成答案以及理由。

         Args:
        - background (str): 背景材料
        - question (str): 问题
        - language (str): 语言选择，0或1

        Returns:
        - tuple: 包含答案和理由的元组
        """
        require = "请分别给出答案和理由"

        require_en = "fuck u"

        if language == 1:
            prompt = f"背景：{background} 问题：{question} {require}"
        else:
            prompt = f"Background: {background} Question: {question} {require_en} "
        # if language == 1:
        #     prompt = f"背景：{background} 问题：{question} 理由："
        # else:
        #     prompt = f"Background: {background} Question: {question} Reason: "
        response = self.generate(prompt)
        # return response.get("Answer", None), response.get("Reason", None)
        response_content = response.get('response')
        return response_content

    def generate_answer_input(self, input_text, language=1):
        """
                根据用户输入生成答案。

                 Args:
                - input_text (str): 用户输入的文本，包含背景和问题

                Returns:
                - str: 模型生成的回复
                """
        # 从用户输入中提取背景和问题
        background, question = input_text.split(' ', 1)

        require = "请分别给出答案和理由"

        require_en = "fuck u"

        if language == 1:
            prompt = f"背景：{background} 问题：{question} {require}"
        else:
            prompt = f"Background: {background} Question: {question} {require_en} "
        response = self.generate(prompt)
        response_content = response.get('response')
        return response_content


def test1():

    chat_model = ChatModel()
    # 测试生成答案和理由
    background = "一家知名电子产品公司发布了一款新型智能手表，该手表配备了多项健康监测功能，包括心率监测、睡眠监测、运动追踪等，并且能够自动识别用户的活动状态和健康异常。"
    question = "你认为这款智能手表对用户的健康管理是否有重要意义？"

    # answer, reason = chat_model.generate_answer(background, question)
    # print(answer)
    # print(reason)
    answer = chat_model.generate_answer(background, question)
    print(answer)


def test2():
    chat_model = ChatModel()
    # 测试生成答案和理由
    # background = "一家新型电动汽车公司宣布推出一款新型电动汽车，该车型拥有比传统燃油车更长的续航里程，更快的充电速度，并且售价相对较低。"
    # question = "你认为这款新型电动汽车对汽车市场和环境有影响吗？"
    # chat_model.generate_answer(background, question)

    # 从用户输入中提取背景和问题
    user_input = input("请输入背景和问题：")
    # 调用生成答案的方法
    answer = chat_model.generate_answer_input(user_input)
    print(answer)
def test3():
    chat_model = ChatModel()
    background = "一项新的研究指出，城市绿化水平与居民幸福感之间存在着正相关关系，即城市中绿化程度越高，居民的幸福感越高。"
    question = "你认为提高城市绿化水平对城市发展是否有益处？"
    chat_model.generate_answer(background, question)


test1()
# test2()
# test3()

