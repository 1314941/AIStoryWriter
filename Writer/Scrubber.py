import Writer.Logger
import Writer.Prompts

# scrub novel 翻译为 剪辑小说，即对小说进行编辑和修改
def ScrubNovel(Interface, _Logger, _Chapters: list, _TotalChapters: int):

    # 定义一个变量，用于存储编辑后的章节
    EditedChapters = _Chapters

    # 遍历所有章节
    for i in range(len(_Chapters)):

        # 定义一个变量，用于存储提示信息
        Prompt: str = Writer.Prompts.CHAPTER_SCRUB_PROMPT.format(
            _Chapter=EditedChapters[i]
        )
        # 记录日志，提示LLM开始进行章节编辑
        _Logger.Log(f"Prompting LLM To Perform Chapter {i+1} Scrubbing Edit", 5)
        # 定义一个空列表，用于存储消息
        Messages = []
        # 将提示信息添加到消息列表中
        Messages.append(Interface.BuildUserQuery(Prompt))
        # 使用安全生成文本的方法，生成编辑后的章节
        Messages = Interface.SafeGenerateText(
            _Logger, Messages, Writer.Config.SCRUB_MODEL
        )
        # 记录日志，提示LLM完成章节编辑
        _Logger.Log(f"Finished Chapter {i+1} Scrubbing Edit", 5)

        # 获取编辑后的章节内容
        NewChapter = Interface.GetLastMessageText(Messages)
        # 将编辑后的章节内容替换原来的章节内容
        EditedChapters[i] = NewChapter
        # 计算编辑后的章节字数
        ChapterWordCount = Writer.Statistics.GetWordCount(NewChapter)
        # 记录日志，提示编辑后的章节字数
        _Logger.Log(f"Scrubbed Chapter Word Count: {ChapterWordCount}", 3)

    # 返回编辑后的章节列表
    return EditedChapters
