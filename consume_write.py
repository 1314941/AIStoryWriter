#!/bin/python3

import argparse
import time
import datetime
import os
import json

import Writer.Config

import Writer.Interface.Wrapper
import Writer.Logger
import Writer.Chapter.ChapterDetector
import Writer.Scrubber
import Writer.Statistics
import Writer.OutlineGenerator
import Writer.Chapter.ChapterGenerator
import Writer.StoryInfo
import Writer.NovelEditor
import Writer.Translator


# Setup Argparser
Parser = argparse.ArgumentParser()
Parser.add_argument("-Prompt",
                    default="prompt.txt", 
                    help="Path to file containing the prompt")
Parser.add_argument(
    "-Output",
    default="",
    type=str,
    help="Optional file output path, if none is speciifed, we will autogenerate a file name based on the story title",
)
Parser.add_argument(
    "-InitialOutlineModel",
    default=Writer.Config.INITIAL_OUTLINE_WRITER_MODEL,
    type=str,
    help="Model to use for writing the base outline content",
)
Parser.add_argument(
    "-ChapterOutlineModel",
    default=Writer.Config.CHAPTER_OUTLINE_WRITER_MODEL,
    type=str,
    help="Model to use for writing the per-chapter outline content",
)
Parser.add_argument(
    "-ChapterS1Model",
    default=Writer.Config.CHAPTER_STAGE1_WRITER_MODEL,
    type=str,
    help="Model to use for writing the chapter (stage 1: plot)",
)
Parser.add_argument(
    "-ChapterS2Model",
    default=Writer.Config.CHAPTER_STAGE2_WRITER_MODEL,
    type=str,
    help="Model to use for writing the chapter (stage 2: character development)",
)
Parser.add_argument(
    "-ChapterS3Model",
    default=Writer.Config.CHAPTER_STAGE3_WRITER_MODEL,
    type=str,
    help="Model to use for writing the chapter (stage 3: dialogue)",
)
Parser.add_argument(
    "-ChapterS4Model",
    default=Writer.Config.CHAPTER_STAGE4_WRITER_MODEL,
    type=str,
    help="Model to use for writing the chapter (stage 4: final correction pass)",
)
Parser.add_argument(
    "-ChapterRevisionModel",
    default=Writer.Config.CHAPTER_REVISION_WRITER_MODEL,
    type=str,
    help="Model to use for revising the chapter until it meets criteria",
)
Parser.add_argument(
    "-RevisionModel",
    default=Writer.Config.REVISION_MODEL,
    type=str,
    help="Model to use for generating constructive criticism",
)
Parser.add_argument(
    "-EvalModel",
    default=Writer.Config.EVAL_MODEL,
    type=str,
    help="Model to use for evaluating the rating out of 100",
)
Parser.add_argument(
    "-InfoModel",
    default=Writer.Config.INFO_MODEL,
    type=str,
    help="Model to use when generating summary/info at the end",
)
Parser.add_argument(
    "-ScrubModel",
    default=Writer.Config.SCRUB_MODEL,
    type=str,
    help="Model to use when scrubbing the story at the end",
)
Parser.add_argument(
    "-CheckerModel",
    default=Writer.Config.CHECKER_MODEL,
    type=str,
    help="Model to use when checking if the LLM cheated or not",
)
Parser.add_argument(
    "-TranslatorModel",
    default=Writer.Config.TRANSLATOR_MODEL,
    type=str,
    help="Model to use if translation of the story is enabled",
)
Parser.add_argument(
    "-Translate",
    default="",
    type=str,
    help="Specify a language to translate the story to - will not translate by default. Ex: 'French'",
)
Parser.add_argument(
    "-TranslatePrompt",
    default="",
    type=str,
    help="Specify a language to translate your input prompt to. Ex: 'French'",
)
Parser.add_argument("-Seed", default=12, type=int, help="Used to seed models.")
Parser.add_argument(
    "-OutlineMinRevisions",
    default=0,
    type=int,
    help="Number of minimum revisions that the outline must be given prior to proceeding",
)
Parser.add_argument(
    "-OutlineMaxRevisions",
    default=3,
    type=int,
    help="Max number of revisions that the outline may have",
)
Parser.add_argument(
    "-ChapterMinRevisions",
    default=0,
    type=int,
    help="Number of minimum revisions that the chapter must be given prior to proceeding",
)
Parser.add_argument(
    "-ChapterMaxRevisions",
    default=3,
    type=int,
    help="Max number of revisions that the chapter may have",
)
Parser.add_argument(
    "-NoChapterRevision", action="store_true", help="Disables Chapter Revisions"
)
Parser.add_argument(
    "-NoScrubChapters",
    action="store_true",
    help="Disables a final pass over the story to remove prompt leftovers/outline tidbits",
)
Parser.add_argument(
    "-ExpandOutline",
    action="store_true",
    default=True,
    help="Disables the system from expanding the outline for the story chapter by chapter prior to writing the story's chapter content",
)
Parser.add_argument(
    "-EnableFinalEditPass",
    action="store_true",
    help="Enable a final edit pass of the whole story prior to scrubbing",
)
Parser.add_argument(
    "-Debug",
    action="store_true",
    help="Print system prompts to stdout during generation",
)
Parser.add_argument(
    "-SceneGenerationPipeline",
    action="store_true",
    default=True,
    help="Use the new scene-by-scene generation pipeline as an initial starting point for chapter writing",
)
Args = Parser.parse_args()


# Measure Generation Time
StartTime = time.time()


# Setup Config
Writer.Config.SEED = Args.Seed

Writer.Config.INITIAL_OUTLINE_WRITER_MODEL = Args.InitialOutlineModel
Writer.Config.CHAPTER_OUTLINE_WRITER_MODEL = Args.ChapterOutlineModel
Writer.Config.CHAPTER_STAGE1_WRITER_MODEL = Args.ChapterS1Model
Writer.Config.CHAPTER_STAGE2_WRITER_MODEL = Args.ChapterS2Model
Writer.Config.CHAPTER_STAGE3_WRITER_MODEL = Args.ChapterS3Model
Writer.Config.CHAPTER_STAGE4_WRITER_MODEL = Args.ChapterS4Model
Writer.Config.CHAPTER_REVISION_WRITER_MODEL = Args.ChapterRevisionModel
Writer.Config.EVAL_MODEL = Args.EvalModel
Writer.Config.REVISION_MODEL = Args.RevisionModel
Writer.Config.INFO_MODEL = Args.InfoModel
Writer.Config.SCRUB_MODEL = Args.ScrubModel
Writer.Config.CHECKER_MODEL = Args.CheckerModel
Writer.Config.TRANSLATOR_MODEL = Args.TranslatorModel

Writer.Config.TRANSLATE_LANGUAGE = Args.Translate
Writer.Config.TRANSLATE_PROMPT_LANGUAGE = Args.TranslatePrompt

Writer.Config.OUTLINE_MIN_REVISIONS = Args.OutlineMinRevisions
Writer.Config.OUTLINE_MAX_REVISIONS = Args.OutlineMaxRevisions

Writer.Config.CHAPTER_MIN_REVISIONS = Args.ChapterMinRevisions
Writer.Config.CHAPTER_MAX_REVISIONS = Args.ChapterMaxRevisions
Writer.Config.CHAPTER_NO_REVISIONS = Args.NoChapterRevision

Writer.Config.SCRUB_NO_SCRUB = Args.NoScrubChapters
Writer.Config.EXPAND_OUTLINE = Args.ExpandOutline
Writer.Config.ENABLE_FINAL_EDIT_PASS = Args.EnableFinalEditPass

Writer.Config.OPTIONAL_OUTPUT_NAME = Args.Output
Writer.Config.SCENE_GENERATION_PIPELINE = Args.SceneGenerationPipeline
Writer.Config.DEBUG = Args.Debug

# Get a list of all used providers
Models = [
    Writer.Config.INITIAL_OUTLINE_WRITER_MODEL,
    Writer.Config.CHAPTER_OUTLINE_WRITER_MODEL,
    Writer.Config.CHAPTER_STAGE1_WRITER_MODEL,
    Writer.Config.CHAPTER_STAGE2_WRITER_MODEL,
    Writer.Config.CHAPTER_STAGE3_WRITER_MODEL,
    Writer.Config.CHAPTER_STAGE4_WRITER_MODEL,
    Writer.Config.CHAPTER_REVISION_WRITER_MODEL,
    Writer.Config.EVAL_MODEL,
    Writer.Config.REVISION_MODEL,
    Writer.Config.INFO_MODEL,
    Writer.Config.SCRUB_MODEL,
    Writer.Config.CHECKER_MODEL,
    Writer.Config.TRANSLATOR_MODEL,
]
Models = list(set(Models))


#step
"""
0 开始
1 生成大纲
2 生成章节大纲
  读取大纲
  从第几章开始写
3 写章节
  读取大纲 章节大纲
  写第几章
4 整合章节
5.输出小说
"""
class NovelWriter:
    def __init__(self):
        self.SysLogger = None
        self.Interface = None
        self.Prompt = None

      # Setup Logger
    def init(self):
        if self.choice=="y":
            self.SysLogger = Writer.Logger.Logger(self.novel_path)

            self.step,self.done_chapter_outlines,self.done_chapters,self.chapter_num=self.SysLogger.get_record()
            self.NumChapters=self.chapter_num


            self.SysLogger.Log("创建 OLLAMA 接口", 5)
            self.Interface = Writer.Interface.Wrapper.Interface(Models)

            Prompt: str = ""
            Prompt = self.SysLogger.get_prompt()

            self.SysLogger.Log("Story loaded successfully!",5)
        else:
            self.SysLogger = Writer.Logger.Logger()

            self.step,self.done_chapter_outlines,self.done_chapters,self.chapter_num=0,0,0,0
            self.NumChapters=0

            # Initialize Interface
            self.SysLogger.Log("创建 OLLAMA 接口", 5)
            self.Interface = Writer.Interface.Wrapper.Interface(Models)

            # Load User Prompt
            Prompt: str = ""
            if Args.Prompt is None:
                raise Exception("No Prompt Provided")
            with open(Args.Prompt, "r", encoding="utf-8") as f:
                Prompt = f.read()


            # If user wants their prompt translated, do so
            if Writer.Config.TRANSLATE_PROMPT_LANGUAGE != "":
                Prompt = Writer.Translator.TranslatePrompt(
                    self.Interface, self.SysLogger, Prompt, Writer.Config.TRANSLATE_PROMPT_LANGUAGE
                )
            
            self.SysLogger.save_prompt(Prompt)
            self.SysLogger.init_record()
            self.save_record()
        
    def get_record(self):
        with open("record.json", "r", encoding="utf-8") as f:
            record = json.load(f)
            #进度
            self.novel_path=record["novel_path"]

    def save_record(self):
        with open("record.json", "r", encoding="utf-8") as f:
            record = json.load(f)
        record["novel_path"]=self.SysLogger.LogDirPrefix
        self.SysLogger.Log(f"record:{record}",5)
        with open("record.json", "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=4)


    def choice_to_continue(self):
        while True:
            self.choice=input("Do you want to continue with the last novel? (y/n)")
            if self.choice=="y":

                self.get_record()              
                break
            elif self.choice=="n":
                break
            else:
                print("Invalid input! Please enter 'y' or 'n'.")
        
        #生成小说的完整步骤
        self.init()
        self.GenerateOutline()
        self.GeneratePerChapterOutline()
        self.WriteChapters()
        self.EditNovel()
        self.GenerateInfo()

  


    # Generate the Outline   1
    def GenerateOutline(self):
        """
        第一步，无须读取已有小说参数，生成大纲
    修改的参数 Outline,Elements,RoughChapterOutline,BaseContext,NumChapters
        """

        if self.choice=="y":
            self.SysLogger.Log("读取step1已有小说参数", 5)

            self.Outline, self.Elements, self.RoughChapterOutline, self.BaseContext,self.NumChapters=self.SysLogger.get_step1()
            
            self.BasePrompt = self.Prompt
            return
        

        self.SysLogger.Log("生成大纲", 5)
        self.Outline, self.Elements, self.RoughChapterOutline, self.BaseContext = Writer.OutlineGenerator.GenerateOutline(
            self.Interface, self.SysLogger, self.Prompt, Writer.Config.OUTLINE_QUALITY
        )
        self.BasePrompt = self.Prompt


        # Detect the number of chapters
        # SysLogger.Log("Detecting Chapters", 5)
        self.SysLogger.Log("检测章节", 5)
        Messages = [self.Interface.BuildUserQuery(self.Outline)]
        self.NumChapters = Writer.Chapter.ChapterDetector.LLMCountChapters(
            self.Interface, self.SysLogger, self.Interface.GetLastMessageText(Messages)
        )
        self.SysLogger.Log(f"检测到 {self.NumChapters} 章", 5)
        self.SysLogger.save_step1(self.Outline, self.Elements, self.RoughChapterOutline, self.BaseContext,self.NumChapters)


    # 2
    ## Write Per-Chapter Outline
    def GeneratePerChapterOutline(self):
        """
    用到的参数 Outline 
    修改的参数 ChapterOutlines,MegaOutline,DetailedOutline,UsedOutline
        """

        Prompt = f"""
        Please help me expand upon the following outline, chapter by chapter.

        ```
        {self.Outline}
        ```
            
        """
        Messages = [self.Interface.BuildUserQuery(Prompt)]

        if self.choice=="y":
            self.SysLogger.Log("读取step2已有小说参数", 5)

            ChapterOutlines: list = self.SysLogger.get_step2(self.done_chapter_outlines)
            if Writer.Config.EXPAND_OUTLINE:
                for Chapter in range(self.done_chapter_outlines+1, self.NumChapters+1):
                    ChapterOutline, Messages = Writer.OutlineGenerator.GeneratePerChapterOutline(
                        self.Interface, self.SysLogger, Chapter, self.Outline, Messages
                    )
                    ChapterOutlines.append(ChapterOutline)
                    self.done_chapter_outlines+=1 
                    self.SysLogger.save_step2(self.done_chapter_outlines,ChapterOutlines)
        else:
          
            ChapterOutlines: list = []
            if Writer.Config.EXPAND_OUTLINE:
        # 注意，range的第二个参数是不包括的  例如，range(1,4)  输出[1,2,3]  所以加一
                for Chapter in range(1, self.NumChapters + 1):
                    self.SysLogger.Log(f"生成第 {Chapter} 章的大纲", 5)
                    ChapterOutline, Messages = Writer.OutlineGenerator.GeneratePerChapterOutline(
                        self.Interface, self.SysLogger, Chapter, self.Outline, Messages
                    )
                    ChapterOutlines.append(ChapterOutline)
                    self.done_chapter_outlines+=1        
                    self.SysLogger.save_step2(self.done_chapter_outlines,ChapterOutlines)


      


        # Create MegaOutline
        self.DetailedOutline: str = ""
        for Chapter in ChapterOutlines:
            self.DetailedOutline += Chapter
        self.MegaOutline: str = f"""

        # Base Outline
        {self.Elements}

        # Detailed Outline
        {self.DetailedOutline}

        """

        #为了生成每章的大纲，创建基础提示
        self.UsedOutline = self.Outline
        if Writer.Config.EXPAND_OUTLINE:
            self.UsedOutline = self.MegaOutline



    # Write the chapters  3
    def WriteChapters(self):
        """
    用到的参数 Outline  NumChapters  BaseContext  Chapters
    修改的参数 Chapters 
        """

        if self.choice=="y":
            self.SysLogger.Log("读取step3已有小说参数", 5)
            #输入已有小说章节数和全部章节数
            self.Chapters=self.SysLogger.get_step3(self.done_chapters,self.chapter_num)
            
        # 注意，range的第二个参数是不包括的  例如，range(1,4)  输出[1,2,3]  所以加一
            for i in range(self.done_chapters+1, self.NumChapters+1):
                Chapter = Writer.Chapter.ChapterGenerator.GenerateChapter(
                    self.Interface,
                    self.SysLogger,
                    i,
                    self.NumChapters,
                    self.Outline,
                    self.Chapters,
                    Writer.Config.OUTLINE_QUALITY,
                    self.BaseContext,   #上下文
                )

                Chapter = f"### Chapter {i}\n\n{Chapter}"
                self.Chapters.append(Chapter)
                ChapterWordCount = Writer.Statistics.GetWordCount(Chapter)
                # SysLogger.Log(f"Chapter Word Count: {ChapterWordCount}", 2)
                self.SysLogger.Log(f"章节字数: {ChapterWordCount}", 2)
                self.done_chapters+=1
                self.SysLogger.save_step3(self.done_chapters,chapters=Chapter)
            return 
        
        self.SysLogger.Log("开始写章节", 5)
        self.Chapters = []
        self.done_chapters=0
        # 注意，range的第二个参数是不包括的  例如，range(1,4)  输出[1,2,3]  所以加一
        for i in range(1, self.NumChapters+1):

            Chapter = Writer.Chapter.ChapterGenerator.GenerateChapter(
                self.Interface,
                self.SysLogger,
                i,
                self.NumChapters,
                self.Outline,
                self.Chapters,
                Writer.Config.OUTLINE_QUALITY,
                self.BaseContext,   #上下文
            )

            Chapter = f"### Chapter {i}\n\n{Chapter}"
            self.Chapters.append(Chapter)
            ChapterWordCount = Writer.Statistics.GetWordCount(Chapter)
            # SysLogger.Log(f"Chapter Word Count: {ChapterWordCount}", 2)
            self.SysLogger.Log(f"章节字数: {ChapterWordCount}", 2)
            self.done_chapters+=1
            self.SysLogger.save_step3(self.done_chapters,self.Chapters)

    def translate_novel(self):
        # If enabled, translate the novel
        if Writer.Config.TRANSLATE_LANGUAGE != "":
            self.NewChapters = Writer.Translator.TranslateNovel(
                self.Interface, self.SysLogger, self.NewChapters, self.NumChapters, Writer.Config.TRANSLATE_LANGUAGE
            )
        else:
            # SysLogger.Log(f"No Novel Translation Requested, Skipping Translation Step", 4)
            self.SysLogger.Log(f"未请求小说翻译，跳过翻译步骤", 4)
        self.StoryInfoJSON.update({"TranslatedChapters": self.NewChapters})

         # Compile The Story
        for Chapter in self.NewChapters:
            self.StoryBodyText += Chapter + "\n\n\n"




    # Now edit the whole thing together   4
    def EditNovel(self):
        """
    用到的参数 Outline Elements RoughChapterOutline BaseContext NumChapters Chapters
    修改的参数 StoryInfoJSON,StoryBodyText   NewChapters 是中间参数 不会在后面步骤用到 不用保存
        """

        if self.choice=="y":
            self.SysLogger.Log("读取step4已有小说参数", 5)
            self.StoryInfoJSON,self.StoryBodyText=self.SysLogger.get_step4()
        else:
            self.StoryBodyText=""
            self.StoryInfoJSON:dict={}
        
       
        self.SysLogger.Log("整合章节", 5)

        if self.StoryInfoJSON=={}:

            StoryInfoJSON:dict = {"Outline": self.Outline}
            StoryInfoJSON.update({"StoryElements": self.Elements})
            StoryInfoJSON.update({"RoughChapterOutline": self.RoughChapterOutline})
            StoryInfoJSON.update({"BaseContext": self.BaseContext})

            if Writer.Config.ENABLE_FINAL_EDIT_PASS:
                self.NewChapters = Writer.NovelEditor.EditNovel(
                    self.Interface, self.SysLogger, self.Chapters, self.Outline, len(self.Chapters)
                )
            else:
                self.NewChapters = self.Chapters
            StoryInfoJSON.update({"UnscrubbedChapters": self.NewChapters})

            # Now scrub it (if enabled)
            if not Writer.Config.SCRUB_NO_SCRUB:
                self.NewChapters = Writer.Scrubber.ScrubNovel(
                    self.Interface, self.SysLogger, self.NewChapters, len(self.NewChapters)
                )
            else:
                # SysLogger.Log(f"Skipping Scrubbing Due To Config", 4)
                self.SysLogger.Log(f"由于配置，跳过清理", 4)
            StoryInfoJSON.update({"ScrubbedChapter": self.NewChapters})

            self.StoryInfoJSON=StoryInfoJSON
           
            self.translate_novel()

            self.SysLogger.save_step4(self.StoryBodyText, self.StoryInfoJSON)

      

    # Now Generate Info 5
    def GenerateInfo(self):
        """
    用到的参数 Outline BasePrompt StoryInfoJSON StoryBodyText
        """
        self.SysLogger.Log("生成信息", 5)
        Messages = []
        Messages.append(self.Interface.BuildUserQuery(self.Outline))
        Info = Writer.StoryInfo.GetStoryInfo(self.Interface, self.SysLogger, Messages)
        Title = Info["Title"]
        self.StoryInfoJSON.update({"Title": Info["Title"]})
        Summary = Info["Summary"]
        self.StoryInfoJSON.update({"Summary": Info["Summary"]})
        Tags = Info["Tags"]
        self.StoryInfoJSON.update({"Tags": Info["Tags"]})

        print("---------------------------------------------")
        print(f"Story Title: {Title}")
        print(f"Summary: {Summary}")
        print(f"Tags: {Tags}")
        print("---------------------------------------------")

        ElapsedTime = time.time() - StartTime


        # Calculate Total Words
        TotalWords: int = Writer.Statistics.GetWordCount(self.StoryBodyText)
        self.SysLogger.Log(f"Story Total Word Count: {TotalWords}", 4)

        StatsString: str = "Work Statistics:  \n"
        StatsString += " - Total Words: " + str(TotalWords) + "  \n"
        StatsString += f" - Title: {Title}  \n"
        StatsString += f" - Summary: {Summary}  \n"
        StatsString += f" - Tags: {Tags}  \n"
        StatsString += f" - Generation Start Date: {datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}  \n"
        StatsString += f" - Generation Total Time: {ElapsedTime}s  \n"
        StatsString += f" - Generation Average WPM: {60 * (TotalWords/ElapsedTime)}  \n"

        StatsString += "\n\nUser Settings:  \n"
        StatsString += f" - Base Prompt: {self.BasePrompt}  \n"

        StatsString += "\n\nGeneration Settings:  \n"
        StatsString += f" - Generator: AIStoryGenerator_2024-06-27  \n"
        StatsString += (
            f" - Base Outline Writer Model: {Writer.Config.INITIAL_OUTLINE_WRITER_MODEL}  \n"
        )
        StatsString += (
            f" - Chapter Outline Writer Model: {Writer.Config.CHAPTER_OUTLINE_WRITER_MODEL}  \n"
        )
        StatsString += f" - Chapter Writer (Stage 1: Plot) Model: {Writer.Config.CHAPTER_STAGE1_WRITER_MODEL}  \n"
        StatsString += f" - Chapter Writer (Stage 2: Char Development) Model: {Writer.Config.CHAPTER_STAGE2_WRITER_MODEL}  \n"
        StatsString += f" - Chapter Writer (Stage 3: Dialogue) Model: {Writer.Config.CHAPTER_STAGE3_WRITER_MODEL}  \n"
        StatsString += f" - Chapter Writer (Stage 4: Final Pass) Model: {Writer.Config.CHAPTER_STAGE4_WRITER_MODEL}  \n"
        StatsString += f" - Chapter Writer (Revision) Model: {Writer.Config.CHAPTER_REVISION_WRITER_MODEL}  \n"
        StatsString += f" - Revision Model: {Writer.Config.REVISION_MODEL}  \n"
        StatsString += f" - Eval Model: {Writer.Config.EVAL_MODEL}  \n"
        StatsString += f" - Info Model: {Writer.Config.INFO_MODEL}  \n"
        StatsString += f" - Scrub Model: {Writer.Config.SCRUB_MODEL}  \n"
        StatsString += f" - Seed: {Writer.Config.SEED}  \n"
        # StatsString += f" - Outline Quality: {Writer.Config.OUTLINE_QUALITY}  \n"
        StatsString += f" - Outline Min Revisions: {Writer.Config.OUTLINE_MIN_REVISIONS}  \n"
        StatsString += f" - Outline Max Revisions: {Writer.Config.OUTLINE_MAX_REVISIONS}  \n"
        # StatsString += f" - Chapter Quality: {Writer.Config.CHAPTER_QUALITY}  \n"
        StatsString += f" - Chapter Min Revisions: {Writer.Config.CHAPTER_MIN_REVISIONS}  \n"
        StatsString += f" - Chapter Max Revisions: {Writer.Config.CHAPTER_MAX_REVISIONS}  \n"
        StatsString += f" - Chapter Disable Revisions: {Writer.Config.CHAPTER_NO_REVISIONS}  \n"
        StatsString += f" - Disable Scrubbing: {Writer.Config.SCRUB_NO_SCRUB}  \n"


        # Save The Story To Disk
        # SysLogger.Log("Saving Story To Disk", 3)
        self.SysLogger.Log("保存小说到磁盘", 3)
        os.makedirs("Stories", exist_ok=True)
        FName = f"Stories/Story_{Title.replace(' ', '_')}"
        if Writer.Config.OPTIONAL_OUTPUT_NAME != "":
            FName = Writer.Config.OPTIONAL_OUTPUT_NAME

        with open(f"{FName}.md", "w", encoding="utf-8") as F:
            Out = f"""
        {StatsString}

        ---

        Note: An outline of the story is available at the bottom of this document.
        Please scroll to the bottom if you wish to read that.

        ---
        # {Title}

        {self.StoryBodyText}


        ---
        # Outline
        ```
        {self.Outline}
        ```
        """
            self.SysLogger.SaveStory(Out)
            F.write(Out)

        # Save JSON
        with open(f"{FName}.json", "w", encoding="utf-8") as F:
            F.write(json.dumps(self.StoryInfoJSON, indent=4))



#主函数
if __name__ == "__main__":
    StartTime = time.time()
    AIStoryWriter = NovelWriter()
    AIStoryWriter.choice_to_continue()