<<<<<<< HEAD
import Writer.Logger
=======
import Writer.PrintUtils
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
import Writer.Config
import Writer.Prompts


def EditNovel(Interface, _Logger, _Chapters: list, _Outline: str, _TotalChapters: int):

<<<<<<< HEAD
    # 定义一个变量EditedChapters，用于存储编辑后的章节列表
    EditedChapters = _Chapters

    # 遍历所有章节
    for i in range(0, len(_Chapters)-1):

        # 定义一个变量NovelText，用于存储所有章节的文本
=======
    EditedChapters = _Chapters

    for i in range(1, _TotalChapters + 1):

>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
        NovelText: str = ""
        for Chapter in EditedChapters:
            NovelText += Chapter

<<<<<<< HEAD
        # 定义一个变量Prompt，用于存储编辑章节的提示
=======
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
        Prompt: str = Writer.Prompts.CHAPTER_EDIT_PROMPT.format(
            _Chapter=EditedChapters[i], NovelText=NovelText, i=i
        )

<<<<<<< HEAD
        # 记录开始编辑章节的日志
=======
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
        _Logger.Log(
            f"Prompting LLM To Perform Chapter {i} Second Pass In-Place Edit", 5
        )
        Messages = []
        Messages.append(Interface.BuildUserQuery(Prompt))
        Messages = Interface.SafeGenerateText(
            _Logger, Messages, Writer.Config.CHAPTER_WRITER_MODEL
        )
<<<<<<< HEAD
        # 记录结束编辑章节的日志
        _Logger.Log(f"Finished Chapter {i} Second Pass In-Place Edit", 5)

        # 获取编辑后的章节文本
        NewChapter = Interface.GetLastMessageText(Messages)
        # 将编辑后的章节文本替换原来的章节文本
        EditedChapters[i] = NewChapter
        # 计算编辑后的章节的单词数
        ChapterWordCount = Writer.Statistics.GetWordCount(NewChapter)
        # 记录编辑后的章节的单词数
        _Logger.Log(f"New Chapter Word Count: {ChapterWordCount}", 3)

    # 返回编辑后的章节列表
=======
        _Logger.Log(f"Finished Chapter {i} Second Pass In-Place Edit", 5)

        NewChapter = Interface.GetLastMessageText(Messages)
        EditedChapters[i] = NewChapter
        ChapterWordCount = Writer.Statistics.GetWordCount(NewChapter)
        _Logger.Log(f"New Chapter Word Count: {ChapterWordCount}", 3)

>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
    return EditedChapters
