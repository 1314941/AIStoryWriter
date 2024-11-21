<<<<<<< HEAD
import Writer.Feedback
import Writer.Logger
=======
import Writer.LLMEditor
import Writer.PrintUtils
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
import Writer.Config
import Writer.Outline.StoryElements
import Writer.Prompts


<<<<<<< HEAD
# 我们应该可能将大纲生成分为多个阶段，以便我们可以回过头来向之前的段落添加预示等元素
=======
# We should probably do outline generation in stages, allowing us to go back and add foreshadowing, etc back to previous segments
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16


def GenerateOutline(Interface, _Logger, _OutlinePrompt, _QualityThreshold: int = 85):

<<<<<<< HEAD
    # 生成提示
=======
    # Get any important info about the base prompt to pass along
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
    Prompt: str = Writer.Prompts.GET_IMPORTANT_BASE_PROMPT_INFO.format(
        _Prompt = _OutlinePrompt
    )


<<<<<<< HEAD
    # 提取重要基础上下文
    _Logger.Log(f"提取重要基础上下文", 4)
=======
    _Logger.Log(f"Extracting Important Base Context", 4)
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
    Messages = [Interface.BuildUserQuery(Prompt)]
    Messages = Interface.SafeGenerateText(
        _Logger, Messages, Writer.Config.INITIAL_OUTLINE_WRITER_MODEL
    )
    BaseContext: str = Interface.GetLastMessageText(Messages)
<<<<<<< HEAD
    _Logger.Log(f"完成提取重要基础上下文", 4)


    # 生成故事元素
=======
    _Logger.Log(f"Done Extracting Important Base Context", 4)


    # Generate Story Elements
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
    StoryElements: str = Writer.Outline.StoryElements.GenerateStoryElements(
        Interface, _Logger, _OutlinePrompt
    )


<<<<<<< HEAD
    # 生成初始大纲
=======
    # Now, Generate Initial Outline
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
    Prompt: str = Writer.Prompts.INITIAL_OUTLINE_PROMPT.format(
        StoryElements=StoryElements, _OutlinePrompt=_OutlinePrompt
    )


<<<<<<< HEAD
    _Logger.Log(f"生成初始大纲", 4)
    Messages = [Interface.BuildUserQuery(Prompt)]
    Messages = Interface.SafeGenerateText(
        _Logger, Messages, Writer.Config.INITIAL_OUTLINE_WRITER_MODEL, _MinWordCount=150
    )
    Outline: str = Interface.GetLastMessageText(Messages)
    _Logger.Log(f"完成生成初始大纲", 4)

    _Logger.Log(f"进入反馈/修订循环", 3)
=======
    _Logger.Log(f"Generating Initial Outline", 4)
    Messages = [Interface.BuildUserQuery(Prompt)]
    Messages = Interface.SafeGenerateText(
        _Logger, Messages, Writer.Config.INITIAL_OUTLINE_WRITER_MODEL, _MinWordCount=250
    )
    Outline: str = Interface.GetLastMessageText(Messages)
    _Logger.Log(f"Done Generating Initial Outline", 4)

    _Logger.Log(f"Entering Feedback/Revision Loop", 3)
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
    WritingHistory = Messages
    Rating: int = 0
    Iterations: int = 0
    while True:
        Iterations += 1
<<<<<<< HEAD
        Feedback = Writer.Feedback.GetFeedbackOnOutline(Interface, _Logger, Outline)
        Rating = Writer.Feedback.GetOutlineRating(Interface, _Logger, Outline)

        # 如果迭代次数超过最大迭代次数，则退出循环
        if Iterations > Writer.Config.OUTLINE_MAX_REVISIONS:
            break
        # 如果迭代次数超过最小迭代次数且评分达到标准，则退出循环
        if (Iterations > Writer.Config.OUTLINE_MIN_REVISIONS) and (Rating == True):
            break

        # 修订大纲
        Outline = ReviseOutline(Interface, _Logger, Outline, Feedback)

    _Logger.Log(f"达到质量标准，退出反馈/修订循环", 4)

=======
        Feedback = Writer.LLMEditor.GetFeedbackOnOutline(Interface, _Logger, Outline)
        Rating = Writer.LLMEditor.GetOutlineRating(Interface, _Logger, Outline)
        # Rating has been changed from a 0-100 int, to does it meet the standards (yes/no)?
        # Yes it has - the 0-100 int isn't actually good at all, LLM just returned a bunch of junk ratings

        if Iterations > Writer.Config.OUTLINE_MAX_REVISIONS:
            break
        if (Iterations > Writer.Config.OUTLINE_MIN_REVISIONS) and (Rating == True):
            break

        Outline = ReviseOutline(Interface, _Logger, Outline, Feedback)

    _Logger.Log(f"Quality Standard Met, Exiting Feedback/Revision Loop", 4)

    # Generate Final Outline
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
    FinalOutline: str = f"""
{BaseContext}

{StoryElements}

{Outline}
    """

<<<<<<< HEAD
    
    return FinalOutline, StoryElements, Outline, BaseContext


# 定义一个函数，用于修订大纲
def ReviseOutline(Interface, _Logger, _Outline, _Feedback, _History: list = []):

    # 构造修订提示
=======
    return FinalOutline, StoryElements, Outline, BaseContext


def ReviseOutline(Interface, _Logger, _Outline, _Feedback, _History: list = []):

>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
    RevisionPrompt: str = Writer.Prompts.OUTLINE_REVISION_PROMPT.format(
        _Outline=_Outline, _Feedback=_Feedback
    )

<<<<<<< HEAD
    # 记录开始修订大纲
    _Logger.Log(f"修订大纲", 2)
    # 将历史消息添加到消息列表中
    Messages = _History
    # 构造用户查询
    Messages.append(Interface.BuildUserQuery(RevisionPrompt))
    # 使用指定的模型生成文本
    Messages = Interface.SafeGenerateText(
        _Logger, Messages, Writer.Config.INITIAL_OUTLINE_WRITER_MODEL, _MinWordCount=150
    )
    # 获取最后一条消息的文本
    SummaryText: str = Interface.GetLastMessageText(Messages)
    # 记录完成修订大纲
    _Logger.Log(f"完成修订大纲", 2)

    Writer.Logger

    # 返回修订后的文本和消息列表
=======
    _Logger.Log(f"Revising Outline", 2)
    Messages = _History
    Messages.append(Interface.BuildUserQuery(RevisionPrompt))
    Messages = Interface.SafeGenerateText(
        _Logger, Messages, Writer.Config.INITIAL_OUTLINE_WRITER_MODEL, _MinWordCount=250
    )
    SummaryText: str = Interface.GetLastMessageText(Messages)
    _Logger.Log(f"Done Revising Outline", 2)

>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
    return SummaryText, Messages


def GeneratePerChapterOutline(Interface, _Logger, _Chapter, _Outline:str, _History: list = []):

<<<<<<< HEAD
    # 生成每章的大纲
=======
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
    RevisionPrompt: str = Writer.Prompts.CHAPTER_OUTLINE_PROMPT.format(
        _Chapter=_Chapter,
        _Outline=_Outline
    )
<<<<<<< HEAD
    _Logger.Log("为章节 " + str(_Chapter) + " 生成大纲", 5)
=======
    _Logger.Log("Generating Outline For Chapter " + str(_Chapter), 5)
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
    Messages = _History
    Messages.append(Interface.BuildUserQuery(RevisionPrompt))
    Messages = Interface.SafeGenerateText(
        _Logger, Messages, Writer.Config.CHAPTER_OUTLINE_WRITER_MODEL, _MinWordCount=50
    )
    SummaryText: str = Interface.GetLastMessageText(Messages)
<<<<<<< HEAD
    _Logger.Log("完成为章节 " + str(_Chapter) + " 生成大纲", 5)

    return SummaryText, Messages







































# import Writer.LLMEditor
# import Writer.PrintUtils
# import Writer.Config
# import Writer.Outline.StoryElements
# import Writer.Prompts


# # We should probably do outline generation in stages, allowing us to go back and add foreshadowing, etc back to previous segments


# def GenerateOutline(Interface, _Logger, _OutlinePrompt, _QualityThreshold: int = 85):

#     # 生成提示
#     Prompt: str = Writer.Prompts.GET_IMPORTANT_BASE_PROMPT_INFO.format(
#         _Prompt = _OutlinePrompt
#     )


#     # 提取重要基础上下文
#     _Logger.Log(f"Extracting Important Base Context", 4)
#     Messages = [Interface.BuildUserQuery(Prompt)]
#     Messages = Interface.SafeGenerateText(
#         _Logger, Messages, Writer.Config.INITIAL_OUTLINE_WRITER_MODEL
#     )
#     BaseContext: str = Interface.GetLastMessageText(Messages)
#     _Logger.Log(f"Done Extracting Important Base Context", 4)


#     # 生成故事元素
#     StoryElements: str = Writer.Outline.StoryElements.GenerateStoryElements(
#         Interface, _Logger, _OutlinePrompt
#     )


#     # 生成初始大纲
#     Prompt: str = Writer.Prompts.INITIAL_OUTLINE_PROMPT.format(
#         StoryElements=StoryElements, _OutlinePrompt=_OutlinePrompt
#     )


#     _Logger.Log(f"Generating Initial Outline", 4)
#     Messages = [Interface.BuildUserQuery(Prompt)]
#     Messages = Interface.SafeGenerateText(
#         _Logger, Messages, Writer.Config.INITIAL_OUTLINE_WRITER_MODEL, _MinWordCount=150
#     )
#     Outline: str = Interface.GetLastMessageText(Messages)
#     _Logger.Log(f"Done Generating Initial Outline", 4)

#     _Logger.Log(f"Entering Feedback/Revision Loop", 3)
#     WritingHistory = Messages
#     Rating: int = 0
#     Iterations: int = 0
#     while True:
#         Iterations += 1
#         Feedback = Writer.LLMEditor.GetFeedbackOnOutline(Interface, _Logger, Outline)
#         Rating = Writer.LLMEditor.GetOutlineRating(Interface, _Logger, Outline)

#         # 如果迭代次数超过最大迭代次数，则退出循环
#         if Iterations > Writer.Config.OUTLINE_MAX_REVISIONS:
#             break
#         # 如果迭代次数超过最小迭代次数且评分达到标准，则退出循环
#         if (Iterations > Writer.Config.OUTLINE_MIN_REVISIONS) and (Rating == True):
#             break

#         # 修订大纲
#         Outline = ReviseOutline(Interface, _Logger, Outline, Feedback)

#     _Logger.Log(f"Quality Standard Met, Exiting Feedback/Revision Loop", 4)

#     FinalOutline: str = f"""
# {BaseContext}

# {StoryElements}

# {Outline}
#     """

#     return FinalOutline, StoryElements, Outline, BaseContext


# # 定义一个函数，用于修订大纲
# def ReviseOutline(Interface, _Logger, _Outline, _Feedback, _History: list = []):

#     # 构造修订提示
#     RevisionPrompt: str = Writer.Prompts.OUTLINE_REVISION_PROMPT.format(
#         _Outline=_Outline, _Feedback=_Feedback
#     )

#     # 记录开始修订大纲
#     _Logger.Log(f"Revising Outline", 2)
#     # 将历史消息添加到消息列表中
#     Messages = _History
#     # 构造用户查询
#     Messages.append(Interface.BuildUserQuery(RevisionPrompt))
#     # 使用指定的模型生成文本
#     Messages = Interface.SafeGenerateText(
#         _Logger, Messages, Writer.Config.INITIAL_OUTLINE_WRITER_MODEL, _MinWordCount=150
#     )
#     # 获取最后一条消息的文本
#     SummaryText: str = Interface.GetLastMessageText(Messages)
#     # 记录完成修订大纲
#     _Logger.Log(f"Done Revising Outline", 2)

#     # 返回修订后的文本和消息列表
#     return SummaryText, Messages


# def GeneratePerChapterOutline(Interface, _Logger, _Chapter, _Outline:str, _History: list = []):

#     # 生成每章的大纲
#     RevisionPrompt: str = Writer.Prompts.CHAPTER_OUTLINE_PROMPT.format(
#         _Chapter=_Chapter,
#         _Outline=_Outline
#     )
#     _Logger.Log("Generating Outline For Chapter " + str(_Chapter), 5)
#     Messages = _History
#     Messages.append(Interface.BuildUserQuery(RevisionPrompt))
#     Messages = Interface.SafeGenerateText(
#         _Logger, Messages, Writer.Config.CHAPTER_OUTLINE_WRITER_MODEL, _MinWordCount=50
#     )
#     SummaryText: str = Interface.GetLastMessageText(Messages)
#     _Logger.Log("Done Generating Outline For Chapter " + str(_Chapter), 5)

#     return SummaryText, Messages
=======
    _Logger.Log("Done Generating Outline For Chapter " + str(_Chapter), 5)

    return SummaryText, Messages
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
