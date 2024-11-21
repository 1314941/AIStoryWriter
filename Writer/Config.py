INITIAL_OUTLINE_WRITER_MODEL = (
    "ollama://novel:latest"  # Note this value is overridden by the argparser
)
CHAPTER_OUTLINE_WRITER_MODEL = (
    "ollama://novel:latest"  # Note this value is overridden by the argparser
)
CHAPTER_STAGE1_WRITER_MODEL = "ollama://novel:latest"  # Note this value is overridden by the argparser
CHAPTER_STAGE2_WRITER_MODEL = "ollama://novel:latest"  # Note this value is overridden by the argparser
CHAPTER_STAGE3_WRITER_MODEL = "ollama://novel:latest"  # Note this value is overridden by the argparser
CHAPTER_STAGE4_WRITER_MODEL = "ollama://novel:latest"  # Note this value is overridden by the argparser
CHAPTER_REVISION_WRITER_MODEL = (
    "ollama://novel:latest"  # Note this value is overridden by the argparser
)
REVISION_MODEL = "ollama://novel:latest"  # Note this value is overridden by the argparser
EVAL_MODEL = "ollama://novel:latest"  # Note this value is overridden by the argparser
INFO_MODEL = "ollama://novel:latest"  # Note this value is overridden by the argparser
SCRUB_MODEL = "ollama://novel:latest"  # Note this value is overridden by the argparser
CHECKER_MODEL = "ollama://novel:latest"  # Model used to check results
TRANSLATOR_MODEL = "ollama://novel:latest"

#翻译为中文

OLLAMA_CTX = 8192  # OLLAMA上下文大小

OLLAMA_HOST = "127.0.0.1:11434"  # OLLAMA主机地址

SEED = 12  # Note this value is overridden by the argparser

TRANSLATE_LANGUAGE = "chinese"  # If the user wants to translate, this'll be changed from empty to a language e.g 'French' or 'Russian'
TRANSLATE_PROMPT_LANGUAGE = "chinese"  # If the user wants to translate their prompt, this'll be changed from empty to a language e.g 'French' or 'Russian'


# 定义一系列的配置参数，用于控制程序或模块的行为
OUTLINE_QUALITY = 87  # 大纲的质量标准，默认值为87
OUTLINE_MIN_REVISIONS = 0  # 大纲的最小修订次数，默认值为0
OUTLINE_MAX_REVISIONS = 3  # 大纲的最大修订次数，默认值为3
CHAPTER_NO_REVISIONS = False  # 是否禁用章节的修订检查，默认值为True
CHAPTER_QUALITY = 85  # 章节的质量标准，默认值为85
CHAPTER_MIN_REVISIONS = 1  # 章节的最小修订次数，默认值为1
CHAPTER_MAX_REVISIONS = 3  # 章节的最大修订次数，默认值为3
SCRUB_NO_SCRUB = True  # 是否进行清理操作，默认值为False
EXPAND_OUTLINE = True  # 是否扩展大纲，默认值为False
ENABLE_FINAL_EDIT_PASS = True  # 是否启用最终编辑轮次，默认值为False
SCENE_GENERATION_PIPELINE = True  # 是否启用场景生成管道，默认值为True
OPTIONAL_OUTPUT_NAME = ""  # 可选的输出文件名，默认值为空字符串
DEBUG = False  # 是否启用调试模式，默认值为False




def save_config(config_file):
    import json

    # 配置参数
    config = {
        "INITIAL_OUTLINE_WRITER_MODEL": INITIAL_OUTLINE_WRITER_MODEL,
        "CHAPTER_OUTLINE_WRITER_MODEL": CHAPTER_OUTLINE_WRITER_MODEL,
        "CHAPTER_STAGE1_WRITER_MODEL": CHAPTER_STAGE1_WRITER_MODEL,
        "CHAPTER_STAGE2_WRITER_MODEL": CHAPTER_STAGE2_WRITER_MODEL,
        "CHAPTER_STAGE3_WRITER_MODEL": CHAPTER_STAGE3_WRITER_MODEL,
        "CHAPTER_STAGE4_WRITER_MODEL": CHAPTER_STAGE4_WRITER_MODEL,
        "CHAPTER_REVISION_WRITER_MODEL": CHAPTER_REVISION_WRITER_MODEL,
        "REVISION_MODEL": REVISION_MODEL,
        "EVAL_MODEL": EVAL_MODEL,
        "INFO_MODEL": INFO_MODEL,
        "SCRUB_MODEL": SCRUB_MODEL,
        "CHECKER_MODEL": CHECKER_MODEL,
        "TRANSLATOR_MODEL": TRANSLATOR_MODEL,
        "OLLAMA_CTX": OLLAMA_CTX,
        "OLLAMA_HOST": OLLAMA_HOST,
        "SEED": SEED,
        "TRANSLATE_LANGUAGE": TRANSLATE_LANGUAGE,
        "TRANSLATE_PROMPT_LANGUAGE": TRANSLATE_PROMPT_LANGUAGE,
        "OUTLINE_QUALITY": OUTLINE_QUALITY,
        "OUTLINE_MIN_REVISIONS": OUTLINE_MIN_REVISIONS,
        "OUTLINE_MAX_REVISIONS": OUTLINE_MAX_REVISIONS,
        "CHAPTER_NO_REVISIONS": CHAPTER_NO_REVISIONS,
        "CHAPTER_QUALITY": CHAPTER_QUALITY,
        "CHAPTER_MIN_REVISIONS": CHAPTER_MIN_REVISIONS,
        "CHAPTER_MAX_REVISIONS": CHAPTER_MAX_REVISIONS,
        "SCRUB_NO_SCRUB": SCRUB_NO_SCRUB,
        "EXPAND_OUTLINE": EXPAND_OUTLINE,
        "ENABLE_FINAL_EDIT_PASS": ENABLE_FINAL_EDIT_PASS,
        "SCENE_GENERATION_PIPELINE": SCENE_GENERATION_PIPELINE,
        "OPTIONAL_OUTPUT_NAME": OPTIONAL_OUTPUT_NAME,
        "DEBUG": DEBUG
    }

    # 将配置保存为JSON文件
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

    print("配置已保存到 {config_file}")












# Tested models:
# "llama3:70b"  # works as editor model, DO NOT use as writer model, it sucks
# "vanilj/midnight-miqu-70b-v1.5"  # works rather well as the writer, not well as anything else
# "command-r"
# "qwen:72b"
# "command-r-plus"
# "nous-hermes2"  # not big enough to really do a good job - do not use
# "dbrx"  # sucks - do not use


