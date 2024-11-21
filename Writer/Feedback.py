import Writer.Logger
import Writer.Prompts

import json



# 定义一个函数，用于获取对大纲的反馈
def GetFeedbackOnOutline(Interface, _Logger, _Outline: str):

    # 创建一个空列表，用于存储历史记录
    History = []
    # 将系统查询添加到历史记录中
    History.append(Interface.BuildSystemQuery(Writer.Prompts.CRITIC_OUTLINE_INTRO))

    # 格式化提示，将大纲作为参数传入
    StartingPrompt: str = Writer.Prompts.CRITIC_OUTLINE_PROMPT.format(_Outline=_Outline)

    # 记录日志，提示正在请求LLM对大纲进行评价
    _Logger.Log("Prompting LLM To Critique Outline", 5)
    # 将用户查询添加到历史记录中
    History.append(Interface.BuildUserQuery(StartingPrompt))
    # 使用安全生成文本的方法，生成大纲的反馈
    History = Interface.SafeGenerateText(
        _Logger, History, Writer.Config.REVISION_MODEL, _MinWordCount=44
    )
    # 记录日志，提示已经获取到大纲的反馈
    _Logger.Log("Finished Getting Outline Feedback", 5)

    # 返回最后一条消息的文本
    return Interface.GetLastMessageText(History)


def GetOutlineRating(
    Interface,
    _Logger,
    _Outline: str,
):

  
    # 初始化历史记录列表
    History = []
    # 将系统查询添加到历史记录中
    History.append(Interface.BuildSystemQuery(Writer.Prompts.OUTLINE_COMPLETE_INTRO))

    # 格式化起始提示
    StartingPrompt: str = Writer.Prompts.OUTLINE_COMPLETE_PROMPT.format(
        _Outline=_Outline
    )

    # 记录开始获取评审JSON
    _Logger.Log("Prompting LLM To Get Review JSON", 5)

    # 将用户查询添加到历史记录中
    History.append(Interface.BuildUserQuery(StartingPrompt))
    # 使用安全生成文本方法获取评审JSON
    History = Interface.SafeGenerateText(
        _Logger, History, Writer.Config.EVAL_MODEL, _Format="json"
    )
    # 记录完成获取评审JSON
    _Logger.Log("Finished Getting Review JSON", 5)

    # 初始化迭代次数
    Iters: int = 0
    # 无限循环
    while True:

        # 获取最后一条消息的文本
        RawResponse = Interface.GetLastMessageText(History)
        # 替换文本中的反引号和json关键字
        RawResponse = RawResponse.replace("`", "")
        RawResponse = RawResponse.replace("json", "")

        try:
            # 增加迭代次数
            Iters += 1
            # 解析JSON，获取IsComplete字段
            Rating = json.loads(RawResponse)["IsComplete"]
            # 记录编辑器确定的IsComplete值
            _Logger.Log(f"Editor Determined IsComplete: {Rating}", 5)
            # 返回IsComplete值
            return Rating
        except Exception as E:
            # 如果迭代次数超过4次，记录错误并返回False
            if Iters > 4:
                _Logger.Log("Critical Error Parsing JSON", 7)
                return False
            # 记录解析JSON错误，并要求编辑器进行修改
            _Logger.Log("Error Parsing JSON Written By LLM, Asking For Edits", 7)
            # 格式化编辑提示
            EditPrompt: str = Writer.Prompts.JSON_PARSE_ERROR.format(_Error=E)
            # 将编辑提示添加到历史记录中
            History.append(Interface.BuildUserQuery(EditPrompt))
            # 记录要求编辑器进行修改
            _Logger.Log("Asking LLM TO Revise", 7)
            # 使用安全生成文本方法获取修改后的JSON
            History = Interface.SafeGenerateText(
                _Logger, History, Writer.Config.EVAL_MODEL, _Format="json"
            )
            _Logger.Log("Done Asking LLM TO Revise JSON", 6)


# 定义一个函数，用于获取对章节的反馈
def GetFeedbackOnChapter(Interface, _Logger, _Chapter: str, _Outline: str):

    # 创建一个空列表，用于存储历史记录
    History = []
    # 将构建的系统查询添加到历史记录中
    History.append(
        Interface.BuildSystemQuery(
            Writer.Prompts.CRITIC_CHAPTER_INTRO.format(_Chapter=_Chapter)
        )
    )

    # 构建起始提示
    StartingPrompt: str = Writer.Prompts.CRITIC_CHAPTER_PROMPT.format(
        _Chapter=_Chapter, _Outline=_Outline
    )

    # 记录日志，提示LLM正在对章节进行评价
    _Logger.Log("Prompting LLM To Critique Chapter", 5)
    # 将起始提示添加到历史记录中
    History.append(Interface.BuildUserQuery(StartingPrompt))
    # 使用安全生成文本方法，生成文本
    Messages = Interface.SafeGenerateText(
        _Logger, History, Writer.Config.REVISION_MODEL
    )
    # 记录日志，完成获取章节反馈
    _Logger.Log("Finished Getting Chapter Feedback", 5)

    # 返回最后一条消息的文本
    return Interface.GetLastMessageText(Messages)


# Switch this to iscomplete true/false (similar to outline)
def GetChapterRating(Interface, _Logger, _Chapter: str):

    # 初始化历史记录列表
    History = []
    # 将构建的系统查询添加到历史记录列表中
    History.append(Interface.BuildSystemQuery(Writer.Prompts.CHAPTER_COMPLETE_INTRO))

    # 格式化提示，将章节名称插入提示中
    StartingPrompt: str = Writer.Prompts.CHAPTER_COMPLETE_PROMPT.format(
        _Chapter=_Chapter
    )

    # 记录日志，提示LLM获取评论JSON
    _Logger.Log("Prompting LLM To Get Review JSON", 5)
    # 将用户查询添加到历史记录列表中
    History.append(Interface.BuildUserQuery(StartingPrompt))
    # 使用安全生成文本方法生成文本
    History = Interface.SafeGenerateText(
        _Logger, History, Writer.Config.EVAL_MODEL
    )
    # 记录日志，完成获取评论JSON
    _Logger.Log("Finished Getting Review JSON", 5)

    # 初始化迭代次数
    Iters: int = 0
    # 无限循环
    while True:

        # 获取历史记录列表中的最后一条消息文本
        RawResponse = Interface.GetLastMessageText(History)
        # 将反引号和json字符串替换为空字符串
        RawResponse = RawResponse.replace("`", "")
        RawResponse = RawResponse.replace("json", "")

        try:
            # 每次迭代增加一次
            Iters += 1
            # 将JSON字符串转换为Python对象，并获取IsComplete属性
            Rating = json.loads(RawResponse)["IsComplete"]
            # 记录日志，编辑器确定IsComplete属性
            _Logger.Log(f"Editor Determined IsComplete: {Rating}", 5)
            # 返回IsComplete属性
            return Rating
        except Exception as E:
            # 如果迭代次数超过4次，记录日志，解析JSON出错
            if Iters > 4:
                _Logger.Log("Critical Error Parsing JSON", 7)
                # 返回False
                return False

            # 记录日志，解析JSON出错，要求LLM进行编辑
            _Logger.Log("Error Parsing JSON Written By LLM, Asking For Edits", 7)
            # 格式化编辑提示，将错误信息插入提示中
            EditPrompt: str = Writer.Prompts.JSON_PARSE_ERROR.format(_Error=E)
            # 将编辑提示添加到历史记录列表中
            History.append(Interface.BuildUserQuery(EditPrompt))
            # 记录日志，要求LLM进行编辑
            _Logger.Log("Asking LLM TO Revise", 7)
            # 使用安全生成文本方法生成文本
            History = Interface.SafeGenerateText(
                _Logger, History, Writer.Config.EVAL_MODEL
            )
            # 记录日志，完成要求LLM进行编辑
            _Logger.Log("Done Asking LLM TO Revise JSON", 6)
