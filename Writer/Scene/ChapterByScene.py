<<<<<<< HEAD
import Writer.Feedback
import Writer.Logger
import Writer.Config
import Writer.Chapter.ChapterGenSummaryCheck
import Writer.Prompts
import Writer.Scene.ChapterOutlineToScenesOutline
=======
import Writer.LLMEditor
import Writer.PrintUtils
import Writer.Config
import Writer.Chapter.ChapterGenSummaryCheck
import Writer.Prompts
import Writer.Scene.ChapterOutlineToScenes
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
import Writer.Scene.ScenesToJSON
import Writer.Scene.SceneOutlineToScene



def ChapterByScene(Interface, _Logger, _ThisChapter:str, _Outline:str, _BaseContext:str = ""):

    # This function calls all other scene-by-scene generation functions and creates a full chapter based on the new scene pipeline.

    _Logger.Log(f"Starting Scene-By-Scene Chapter Generation Pipeline", 2)

<<<<<<< HEAD
    # 将章节大纲转换为场景
    SceneBySceneOutline = Writer.Scene.ChapterOutlineToScenesOutline.ChapterOutlineToScenes(Interface, _Logger, _ThisChapter, _Outline, _BaseContext=_BaseContext)

    # 将场景转换为JSON格式
=======
    SceneBySceneOutline = Writer.Scene.ChapterOutlineToScenes.ChapterOutlineToScenes(Interface, _Logger, _ThisChapter, _Outline, _BaseContext=_BaseContext)

>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
    SceneJSONList = Writer.Scene.ScenesToJSON.ScenesToJSON(Interface, _Logger, SceneBySceneOutline)


    # Now we iterate through each scene one at a time and write it, then add it to this rough chapter, which is then returned for further editing
<<<<<<< HEAD
    # 遍历每个场景，一次写入，然后将其添加到这个粗糙的章节中，然后返回进行进一步编辑
    RoughChapter:str = ""
    for Scene in SceneJSONList:
        # 将场景大纲转换为场景
        RoughChapter += Writer.Scene.SceneOutlineToScene.SceneOutlineToScene(Interface, _Logger, Scene, _Outline, _BaseContext)


    _Logger.Log(f"Finished Scene-By-Scene Chapter Generation Pipeline", 2)
=======
    RoughChapter:str = ""
    for Scene in SceneJSONList:
        RoughChapter += Writer.Scene.SceneOutlineToScene.SceneOutlineToScene(Interface, _Logger, Scene, _Outline, _BaseContext)


    _Logger.Log(f"Starting Scene-By-Scene Chapter Generation Pipeline", 2)
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16

    return RoughChapter
