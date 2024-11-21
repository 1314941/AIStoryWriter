<<<<<<< HEAD
import Writer.Feedback
import Writer.Logger
import Writer.Config
import Writer.Chapter.ChapterGenSummaryCheck
import Writer.Prompts 


# 定义一个函数，将场景大纲转换为场景
def SceneOutlineToScene(Interface, _Logger, _ThisSceneOutline:str, _Outline:str, _BaseContext: str = ""):

    # 记录开始转换场景大纲
    # _Logger.Log(f"Starting SceneOutline->Scene", 2)
    _Logger.Log(f"开始场景大纲到场景的转换", 2)
    # 创建一个空列表，用于存储消息历史
    MesssageHistory: list = []
    # 将默认系统提示添加到消息历史中
    MesssageHistory.append(Interface.BuildSystemQuery(Writer.Prompts.DEFAULT_SYSTEM_PROMPT))
    # 将场景大纲转换为场景的提示添加到消息历史中
    MesssageHistory.append(Interface.BuildUserQuery(Writer.Prompts.SCENE_OUTLINE_TO_SCENE.format(_SceneOutline=_ThisSceneOutline, _Outline=_Outline)))

    # 使用指定的模型生成文本，并记录最小单词数
    Response = Interface.SafeGenerateText(_Logger, MesssageHistory, Writer.Config.CHAPTER_STAGE1_WRITER_MODEL, _MinWordCount=100)
    # 记录完成转换场景大纲
    # _Logger.Log(f"Finished SceneOutline->Scene", 5)
    _Logger.Log(f"完成场景大纲到场景的转换", 5)

    # 返回生成的文本
=======
import Writer.LLMEditor
import Writer.PrintUtils
import Writer.Config
import Writer.Chapter.ChapterGenSummaryCheck
import Writer.Prompts


def SceneOutlineToScene(Interface, _Logger, _ThisSceneOutline:str, _Outline:str, _BaseContext: str = ""):

    # Now we're finally going to go and write the scene provided.


    _Logger.Log(f"Starting SceneOutline->Scene", 2)
    MesssageHistory: list = []
    MesssageHistory.append(Interface.BuildSystemQuery(Writer.Prompts.DEFAULT_SYSTEM_PROMPT))
    MesssageHistory.append(Interface.BuildUserQuery(Writer.Prompts.SCENE_OUTLINE_TO_SCENE.format(_SceneOutline=_ThisSceneOutline, _Outline=_Outline)))

    Response = Interface.SafeGenerateText(_Logger, MesssageHistory, Writer.Config.CHAPTER_STAGE1_WRITER_MODEL, _MinWordCount=100)
    _Logger.Log(f"Finished SceneOutline->Scene", 5)

>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
    return Interface.GetLastMessageText(Response)
