import Writer.Feedback
import Writer.Logger
import Writer.Config
import Writer.Chapter.ChapterGenSummaryCheck
import Writer.Prompts


def ChapterOutlineToScenes(Interface, _Logger, _ThisChapter:str, _Outline:str, _BaseContext: str = ""):


    # 记录日志，开始将章节拆分为场景
    # _Logger.Log(f"Splitting Chapter Into Scenes", 2)
    #中文
    _Logger.Log(f"将章节拆分为场景", 2)
    # 创建一个空列表，用于存储消息历史
    MesssageHistory: list = []
    # 将默认的系统提示添加到消息历史中
    MesssageHistory.append(Interface.BuildSystemQuery(Writer.Prompts.DEFAULT_SYSTEM_PROMPT))
    # 将用户提示添加到消息历史中，提示用户将章节拆分为场景
    MesssageHistory.append(Interface.BuildUserQuery(Writer.Prompts.CHAPTER_TO_SCENES.format(_ThisChapter=_ThisChapter, _Outline=_Outline)))

    # 使用指定的模型和最小字数生成文本
    Response = Interface.SafeGenerateText(_Logger, MesssageHistory, Writer.Config.CHAPTER_OUTLINE_WRITER_MODEL, _MinWordCount=100)
    # 记录日志，完成将章节拆分为场景
    _Logger.Log(f"完成将章节拆分为场景", 5)

    # 返回生成的文本
    return Interface.GetLastMessageText(Response)
