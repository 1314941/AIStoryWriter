import json

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

import Writer.Scene.ChapterByScene

def GenerateChapter(
    Interface,
    _Logger,
    _ChapterNum: int,
    _TotalChapters: int,
    _Outline: str,
    _Chapters: list = [],
    _QualityThreshold: int = 85,
    _BaseContext:str = ""
):

    # Some important notes
    # We're going to remind the author model of the previous chapters here, so it knows what has been written before.

    #### Stage 0: Create base language chain
    _Logger.Log(f"Creating Base Langchain For Chapter {_ChapterNum} Generation", 2)
    MesssageHistory: list = []
    MesssageHistory.append(
        Interface.BuildSystemQuery(
            Writer.Prompts.CHAPTER_GENERATION_INTRO.format(
                _ChapterNum=_ChapterNum, _TotalChapters=_TotalChapters
            )
        )
    )

    ContextHistoryInsert: str = ""

    if len(_Chapters) > 0:

        ChapterSuperlist: str = ""
        for Chapter in _Chapters:
            ChapterSuperlist += f"{Chapter}\n"

        ContextHistoryInsert += Writer.Prompts.CHAPTER_HISTORY_INSERT.format(
            _Outline=_Outline, ChapterSuperlist=ChapterSuperlist
        )

    #
    # MesssageHistory.append(Interface.BuildUserQuery(f"""
    # Here is the novel so far.
    # """))
    # MesssageHistory.append(Interface.BuildUserQuery(ChapterSuperlist))
    # MesssageHistory.append(Interface.BuildSystemQuery("Make sure to pay attention to the content that has happened in these previous chapters. It's okay to deviate from the outline a little in order to ensure you continue the same story from previous chapters."))

    # Now, extract the this-chapter-outline segment
<<<<<<< HEAD
    # _Logger.Log(f"Extracting Chapter Specific Outline", 4)
    _Logger.Log(f"提取章节的大纲段落", 4)
=======
    _Logger.Log(f"Extracting Chapter Specific Outline", 4)
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
    ThisChapterOutline: str = ""
    ChapterSegmentMessages = []
    ChapterSegmentMessages.append(
        Interface.BuildSystemQuery(Writer.Prompts.CHAPTER_GENERATION_INTRO)
    )
    ChapterSegmentMessages.append(
        Interface.BuildUserQuery(
            Writer.Prompts.CHAPTER_GENERATION_PROMPT.format(
                _Outline=_Outline, _ChapterNum=_ChapterNum
            )
        )
    )
    ChapterSegmentMessages = Interface.SafeGenerateText(
        _Logger,
        ChapterSegmentMessages,
<<<<<<< HEAD
        Writer.Config.CHAPTER_STAGE1_WRITER_MODEL, _MinWordCount=55
    )  # CHANGE THIS MODEL EVENTUALLY - BUT IT WORKS FOR NOW!!!
    ThisChapterOutline: str = Interface.GetLastMessageText(ChapterSegmentMessages)
    # _Logger.Log(f"Created Chapter Specific Outline", 4)
    _Logger.Log(f"创建了章节的大纲段落", 4)
=======
        Writer.Config.CHAPTER_STAGE1_WRITER_MODEL, _MinWordCount=120
    )  # CHANGE THIS MODEL EVENTUALLY - BUT IT WORKS FOR NOW!!!
    ThisChapterOutline: str = Interface.GetLastMessageText(ChapterSegmentMessages)
    _Logger.Log(f"Created Chapter Specific Outline", 4)
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16

    # Generate Summary of Last Chapter If Applicable
    FormattedLastChapterSummary: str = ""
    if len(_Chapters) > 0:
<<<<<<< HEAD
        # _Logger.Log(f"Creating Summary Of Last Chapter Info", 3)
        _Logger.Log(f"正在创建上一章节的总结信息", 3)
=======
        _Logger.Log(f"Creating Summary Of Last Chapter Info", 3)
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
        ChapterSummaryMessages = []
        ChapterSummaryMessages.append(
            Interface.BuildSystemQuery(Writer.Prompts.CHAPTER_SUMMARY_INTRO)
        )
        ChapterSummaryMessages.append(
            Interface.BuildUserQuery(
                Writer.Prompts.CHAPTER_SUMMARY_PROMPT.format(
                    _ChapterNum=_ChapterNum,
                    _TotalChapters=_TotalChapters,
                    _Outline=_Outline,
                    _LastChapter=_Chapters[-1],
                )
            )
        )
        ChapterSummaryMessages = Interface.SafeGenerateText(
            _Logger,
            ChapterSummaryMessages,
<<<<<<< HEAD
            Writer.Config.CHAPTER_STAGE1_WRITER_MODEL, _MinWordCount=55
=======
            Writer.Config.CHAPTER_STAGE1_WRITER_MODEL, _MinWordCount=100
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
        )  # CHANGE THIS MODEL EVENTUALLY - BUT IT WORKS FOR NOW!!!
        FormattedLastChapterSummary: str = Interface.GetLastMessageText(
            ChapterSummaryMessages
        )
<<<<<<< HEAD
        # _Logger.Log(f"Created Summary Of Last Chapter Info", 3)
        _Logger.Log(f"创建了上一章节的总结信息", 3)
=======
        _Logger.Log(f"Created Summary Of Last Chapter Info", 3)
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16

    DetailedChapterOutline: str = ThisChapterOutline
    if FormattedLastChapterSummary != "":
        DetailedChapterOutline = ThisChapterOutline

<<<<<<< HEAD
    # _Logger.Log(f"Done with base langchain setup", 2)
    _Logger.Log(f"完成了基础语言链的设置", 2)
=======
    _Logger.Log(f"Done with base langchain setup", 2)
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16


    # If scene generation disabled, use the normal initial plot generator
    Stage1Chapter = ""
    if (not Writer.Config.SCENE_GENERATION_PIPELINE):

        #### STAGE 1: Create Initial Plot
        IterCounter: int = 0
        Feedback: str = ""
        while True:
            Prompt = Writer.Prompts.CHAPTER_GENERATION_STAGE1.format(
                ContextHistoryInsert=ContextHistoryInsert,
                _ChapterNum=_ChapterNum,
                _TotalChapters=_TotalChapters,
                ThisChapterOutline=ThisChapterOutline,
                FormattedLastChapterSummary=FormattedLastChapterSummary,
                Feedback=Feedback,
                _BaseContext=_BaseContext
            )

            # Generate Initial Chapter
<<<<<<< HEAD
            # _Logger.Log(
            #     f"Generating Initial Chapter (Stage 1: Plot) {_ChapterNum}/{_TotalChapters} (Iteration {IterCounter})",
            #     5,
            # )
            _Logger.Log(
                f"正在生成初始章节（阶段1：情节） {_ChapterNum}/{_TotalChapters} (迭代次数 {IterCounter})",
=======
            _Logger.Log(
                f"Generating Initial Chapter (Stage 1: Plot) {_ChapterNum}/{_TotalChapters} (Iteration {IterCounter})",
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
                5,
            )
            Messages = MesssageHistory.copy()
            Messages.append(Interface.BuildUserQuery(Prompt))

            Messages = Interface.SafeGenerateText(
                _Logger,
                Messages,
                Writer.Config.CHAPTER_STAGE1_WRITER_MODEL,
                _SeedOverride=IterCounter + Writer.Config.SEED,
<<<<<<< HEAD
                _MinWordCount=50
            )
            IterCounter += 1
            Stage1Chapter: str = Interface.GetLastMessageText(Messages)
            # _Logger.Log(
            #     f"Finished Initial Generation For Initial Chapter (Stage 1: Plot)  {_ChapterNum}/{_TotalChapters}",
            #     5,
            # )
            _Logger.Log(
                f"完成了初始生成初始章节（阶段1：情节） {_ChapterNum}/{_TotalChapters}",
=======
                _MinWordCount=100
            )
            IterCounter += 1
            Stage1Chapter: str = Interface.GetLastMessageText(Messages)
            _Logger.Log(
                f"Finished Initial Generation For Initial Chapter (Stage 1: Plot)  {_ChapterNum}/{_TotalChapters}",
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
                5,
            )

            # Check if LLM did the work
            if IterCounter > Writer.Config.CHAPTER_MAX_REVISIONS:
<<<<<<< HEAD
                # _Logger.Log(
                #     "Chapter Summary-Based Revision Seems Stuck - Forcefully Exiting", 7
                # )
                _Logger.Log(
                    "基于章节摘要的修订似乎卡住了 - 强制退出", 7
=======
                _Logger.Log(
                    "Chapter Summary-Based Revision Seems Stuck - Forcefully Exiting", 7
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
                )
                break
            Result, Feedback = Writer.Chapter.ChapterGenSummaryCheck.LLMSummaryCheck(
                Interface, _Logger, DetailedChapterOutline, Stage1Chapter
            )
            if Result:
<<<<<<< HEAD
                # _Logger.Log(
                #     f"Done Generating Initial Chapter (Stage 1: Plot)  {_ChapterNum}/{_TotalChapters}",
                #     5,
                # )

                _Logger.Log(
                    f"完成了生成初始章节（阶段1：情节） {_ChapterNum}/{_TotalChapters}",
=======
                _Logger.Log(
                    f"Done Generating Initial Chapter (Stage 1: Plot)  {_ChapterNum}/{_TotalChapters}",
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
                    5,
                )
                break
    
    else:

        Stage1Chapter = Writer.Scene.ChapterByScene.ChapterByScene(Interface, _Logger, ThisChapterOutline, _Outline, _BaseContext)


    #### STAGE 2: Add Character Development
    Stage2Chapter = ""
    IterCounter: int = 0
    Feedback: str = ""
    while True:
        Prompt = Writer.Prompts.CHAPTER_GENERATION_STAGE2.format(
            ContextHistoryInsert=ContextHistoryInsert,
            _ChapterNum=_ChapterNum,
            _TotalChapters=_TotalChapters,
            ThisChapterOutline=ThisChapterOutline,
            FormattedLastChapterSummary=FormattedLastChapterSummary,
            Stage1Chapter=Stage1Chapter,
            Feedback=Feedback,
            _BaseContext=_BaseContext
        )

        # Generate Initial Chapter
<<<<<<< HEAD
        # _Logger.Log(
        #     f"Generating Initial Chapter (Stage 2: Character Development) {_ChapterNum}/{_TotalChapters} (Iteration {IterCounter})",
        #     5,
        # )
        _Logger.Log(
            f"正在生成初始章节（阶段2：角色发展） {_ChapterNum}/{_TotalChapters} (迭代次数 {IterCounter})",
=======
        _Logger.Log(
            f"Generating Initial Chapter (Stage 2: Character Development) {_ChapterNum}/{_TotalChapters} (Iteration {IterCounter})",
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
            5,
        )
        Messages = MesssageHistory.copy()
        Messages.append(Interface.BuildUserQuery(Prompt))

        Messages = Interface.SafeGenerateText(
            _Logger,
            Messages,
            Writer.Config.CHAPTER_STAGE2_WRITER_MODEL,
            _SeedOverride=IterCounter + Writer.Config.SEED,
<<<<<<< HEAD
            _MinWordCount=50
=======
            _MinWordCount=100
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
        )
        IterCounter += 1
        Stage2Chapter: str = Interface.GetLastMessageText(Messages)
        _Logger.Log(
            f"Finished Initial Generation For Initial Chapter (Stage 2: Character Development)  {_ChapterNum}/{_TotalChapters}",
            5,
        )

        # Check if LLM did the work
        if IterCounter > Writer.Config.CHAPTER_MAX_REVISIONS:
            _Logger.Log(
                "Chapter Summary-Based Revision Seems Stuck - Forcefully Exiting", 7
            )
            break
        Result, Feedback = Writer.Chapter.ChapterGenSummaryCheck.LLMSummaryCheck(
            Interface, _Logger, DetailedChapterOutline, Stage2Chapter
        )
        if Result:
            _Logger.Log(
                f"Done Generating Initial Chapter (Stage 2: Character Development)  {_ChapterNum}/{_TotalChapters}",
                5,
            )
            break

    #### STAGE 3: Add Dialogue
    Stage3Chapter = ""
    IterCounter: int = 0
    Feedback: str = ""
    while True:
        Prompt = Writer.Prompts.CHAPTER_GENERATION_STAGE3.format(
            ContextHistoryInsert=ContextHistoryInsert,
            _ChapterNum=_ChapterNum,
            _TotalChapters=_TotalChapters,
            ThisChapterOutline=ThisChapterOutline,
            FormattedLastChapterSummary=FormattedLastChapterSummary,
            Stage2Chapter=Stage2Chapter,
            Feedback=Feedback,
            _BaseContext=_BaseContext
        )
        # Generate Initial Chapter
        _Logger.Log(
            f"Generating Initial Chapter (Stage 3: Dialogue) {_ChapterNum}/{_TotalChapters} (Iteration {IterCounter})",
            5,
        )
        Messages = MesssageHistory.copy()
        Messages.append(Interface.BuildUserQuery(Prompt))

        Messages = Interface.SafeGenerateText(
            _Logger,
            Messages,
            Writer.Config.CHAPTER_STAGE3_WRITER_MODEL,
            _SeedOverride=IterCounter + Writer.Config.SEED,
<<<<<<< HEAD
            _MinWordCount=50
=======
            _MinWordCount=100
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
        )
        IterCounter += 1
        Stage3Chapter: str = Interface.GetLastMessageText(Messages)
        _Logger.Log(
            f"Finished Initial Generation For Initial Chapter (Stage 3: Dialogue)  {_ChapterNum}/{_TotalChapters}",
            5,
        )

        # Check if LLM did the work
        if IterCounter > Writer.Config.CHAPTER_MAX_REVISIONS:
            _Logger.Log(
                "Chapter Summary-Based Revision Seems Stuck - Forcefully Exiting", 7
            )
            break
        Result, Feedback = Writer.Chapter.ChapterGenSummaryCheck.LLMSummaryCheck(
            Interface, _Logger, DetailedChapterOutline, Stage3Chapter
        )
        if Result:
            _Logger.Log(
                f"Done Generating Initial Chapter (Stage 3: Dialogue)  {_ChapterNum}/{_TotalChapters}",
                5,
            )
            break

        #     #### STAGE 4: Final-Pre-Revision Edit Pass
        # Prompt = Writer.Prompts.CHAPTER_GENERATION_STAGE4.format(
        #    ContextHistoryInsert=ContextHistoryInsert,
        #     _ChapterNum=_ChapterNum,
        #     _TotalChapters=_TotalChapters,
        #     _Outline=_Outline,
        #     Stage3Chapter=Stage3Chapter,
        #     Feedback=Feedback,
        # )

    #     # Generate Initial Chapter
    #     _Logger.Log(f"Generating Initial Chapter (Stage 4: Final Pass) {_ChapterNum}/{_TotalChapters}", 5)
    #     Messages = MesssageHistory.copy()
    #     Messages.append(Interface.BuildUserQuery(Prompt))

    #     Messages = Interface.SafeGenerateText(_Logger, Messages, Writer.Config.CHAPTER_STAGE4_WRITER_MODEL)
    #     Chapter:str = Interface.GetLastMessageText(Messages)
    #     _Logger.Log(f"Done Generating Initial Chapter (Stage 4: Final Pass)  {_ChapterNum}/{_TotalChapters}", 5)
    Chapter: str = Stage3Chapter

    #### Stage 5: Revision Cycle
    if Writer.Config.CHAPTER_NO_REVISIONS:
        _Logger.Log(f"Chapter Revision Disabled In Config, Exiting Now", 5)
        return Chapter

    _Logger.Log(
        f"Entering Feedback/Revision Loop (Stage 5) For Chapter {_ChapterNum}/{_TotalChapters}",
        4,
    )
    WritingHistory = MesssageHistory.copy()
    Rating: int = 0
    Iterations: int = 0
    while True:
        Iterations += 1
<<<<<<< HEAD
        Feedback = Writer.Feedback.GetFeedbackOnChapter(
            Interface, _Logger, Chapter, _Outline
        )
        Rating = Writer.Feedback.GetChapterRating(Interface, _Logger, Chapter)
=======
        Feedback = Writer.LLMEditor.GetFeedbackOnChapter(
            Interface, _Logger, Chapter, _Outline
        )
        Rating = Writer.LLMEditor.GetChapterRating(Interface, _Logger, Chapter)
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16

        if Iterations > Writer.Config.CHAPTER_MAX_REVISIONS:
            break
        if (Iterations > Writer.Config.CHAPTER_MIN_REVISIONS) and (Rating == True):
            break
        Chapter, WritingHistory = ReviseChapter(
            Interface, _Logger, Chapter, Feedback, WritingHistory
        )

    _Logger.Log(
        f"Quality Standard Met, Exiting Feedback/Revision Loop (Stage 5) For Chapter {_ChapterNum}/{_TotalChapters}",
        4,
    )

    return Chapter


def ReviseChapter(Interface, _Logger, _Chapter, _Feedback, _History: list = []):

    RevisionPrompt = Writer.Prompts.CHAPTER_REVISION.format(
        _Chapter=_Chapter, _Feedback=_Feedback
    )

    _Logger.Log("Revising Chapter", 5)
    Messages = _History
    Messages.append(Interface.BuildUserQuery(RevisionPrompt))
    Messages = Interface.SafeGenerateText(
        _Logger, Messages, Writer.Config.CHAPTER_REVISION_WRITER_MODEL,
<<<<<<< HEAD
        _MinWordCount=50
=======
        _MinWordCount=100
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
    )
    SummaryText: str = Interface.GetLastMessageText(Messages)
    _Logger.Log("Done Revising Chapter", 5)

    return SummaryText, Messages
