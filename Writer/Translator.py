import Writer.Logger
import Writer.Config
import Writer.Prompts


#输出中文提示  方便查看效果   前往prompt中改成翻译为中文  ctrl+f搜索  TRANSLATE_PROMPT
#另外，由于英语和汉语的差异，同样的意思，英语空格数会比中文多很多 默认的最低输出限制需要修改。  ctrl+f搜索  _MinWordCount   
#比如，将200改为100  不太好掌控
#也可以将根据空格识别单词数 改为 识别字数 


# 定义一个名为TranslatePrompt的函数，该函数接受四个参数：Interface，_Logger，_Prompt和_Language
def TranslatePrompt(Interface, _Logger, _Prompt: str, _Language: str = "chinese"):

    Prompt: str = Writer.Prompts.TRANSLATE_PROMPT.format(
        _Prompt=_Prompt, _Language=_Language
    )
    _Logger.Log(f"Prompting LLM To Translate User Prompt", 5)
    Messages = []
    Messages.append(Interface.BuildUserQuery(Prompt))
    Messages = Interface.SafeGenerateText(
        _Logger, Messages, Writer.Config.TRANSLATOR_MODEL, _MinWordCount=50
    )
    _Logger.Log(f"Finished Prompt Translation", 5)

    return Interface.GetLastMessageText(Messages)


def TranslateNovel(
    Interface, _Logger, _Chapters: list, _TotalChapters: int, _Language: str = "chinese"
):

    EditedChapters = _Chapters

    for i in range(_TotalChapters):

        Prompt: str = Writer.Prompts.CHAPTER_TRANSLATE_PROMPT.format(
            _Chapter=EditedChapters[i], _Language=_Language
        )
        _Logger.Log(f"Prompting LLM To Perform Chapter {i+1} Translation", 5)
        Messages = []
        Messages.append(Interface.BuildUserQuery(Prompt))
        Messages = Interface.SafeGenerateText(
            _Logger, Messages, Writer.Config.TRANSLATOR_MODEL
        )
        _Logger.Log(f"Finished Chapter {i+1} Translation", 5)

        NewChapter = Interface.GetLastMessageText(Messages)
        EditedChapters[i] = NewChapter
        ChapterWordCount = Writer.Statistics.GetWordCount(NewChapter)
        _Logger.Log(f"Translation Chapter Word Count: {ChapterWordCount}", 3)

    return EditedChapters
