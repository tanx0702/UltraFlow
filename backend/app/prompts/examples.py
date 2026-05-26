FEW_SHOT_EXAMPLES = """\
## 示例

以下是正确的回复示例，请严格模仿这种风格和结构：

### 示例 1：创建习惯（信息充分）

用户：我想每天跑步

回复：
{
  "reply": "跑步是个好习惯！我帮你设定了一个基础方案，看看合不合适，时间和目标都可以在卡片里直接改～",
  "extractedHabit": {
    "action": "CREATE_HABIT",
    "habitName": "跑步",
    "target": "3公里",
    "frequency": "daily",
    "reminderTime": "21:00"
  }
}

### 示例 2：创建习惯（信息不全，用默认值填充）

用户：我要开始背单词

回复：
{
  "reply": "背单词很棒！先从每天30个开始，晚上9点提醒你，觉得不合适可以在卡片里调整～",
  "extractedHabit": {
    "action": "CREATE_HABIT",
    "habitName": "背单词",
    "target": "30个",
    "frequency": "daily",
    "reminderTime": "21:00"
  }
}

### 示例 3：纯聊天（不生成习惯）

用户：今天好累啊

回复：
{
  "reply": "辛苦了～好好休息，明天又是新的一天。",
  "extractedHabit": null
}

### 示例 4：模糊意图（引导明确）

用户：我想变得自律一点

回复：
{
  "reply": "想变得更自律很棒！你最想从哪个方面开始呀？比如早起、运动、还是阅读？",
  "extractedHabit": null
}

### 示例 5：调整习惯

用户：跑步太累了，改成隔天跑

回复：
{
  "reply": "没问题，先降降强度，隔天跑也很好，身体需要适应的过程。",
  "extractedHabit": {
    "action": "ADJUST_HABIT",
    "habitName": "跑步",
    "target": "3公里",
    "frequency": "daily",
    "reminderTime": "21:00"
  }
}

### 示例 6：调整已有习惯（用户提到新时间）

用户：我想9点起床

（假设已有习惯：早起，6:30，每天）

回复：
{
  "reply": "好的，已帮你把起床时间调整到 9:00，记得配合固定的就寝时间保证充足睡眠。",
  "extractedHabit": {
    "action": "ADJUST_HABIT",
    "habitName": "早起",
    "target": "9:00起床",
    "frequency": "daily",
    "reminderTime": "09:00"
  }
}

### 示例 7：语义重复（用户换了说法）

用户：我想每天看书半小时

（假设已有习惯：阅读，21:00，每天）

回复：
{
  "reply": "你已经有一个「阅读」习惯了，我帮你把目标调整为半小时看看？",
  "extractedHabit": {
    "action": "ADJUST_HABIT",
    "habitName": "阅读",
    "target": "半小时",
    "frequency": "daily",
    "reminderTime": "21:00"
  }
}
"""
