import Writer.Config
import json


def GetStoryInfo(Interface, _Logger, _Messages: list):

<<<<<<< HEAD
    # 定义提示词
    Prompt: str = Writer.Prompts.STATS_PROMPT

    # 记录日志，提示LLM生成统计数据
    _Logger.Log("Prompting LLM To Generate Stats", 5)
    # 将用户查询添加到消息列表中
    Messages = _Messages
    Messages.append(Interface.BuildUserQuery(Prompt))
    # 使用安全生成文本方法生成文本
    Messages = Interface.SafeGenerateText(
        _Logger, Messages, Writer.Config.INFO_MODEL, _Format="json"
    )
    # 记录日志，完成获取统计数据反馈
    _Logger.Log("Finished Getting Stats Feedback", 5)

    # 初始化迭代次数
    Iters: int = 0
    while True:

        # 获取最后一条消息的文本
        RawResponse = Interface.GetLastMessageText(Messages)
        # 替换文本中的反引号和json关键字
=======
    Prompt: str = Writer.Prompts.STATS_PROMPT

    _Logger.Log("Prompting LLM To Generate Stats", 5)
    Messages = _Messages
    Messages.append(Interface.BuildUserQuery(Prompt))
    Messages = Interface.SafeGenerateText(
        _Logger, Messages, Writer.Config.INFO_MODEL, _Format="json"
    )
    _Logger.Log("Finished Getting Stats Feedback", 5)

    Iters: int = 0
    while True:

        RawResponse = Interface.GetLastMessageText(Messages)
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
        RawResponse = RawResponse.replace("`", "")
        RawResponse = RawResponse.replace("json", "")

        try:
<<<<<<< HEAD
            # 每次迭代增加一次
            Iters += 1
            # 将文本解析为字典
            Dict = json.loads(RawResponse)
            # 返回字典
            return Dict
        except Exception as E:
            # 如果迭代次数超过4次，记录错误日志并返回空字典
            if Iters > 4:
                _Logger.Log("Critical Error Parsing JSON", 7)
                return {}
            # 记录错误日志，提示LLM解析JSON时出错，并要求修改
            _Logger.Log("Error Parsing JSON Written By LLM, Asking For Edits", 7)
            # 定义修改提示词
            EditPrompt: str = (
                f"Please revise your JSON. It encountered the following error during parsing: {E}. Remember that your entire response is plugged directly into a JSON parser, so don't write **anything** except pure json."
            )
            # 将修改提示词添加到消息列表中
            Messages.append(Interface.BuildUserQuery(EditPrompt))
            # 记录日志，提示LLM修改
            _Logger.Log("Asking LLM TO Revise", 7)
            # 使用安全生成文本方法生成修改后的文本
            Messages = Interface.SafeGenerateText(
                _Logger, Messages, Writer.Config.INFO_MODEL, _Format="json"
            )
            # 记录日志，完成修改
=======
            Iters += 1
            Dict = json.loads(RawResponse)
            return Dict
        except Exception as E:
            if Iters > 4:
                _Logger.Log("Critical Error Parsing JSON", 7)
                return {}
            _Logger.Log("Error Parsing JSON Written By LLM, Asking For Edits", 7)
            EditPrompt: str = (
                f"Please revise your JSON. It encountered the following error during parsing: {E}. Remember that your entire response is plugged directly into a JSON parser, so don't write **anything** except pure json."
            )
            Messages.append(Interface.BuildUserQuery(EditPrompt))
            _Logger.Log("Asking LLM TO Revise", 7)
            Messages = Interface.SafeGenerateText(
                _Logger, Messages, Writer.Config.INFO_MODEL, _Format="json"
            )
>>>>>>> 25d675377e82f0bd0308ed630ebf25b2b7b41e16
            _Logger.Log("Done Asking LLM TO Revise JSON", 6)
