<<<<<<< HEAD
import Writer.Feedback
import Writer.Logger
=======
import Writer.LLMEditor
import Writer.PrintUtils
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
import Writer.Config
import Writer.Chapter.ChapterGenSummaryCheck
import Writer.Prompts

<<<<<<< HEAD
def get_template():
    dir='template/scene_to_json'
    with open(dir+'/user.txt', 'r',encoding='utf-8') as f:
        user_template = f.read()
    with open(dir+'/ai.txt', 'r',encoding='utf-8') as f:
        ai_template = f.read()
    return user_template, ai_template


def ScenesToJSON(Interface, _Logger, _Scenes:str):

    # 记录开始转换章节场景到JSON的过程
    _Logger.Log(f"Starting ChapterScenes->JSON", 2)

    # 创建一个空列表，用于存储消息历史
    MesssageHistory: list = []
    # 将系统提示添加到消息历史中
    MesssageHistory.append(Interface.BuildSystemQuery(Writer.Prompts.DEFAULT_SYSTEM_PROMPT_TO_JSON))
    # 将用户提示添加到消息历史中
    user_template, ai_template = get_template()
    MesssageHistory.append(Interface.BuildUserQuery(Writer.Prompts.SCENES_TO_JSON.format(_Scenes=_Scenes, _UserPrompt=user_template, _AssistantPrompt=ai_template)))

    # 使用安全生成JSON的方法，将消息历史和检查模型作为参数传入
    _, SceneList = Interface.SafeGenerateJSON(_Logger, MesssageHistory, Writer.Config.CHECKER_MODEL)

    # 记录完成转换章节场景到JSON的过程，并输出找到的场景数量
    _Logger.Log(f"Finished ChapterScenes->JSON ({len(SceneList)} Scenes Found)", 5)


    # 返回找到的场景列表
=======

def ScenesToJSON(Interface, _Logger, _Scenes:str):

    # This function converts the given scene list (from markdown format, to a specified JSON format).

    _Logger.Log(f"Starting ChapterScenes->JSON", 2)
    MesssageHistory: list = []
    MesssageHistory.append(Interface.BuildSystemQuery(Writer.Prompts.DEFAULT_SYSTEM_PROMPT))
    MesssageHistory.append(Interface.BuildUserQuery(Writer.Prompts.SCENES_TO_JSON.format(_Scenes=_Scenes)))

    _, SceneList = Interface.SafeGenerateJSON(_Logger, MesssageHistory, Writer.Config.CHECKER_MODEL)
    _Logger.Log(f"Finished ChapterScenes->JSON ({len(SceneList)} Scenes Found)", 5)

>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
    return SceneList
