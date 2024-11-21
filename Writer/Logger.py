import termcolor
import datetime
import os
import json


def PrintMessageHistory(_Messages):
    print("------------------------------------------------------------")
    for Message in _Messages:
        print(Message)
    print("------------------------------------------------------------")


class Logger:

    def __init__(self,last_novel_path:str="", _LogfilePrefix="Logs"):

        # Make Paths For Log
        if last_novel_path=="":
            LogDirPath = _LogfilePrefix + "/Generation_" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            os.makedirs(LogDirPath + "/LangchainDebug", exist_ok=True)
        else:
            LogDirPath = last_novel_path

        # Setup Log Path
        self.LogDirPrefix = LogDirPath
        self.LogPath = LogDirPath + "/Main.log"
        self.File = open(self.LogPath, "a",encoding="utf-8")
        self.LangchainID = 0

        self.recordPath=LogDirPath + "/record.json"

        self.count=1;
        os.makedirs(LogDirPath + "/chapter", exist_ok=True)
        os.makedirs(LogDirPath + "/chapter_outline", exist_ok=True)
        self.chapter_path=LogDirPath + f"/chapter/{self.count}.md"
        self.chapter_outline_path=LogDirPath + f"/chapter_outline/{self.count}.md"

        self.prompt_path=LogDirPath + "/prompt.md"

        self.Outline_path=LogDirPath + "/outline.md"
        self.Elements_path=LogDirPath + "/elements.md"
        self.RoughChapterOutline_path=LogDirPath + "/rough_chapter_outline.md"
        
        self.BaseContext_path=LogDirPath + "/base_context.md"
        self.BasePrompt_path=LogDirPath + "/basePrompt.md"

        self.StoryBodytext_path=LogDirPath + "/storyBodyText.md"
        self.StoryInfoJSON_path=LogDirPath + "/storyInfo.json"



        self.LogItems = []


    # Helper function that saves the entire language chain object as both json and markdown for debugging later
    def SaveLangchain(self, _LangChainID:str, _LangChain:list):

        # Calculate Filepath For This Langchain
        # ThisLogPathJSON:str = self.LogDirPrefix + f"/LangchainDebug/{self.LangchainID}_{_LangChainID}.json"
        # ThisLogPathMD:str = self.LogDirPrefix + f"/LangchainDebug/{self.LangchainID}_{_LangChainID}.md"
        # LangChainDebugTitle:str = f"{self.LangchainID}_{_LangChainID}"
        # self.LangchainID += 1

        # # Generate and Save JSON Version
        # with open(ThisLogPathJSON, "w",encoding="utf-8") as f:
        #     f.write(json.dumps(_LangChain, indent=4, sort_keys=True))
        
        # # Now, Save Markdown Version
        # with open(ThisLogPathMD, "w",encoding="utf-8") as f:
        #     MarkdownVersion:str = f"# Debug LangChain {LangChainDebugTitle}\n**Note: '```' tags have been removed in this version.**\n"
        #     for Message in _LangChain:
        #         MarkdownVersion += f"\n\n\n# Role: {Message['role']}\n"
        #         MarkdownVersion += f"```{Message['content'].replace('```', '')}```"
        #     f.write(MarkdownVersion)
        
        # self.Log(f"Wrote This Language Chain ({LangChainDebugTitle}) To Debug File {ThisLogPathMD}", 5)

        pass
    


    def get_record(self):
        with open(self.recordPath, "r", encoding="utf-8") as f:
            novel_config = json.load(f)
        self.step=novel_config["step"]
        self.done_chapter_outlines=novel_config["done_chapter_outlines"]
        self.done_chapters=novel_config["done_chapters"]
        self.chapter_num=novel_config["chapter_num"]
        return self.step,self.done_chapter_outlines,self.done_chapters,self.chapter_num

    def init_record(self):
        data={
            "step":0,
            "done_chapter_outlines":0,
            "done_chapters":0,
            "chapter_num":0
        }
        with open(self.recordPath,"w",encoding="utf-8") as f:
            json.dump(data,f,indent=4)
        return

    def update_record(self,done_chapters:int=-1,step:int=-1,done_chapter_outlines:int=-1,chapter_num:int=-1):
        with open(self.recordPath,"r",encoding="utf-8") as f:
            record=json.load(f)
        if done_chapters!=-1:
            record["done_chapters"]=done_chapters
        if step!=-1:
            record["step"]=step
        if done_chapter_outlines!=-1:
            record["done_chapter_outlines"]=done_chapter_outlines
        if chapter_num!=-1:
            record["chapter_num"]=chapter_num
        with open(self.recordPath,"w",encoding="utf-8") as f:
            json.dump(record,f,ensure_ascii=False,indent=4)




    def get_prompt(self):
        with open(self.prompt_path,"r",encoding="utf-8") as f:
            base_prompt=f.read()
        return base_prompt

    def save_prompt(self,base_prompt:str):
        with open(self.prompt_path,"w",encoding="utf-8") as f:
            f.write(base_prompt)
        return



    def save_step1(self,outline:str,elements:str,rough_chapter_outline:str,base_context:str,chapter_num:int):
        with open(self.Outline_path,"w",encoding="utf-8") as f:
            f.write(outline)
        with open(self.Elements_path,"w",encoding="utf-8") as f:
            f.write(elements)
        with open(self.RoughChapterOutline_path,"w",encoding="utf-8") as f:
            f.write(rough_chapter_outline)
        with open(self.BaseContext_path,"w",encoding="utf-8") as f:
            f.write(base_context)

        self.update_record(step=1,chapter_num=chapter_num)
        return
    
   
    def get_step1(self):
        with open(self.Outline_path,"r",encoding="utf-8") as f:
            outline=f.read()
        with open(self.Elements_path,"r",encoding="utf-8") as f:
            elements=f.read()
        with open(self.RoughChapterOutline_path,"r",encoding="utf-8") as f:
            rough_chapter_outline=f.read()
        with open(self.BaseContext_path,"r",encoding="utf-8") as f:
            base_context=f.read()
        with open(self.recordPath,"r",encoding="utf-8") as f:
            #json
            record=json.load(f)
            chapter_num=record["chapter_num"]
        return outline,elements,rough_chapter_outline,base_context,chapter_num


    def save_step2(self,done_chapters,chapters:list):
        self.chapter_path=f"chapter_outline/{done_chapters}.txt"
        self.chapter_path=self.LogDirPrefix + f"/{self.chapter_path}"
        with open(self.chapter_path,"a",encoding="utf-8") as f:
            f.write(chapters[done_chapters-1])
        self.update_record(step=2,done_chapter_outlines=done_chapters)
        return


    def get_step2(self,done_chapters):
        chapters=[]
        # 注意，range的第二个参数是不包括的  例如，range(1,4)  输出[1,2,3]  所以加一
        for i in range(1,done_chapters+1):
            self.chapter_path=f"chapter_outline/{i}.txt"
            self.chapter_path=self.LogDirPrefix + f"/{self.chapter_path}"
            with open(self.chapter_path,"r",encoding="utf-8") as f:
                chapter_content=f.read()
                chapters.append(chapter_content)
        return chapters


 
    #每次保存一章
    def save_step3(self,done_chapters:int,chapters:str):
        self.chapter_path=f"chapter/{done_chapters}.md"
        self.chapter_path=self.LogDirPrefix + f"/{self.chapter_path}"
        with open(self.chapter_path,"w",encoding="utf-8") as f:
            f.write(chapters)
        self.update_record(step=3,done_chapters=done_chapters)
        return


    def get_step3(self,done_chapters,chapter_num):
        chapters=[]
        for i in range(1,done_chapters+1):
            self.chapter_path=f"chapter/{i}.md"
            self.chapter_path=self.LogDirPrefix + f"/{self.chapter_path}"
            with open(self.chapter_path,"r",encoding="utf-8") as f:
                chapter_content=f.read()
                chapters.append(chapter_content)
        return chapters



    def save_step4(self,StoryBodyText, StoryInfoJSON):
        with open(self.StoryBodytext_path,"w",encoding="utf-8") as f:
            f.write(StoryBodyText)
        with open(self.StoryInfoJSON_path,"w",encoding="utf-8") as f:
            f.write(json.dumps(StoryInfoJSON,indent=4))
        self.update_record(step=4)

    def get_step4(self)->str:
        StoryBodyText=""
        StoryInfoJSON={}
        if os.path.exists(self.StoryBodytext_path):
            with open(self.StoryBodytext_path,"r",encoding="utf-8") as f:
                StoryBodyText=f.read()
        if os.path.exists(self.StoryInfoJSON_path):
            with open(self.StoryInfoJSON_path,"r",encoding="utf-8") as f:
                StoryInfoJSON=json.load(f)
        return StoryInfoJSON,StoryBodyText






  
    # Saves the given story to disk
    def SaveStory(self, _StoryContent:str):

        with open(f"{self.LogDirPrefix}/Story.md", "w",encoding="utf-8") as f:
            f.write(_StoryContent)

        self.Log(f"Wrote Story To Disk At {self.LogDirPrefix}/Story.md", 5)


    # Logs an item
    def Log(self, _Item, _Level:int):

        # Create Log Entry
        LogEntry = f"[{str(_Level).ljust(2)}] [{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}] {_Item}"

        # Write it to file
        self.File.write(LogEntry + "\n")
        self.LogItems.append(LogEntry)

        # Now color and print it
        if (_Level == 0):
            LogEntry = termcolor.colored(LogEntry, "white")
        elif (_Level == 1):
            LogEntry = termcolor.colored(LogEntry, "grey")
        elif (_Level == 2):
            LogEntry = termcolor.colored(LogEntry, "blue")
        elif (_Level == 3):
            LogEntry = termcolor.colored(LogEntry, "cyan")
        elif (_Level == 4):
            LogEntry = termcolor.colored(LogEntry, "magenta")
        elif (_Level == 5):
            LogEntry = termcolor.colored(LogEntry, "green")
        elif (_Level == 6):
            LogEntry = termcolor.colored(LogEntry, "yellow")
        elif (_Level == 7):
            LogEntry = termcolor.colored(LogEntry, "red")

        print(LogEntry)



    def __del__(self):
        self.File.close()