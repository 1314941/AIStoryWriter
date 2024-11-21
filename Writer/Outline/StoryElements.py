import Writer.Feedback
import Writer.Logger
import Writer.Config


def GenerateStoryElements(Interface, _Logger, _OutlinePrompt):

    # 定义一个字符串变量Prompt，用于存储故事元素的提示  不懂为何不放在Prompts.py里  
    Prompt: str = f"""
我正在编写一部虚构的故事，希望能得到你的帮助来构思故事元素。

这是我的故事提示。
<PROMPT>
{_OutlinePrompt}
</PROMPT>

请让你的回答遵循以下格式：

<RESPONSE_TEMPLATE>
# 故事标题

## 类型
- **类别**： (例如，浪漫，悬疑，科幻，奇幻，恐怖)

## 主题
- **中心思想或信息**：

## 情节发展
- **节奏**： (例如，缓慢，快速)

## 风格
- **语言运用**： (例如，句子结构，词汇，语气，比喻语言)

## 情节
- ** exposition**：
- **上升动作**：
- **高潮**：
- **下降动作**：
- **结局**：

## 场景
### 场景 1
- **时间**： (例如，现代，未来，过去)
- **地点**： (例如，城市，乡村，其他星球)
- **文化**： (例如，现代，中世纪，外星)
- **氛围**： (例如，阴暗，高科技，反乌托邦)

(重复上述结构以添加更多场景)

## 矛盾
- **类型**： (例如，内在，外在)
- **描述**：

## 符号
### 符号 1
- **符号**：
- **含义**：

(重复上述结构以添加更多符号)

## 角色
### 主角(s)
#### 主角 1
- **名字**：
- **外貌描述**：
- **个性**：
- **背景**：
- **动机**：

(重复上述结构以添加更多主角)

### 支持角色
#### 角色 1
- **名字**：
- **外貌描述**：
- **个性**：
- **背景**：
- **在故事中的角色**：

#### 角色 2
- **名字**：
- **外貌描述**：
- **个性**：
- **背景**：
- **在故事中的角色**：

#### 角色 3
- **名字**：
- **外貌描述**：
- **个性**：
- **背景**：
- **在故事中的角色**：

#### 角色 4
- **名字**：
- **外貌描述**：
- **个性**：
- **背景**：
- **在故事中的角色**：

#### 角色 5
- **名字**：
- **外貌描述**：
- **个性**：
- **背景**：
- **在故事中的角色**：

#### 角色 6
- **名字**：
- **外貌描述**：
- **个性**：
- **背景**：
- **在故事中的角色**：

#### 角色 7
- **名字**：
- **外貌描述**：
- **个性**：
- **背景**：
- **在故事中的角色**：

#### 角色 8
- **名字**：
- **外貌描述**：
- **个性**：
- **背景**：
- **在故事中的角色**：

(重复上述结构以添加更多支持角色)

</RESPONSE_TEMPLATE>

当然，不要包含XML标签 - 这些只是为了指示示例，并且应该从你的回答中省略。
    
    """

    # Generate Initial Story Elements
    _Logger.Log(f"Generating Main Story Elements", 4)
    Messages = [Interface.BuildUserQuery(Prompt)]
    Messages = Interface.SafeGenerateText(
        _Logger, Messages, Writer.Config.INITIAL_OUTLINE_WRITER_MODEL, _MinWordCount=150
    )
    Elements: str = Interface.GetLastMessageText(Messages)
    _Logger.Log(f"Done Generating Main Story Elements", 4)

    return Elements






# """
#     Prompt: str = f"""
# I'm working on writing a fictional story, and I'd like your help writing out the story elements.

# Here's the prompt for my story.
# <PROMPT>
# {_OutlinePrompt}
# </PROMPT>

# Please make your response have the following format:

# <RESPONSE_TEMPLATE>
# # Story Title

# ## Genre
# - **Category**: (e.g., romance, mystery, science fiction, fantasy, horror)

# ## Theme
# - **Central Idea or Message**:

# ## Pacing
# - **Speed**: (e.g., slow, fast)

# ## Style
# - **Language Use**: (e.g., sentence structure, vocabulary, tone, figurative language)

# ## Plot
# - **Exposition**:
# - **Rising Action**:
# - **Climax**:
# - **Falling Action**:
# - **Resolution**:

# ## Setting
# ### Setting 1
# - **Time**: (e.g., present day, future, past)
# - **Location**: (e.g., city, countryside, another planet)
# - **Culture**: (e.g., modern, medieval, alien)
# - **Mood**: (e.g., gloomy, high-tech, dystopian)

# (Repeat the above structure for additional settings)

# ## Conflict
# - **Type**: (e.g., internal, external)
# - **Description**:

# ## Symbolism
# ### Symbol 1
# - **Symbol**:
# - **Meaning**:

# (Repeat the above structure for additional symbols)

# ## Characters
# ### Main Character(s)
# #### Main Character 1
# - **Name**:
# - **Physical Description**:
# - **Personality**:
# - **Background**:
# - **Motivation**:

# (Repeat the above structure for additional main characters)


# ### Supporting Characters
# #### Character 1
# - **Name**:
# - **Physical Description**:
# - **Personality**:
# - **Background**:
# - **Role in the story**:

# #### Character 2
# - **Name**:
# - **Physical Description**:
# - **Personality**:
# - **Background**:
# - **Role in the story**:

# #### Character 3
# - **Name**:
# - **Physical Description**:
# - **Personality**:
# - **Background**:
# - **Role in the story**:

# #### Character 4
# - **Name**:
# - **Physical Description**:
# - **Personality**:
# - **Background**:
# - **Role in the story**:

# #### Character 5
# - **Name**:
# - **Physical Description**:
# - **Personality**:
# - **Background**:
# - **Role in the story**:

# #### Character 6
# - **Name**:
# - **Physical Description**:
# - **Personality**:
# - **Background**:
# - **Role in the story**:

# #### Character 7
# - **Name**:
# - **Physical Description**:
# - **Personality**:
# - **Background**:
# - **Role in the story**:

# #### Character 8
# - **Name**:
# - **Physical Description**:
# - **Personality**:
# - **Background**:
# - **Role in the story**:

# (Repeat the above structure for additional supporting character)

# </RESPONSE_TEMPLATE>

# Of course, don't include the XML tags - those are just to indicate the example.
# Also, the items in parenthesis are just to give you a better idea of what to write about, and should also be omitted from your response.
    
#     """

