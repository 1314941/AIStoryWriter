# 改动
## 一.汉化
1.将提示词通过ai辅助汉化。方便调整
2.输出的log和ai返回的内容也变成中文。
>将翻译指令里的目标语言改为汉语(ctrl+f 查找"en"或"英语'')
>提示词汉化后使得ai也返回相同语言

## 二.重连
意外中断后，再次启动时可通过读取记录文件，继续之前的进度。
>1大纲
>2章节细纲
>3章节
>4清洗章节
>5总结
```
{
    "step": 1,
    "done_chapter_outlines": 0,
    "done_chapters": 0,
    "chapter_num": 6
}
```

Logs 里面的文件即为记录文件。
record.json里面记录了已经完成的章节细纲和章节数。
step   进行到哪一步
chapter_num 总章节数
## 三.模型的改动
电脑撑不起原项目的llama3:70b。然后本人又懒得去配其他的模型。直接全部改用了ollama的qwen2.5。
但通过modelfile调整了一下。(有个小毛病,用vscode的ctrl+/ 注释键出来的注释符";"无效，需要手动敲#)
```
#modelfile

#rwkv6模型不能使用   Error: llama runner process has terminated: GGML_ASSERT(inp != nullptr && "missing result_norm/result_embd tensor") failed
FROM qwen2.5:latest

# 设置温度为 1 [越高越有创造力，越低越连贯]
PARAMETER temperature 1
# 设置上下文窗口大小为 4096，这控制了 LLM 可以用来生成下一个标记的标记数量
PARAMETER num_ctx 4096

# 设置一个自定义的系统消息来指定小说作家的行为
#使用介绍
#   ollama create example -f modelfile
#   ollama run example


#SYSTEM 根据输出的网络小说情节,生成符合小说情节的人物卡片,人物卡片记录着不同角色的性格,外貌和经历,并提供一些提示信息。
#SYSTEM 根据输出的网络小说人物卡片,生成符合小说情节的大纲,包含主要人物的故事线,主要事件,注意要符合给定角色的性格,外貌和经历。
#SYSTEM 根据输入的小说大纲和上一章内容,生成下一章细纲,并写出下一章的标题,主题,情节走向,爽点,伏笔。每张字数在1500-3000字之间,要预留出一些字数给细节描写。
#SYSTEM 根据输入的章节细纲,写出下一章,字数在1500-3000字之间,并保持情节的连贯性和逻辑性。同时，请适当在小说中描写环境、人物表情和动作，以增加故事的生动性和吸引力，让读者更容易沉浸其中。

SYSTEM 你是一个杰出的作家,能灵活地根据输入的请求,输出符合小说情节的大纲,人物卡片,章节细纲,章节内容。


TEMPLATE """{{ if .System }}<|im_start|>system
{{ .System }}<|im_end|>
{{ end }}{{ if .Prompt }}<|im_start|>user
{{ .Prompt }}<|im_end|>
{{ end }}<|im_start|>assistant
"""

```
## 尝试 添加示例
在对话中插入示例。
从template中读取对应文件夹，并读取txt文件,获得示例。
目前只在部分需要ai返回json的地方实现,因为总是返回读取不成功的信息。
>总在前面加上```json
>不够规范，导致识别到过多场景，又耗时效果又不好
 
> 原项目处理方式：对ai返回的信息删去"``"和"json"
> 或许还可以只取第一个"["和最后一个"]"之间的内容
 
 
# todo
重连粒度不够细。4清洗章节这一步也相当耗时
模型参数不够大，出来的效果没有原项目的好。可能需要在输入的信息里加上示例(done)。



# AI Story Generator 📚✨

Generate full-length novels with AI! Harness the power of large language models to create engaging stories based on your prompts.

[![Discord](https://img.shields.io/discord/1255847829763784754?color=7289DA&label=Discord&logo=discord&logoColor=white)](https://discord.gg/R2SySWDr2s)

## 🚀 Features

- Generate medium to full-length novels: Produce substantial stories with coherent narratives, suitable for novella or novel-length works.
- Easy setup and use: Get started quickly with minimal configuration required.
- Customizable prompts and models: Choose from existing prompts or create your own, and select from various language models.
- Automatic model downloading: The system can automatically download required models via Ollama if they aren't already available.
- Support for local models via Ollama: Run language models locally for full control and privacy.
- Cloud provider support (currently Google): Access high-performance computing resources for those without powerful GPUs.
- Flexible configuration options: Fine-tune the generation process through easily modifiable settings.
- Works across all operating systems
- Supoorts translation of the generated stories in all languages

## 🏁 Quick Start

Getting started with AI Story Generator is easy:

1. Clone the repository
2. Install [Ollama](https://ollama.com/) for local model support
3. Run the generator:

```sh
./Write.py -Prompt Prompts/YourChosenPrompt.txt
```

That's it! The system will automatically download any required models and start generating your story.

**Optional steps:**

- Modify prompts in `Writer/Prompts.py` or create your own
- Configure the model selection in `Writer/Config.py`

## 💻 Hardware Recommendations

Not sure which models to use with your GPU? Check out our [Model Recommendations](Docs/Models.md) page for suggestions based on different GPU capabilities. We provide a quick reference table to help you choose the right models for your hardware, ensuring optimal performance and quality for your story generation projects.

## 🛠️ Usage

You can customize the models used for different parts of the story generation process in two ways:

### 1. Using Command-Line Arguments (Recommended)

You can override the default models by specifying them as command-line arguments:

```sh
./Write.py -Prompt Prompts/YourChosenPrompt.txt -InitialOutlineModel "ollama://llama3:70b" ...
```

Available command-line arguments are stated in the `Write.py` file.

The model format is: `{ModelProvider}://{ModelName}@{ModelHost}?parameter=value`

- Default host is `127.0.0.1:11434` (currently only affects ollama)
- Default ModelProvider is `ollama`
- Supported providers: `ollama`, `google`, `openrouter`
- For `ollama` we support the passing of parameters (e.g. `temperature`) on a per model basis

Example:
```sh
./Write.py -Prompt Prompts/YourChosenPrompt.txt -InitialOutlineModel "google://gemini-1.5-pro" -ChapterOutlineModel "ollama://llama3:70b@192.168.1.100:11434" ...
```

This flexibility allows you to experiment with different models for various parts of the story generation process, helping you find the optimal combination for your needs.


NOTE: If you're using a provider that needs an API key, please copy `.env.example` to `.env` and paste in your API keys there.


### 2. Using Writer/Config.py


Edit the `Writer/Config.py` file to change the default models:

```python
INITIAL_OUTLINE_WRITER_MODEL = "ollama://llama3:70b"
CHAPTER_OUTLINE_WRITER_MODEL = "ollama://gemma2:27b"
CHAPTER_WRITER_MODEL = "google://gemini-1.5-flash"
...
```

## 🧰 Architecture Overview

![Block Diagram](Docs/BlockDiagram.drawio.svg)

## 🛠️ Customization

- Experiment with different local models via Ollama: Try out various language models to find the best fit for your storytelling needs.
- Test various model combinations for different story components: Mix and match models for outline generation, chapter writing, and revisions to optimize output quality.

## 💪 What's Working Well

- Generating decent-length stories: The system consistently produces narratives of substantial length, suitable for novella or novel-length works.
- Character consistency: AI models maintain coherent character traits and development throughout the generated stories.
- Interesting story outlines: The initial outline generation creates compelling story structures that serve as strong foundations for the full narratives.

## 🔧 Areas for Improvement

- Reducing repetitive phrases: We're working on enhancing the language variety to create more natural-sounding prose.
- Improving chapter flow and connections: Efforts are ongoing to create smoother transitions between chapters and maintain narrative cohesion.
- Addressing pacing issues: Refinements are being made to ensure proper story pacing and focus on crucial plot points.
- Optimizing generation speed: We're continuously working on improving performance to reduce generation times without sacrificing quality.

## 🤝 Contributing

We're excited to hear from you! Your feedback and contributions are crucial to improving the AI Story Generator. Here's how you can get involved:

1. 🐛 **Open Issues**: Encountered a bug or have a feature request? [Open an issue](https://github.com/datacrystals/AIStoryWriter/issues) and let us know!

2. 💡 **Start Discussions**: Have ideas or want to brainstorm? [Start a discussion](https://github.com/datacrystals/AIStoryWriter/discussions) in our GitHub Discussions forum.

3. 🔬 **Experiment and Share**: Try different model combinations and share your results. Your experiments can help improve the system for everyone!

4. 🖊️ **Submit Pull Requests**: Ready to contribute code? We welcome pull requests for improvements and new features.

5. 💬 **Join our Discord**: For real-time chat, support, and community engagement, [join our Discord server](https://discord.gg/R2SySWDr2s).

Don't hesitate to reach out – your input is valuable, and we're here to help!

## 📄 License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). This means that if you modify the code and use it to provide a service over a network, you must make your modified source code available to the users of that service. For more details, see the [LICENSE](LICENSE) file in the repository or visit [https://www.gnu.org/licenses/agpl-3.0.en.html](https://www.gnu.org/licenses/agpl-3.0.en.html).

---

Join us in shaping the future of AI-assisted storytelling! 🖋️🤖
