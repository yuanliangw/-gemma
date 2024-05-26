# -gemma
自然语言处理第一次实验
# 项目背景

本项目旨在使用大语言模型（`gemma:2b`）实现知识挖掘和问答功能。具体任务包括根据给定的背景材料和问题生成对应的答案及其理由。

# 安装

在开始使用本项目之前，请确保你已安装了以下依赖项：

 Python 3.7+
 `ollama` 库

你可以使用以下命令来安装所需的库：

```bash
pip install ollama
使用说明
本地模型部署
git clone https://github.com/yuanliangw/-gemma
初始化并运行模型：
from model import ChatModel

# 创建模型实例
chat_model = ChatModel()

# 列出可用模型
chat_model.list()

# 显示模型信息
chat_model.show()
生成答案
以下是生成答案和理由的示例代码：
background = "一家知名电子产品公司发布了一款新型智能手表，该手表配备了多项健康监测功能，包括心率监测、睡眠监测、运动追踪等，并且能够自动识别用户的活动状态和健康异常。"
question = "你认为这款智能手表对用户的健康管理是否有重要意义？"

# 生成答案和理由
answer = chat_model.generate_answer(background, question)
print(answer)
清空上下文
你可以随时清空上下文：
chat_model.clear_context()
测试示例
在 model.py 中，我们提供了几个测试函数来验证模型的功能
测试生成答案和理由：
def test1():
    chat_model = ChatModel()
    background = "一家知名电子产品公司发布了一款新型智能手表，该手表配备了多项健康监测功能，包括心率监测、睡眠监测、运动追踪等，并且能够自动识别用户的活动状态和健康异常。"
    question = "你认为这款智能手表对用户的健康管理是否有重要意义？"
    answer = chat_model.generate_answer(background, question)
    print(answer)
test1()
从用户输入中提取背景和问题：
def test2():
    chat_model = ChatModel()
    user_input = input("请输入背景和问题：")
    answer = chat_model.generate_answer_input(user_input)
    print(answer)
test2()
前端界面
我们还实现了一个简单的前端演示界面。请确保已安装 Flask 等必要的依赖项。启动前端界面：
cd web
python app.py
启动后，打开浏览器并访问 http://localhost:5000 以查看前端演示界面。

