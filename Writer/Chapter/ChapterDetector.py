import Writer.Config
import Writer.Prompts

import re
import json


def LLMCountChapters(Interface, _Logger, _Summary):

    # 格式化提示信息
    Prompt = Writer.Prompts.CHAPTER_COUNT_PROMPT.format(_Summary=_Summary)

    # 记录日志，提示LLM获取章节数量JSON
    # _Logger.Log("Prompting LLM To Get ChapterCount JSON", 5)
    _Logger.Log("提示LLM以获取章节数量JSON", 5)
    Messages = []
    # 构建用户查询
    Messages.append(Interface.BuildUserQuery(Prompt))
    # 调用SafeGenerateText方法，获取LLM生成的文本
    Messages = Interface.SafeGenerateText(
        _Logger, Messages, Writer.Config.EVAL_MODEL, _Format="json"
    )
    # 记录日志，完成获取章节数量JSON
    # _Logger.Log("Finished Getting ChapterCount JSON", 5)
    _Logger.Log("完成获取章节数量JSON", 5)

    Iters: int = 0

    while True:

        # 获取LLM生成的文本
        RawResponse = Interface.GetLastMessageText(Messages)
        # 去除文本中的反引号和json关键字
        RawResponse = RawResponse.replace("`", "")
        RawResponse = RawResponse.replace("json", "")

        try:
            # 计数器加1
            Iters += 1
            # 解析JSON，获取TotalChapters
            TotalChapters = json.loads(RawResponse)["TotalChapters"]
            # 记录日志，获取到总章节数量
            # _Logger.Log("Got Total Chapter Count At {TotalChapters}", 5)
            _Logger.Log(f"获取到总章节数量{TotalChapters}", 5)
            return TotalChapters
        except Exception as E:
            # 如果计数器大于4，记录日志，返回-1
            if Iters > 4:
                _Logger.Log("Critical Error Parsing JSON", 7)
                return -1
            # 记录日志，解析JSON出错，要求LLM进行修改
            # _Logger.Log("Error Parsing JSON Written By LLM, Asking For Edits", 7)
            _Logger.Log("LLM生成的JSON解析出错，请修改", 7)
            # 构建修改提示信息
            EditPrompt: str = (
                f"Please revise your JSON. It encountered the following error during parsing: {E}. Remember that your entire response is plugged directly into a JSON parser, so don't write **anything** except pure json."
            )
            # 构建用户查询
            Messages.append(Interface.BuildUserQuery(EditPrompt))
            # 记录日志，要求LLM进行修改
            # _Logger.Log("Asking LLM TO Revise", 7)
            _Logger.Log("要求LLM进行修改", 7)
            # 调用SafeGenerateText方法，获取LLM生成的文本
            Messages = Interface.SafeGenerateText(
                _Logger, Messages, Writer.Config.EVAL_MODEL, _Format="json"
            )
            # 记录日志，完成要求LLM进行修改
            # _Logger.Log("Done Asking LLM TO Revise JSON", 6)
            _Logger.Log("完成要求LLM进行修改JSON", 6)
