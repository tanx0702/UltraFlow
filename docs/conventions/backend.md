# 后端编码规范与检查清单

> last_updated: 2026-05-26
> status: active

---

## 一、API 接口规范

### 1.1 统一响应格式（CRITICAL）

所有接口必须返回 `ApiResponse[T]`，**严禁裸 dict**。

```python
# app/models/common.py
from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    code: int = 0
    data: T | None = None
    msg: str = ""
```

**正确示例：**

```python
@router.put("/user/reminder", response_model=ApiResponse[None])
async def update_reminder(...):
    ...
    return ApiResponse(code=0, data=None, msg="")
```

**错误示例（禁止）：**

```python
# ❌ 裸 dict，没有 response_model
return {"success": True}
```

### 1.2 接口规范清单

生成或修改 API 接口时，逐项检查：

- [ ] 路由装饰器包含 `response_model=ApiResponse[T]`
- [ ] 返回值为 `ApiResponse(...)` 实例，非裸 dict
- [ ] 异常统一用 `HTTPException(status_code=...)`，exception handler 会自动转为 `ApiResponse` 格式
- [ ] Request Body 使用 Pydantic BaseModel，不在参数列表中直接用 `str` / `dict`
- [ ] 需要鉴权的接口包含 `user: dict = Depends(get_current_user)`
- [ ] 数据库查询强制按 `userId` 过滤

### 1.3 路由注册

新增模块后必须在 `main.py` 中注册：
```python
app.include_router(xxx.router, prefix="/api")
```

---

## 二、异步编程

- [ ] 所有路由函数必须 `async def`
- [ ] 所有数据库操作使用 `await`（Motor 异步驱动）
- [ ] 所有 HTTP 调用使用 `await`（如 AI API）
- [ ] 禁止使用 `time.sleep()`，用 `await asyncio.sleep()`

---

## 三、AI 服务规范

### 3.1 Prompt 修改

修改 `backend/app/prompts/` 下的 Prompt 文件时：

- [ ] 每次回复必须是合法 JSON（`response_format: json_object` 已保证）
- [ ] `extractedHabit` 的 action 必须在 `VALID_ACTIONS` 内
- [ ] 新增 example 必须覆盖边界情况（无意图 / 模糊意图 / 去重 / 调整）
- [ ] `reply` 不写编号列表，不写长段分析

### 3.2 输出处理

- [ ] JSON 解析必须经 `parse_llm_output()` — 含正则兜底
- [ ] habit 必须经 `validate_extracted_habit()` — 校验 action / name / target / frequency / reminderTime
- [ ] 校验失败时返回 `{"reply": raw, "extractedHabit": null}`，不丢异常

### 3.3 安全

- [ ] 用户输入不直接拼入 system prompt（通过 `user_context` 参数注入）
- [ ] 对话历史取最近 20 条（`MAX_HISTORY_MESSAGES`），防止 token 溢出

---

## 四、模型层

- [ ] 新数据模型定义在 `app/models/` 对应文件中
- [ ] 所有模型继承 `pydantic.BaseModel`
- [ ] 字段必须标注类型，使用 `| None` 而非 `Optional[X]`
- [ ] 字符串字段按需加 `max_length` 约束

---

## 五、数据库

- [ ] 新增集合后更新 `backend/app/core/database.py` 的索引创建逻辑
- [ ] 查询按 `userId` 隔离（多租户）
- [ ] 时间字段使用 UTC：`datetime.now(timezone.utc)`

---

## 六、检查脚本（建议 CI 运行）

新建接口后运行此脚本检查合规：

```python
# scripts/check_api.py
import ast, sys, os

def check_file(filepath):
    with open(filepath) as f:
        source = f.read()
    tree = ast.parse(source)

    functions = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) if not n.name.startswith("_")]
    has_A = "ApiResponse" in source
    has_response_model = any(hasattr(d, "value") and "response_model" in ast.unparse(d) for d in ast.walk(tree) if isinstance(d, ast.keyword))

    issues = []
    for func in functions:
        for node in ast.walk(func):
            if isinstance(node, ast.Return) and isinstance(node.value, ast.Dict):
                issues.append(f"  ❌ {func.name}: 返回裸 dict")
    return issues

for root, dirs, files in os.walk("backend/app/api"):
    for f in files:
        if f.endswith(".py") and f != "__init__.py":
            fp = os.path.join(root, f)
            for issue in check_file(fp):
                print(issue)

print("✅ 检查完成")
```

---

## 七、文件组织

```
backend/
├── main.py               # FastAPI 入口
├── app/
│   ├── api/               # 路由层 — 只做参数校验和响应组装
│   ├── services/          # 业务逻辑层 — AI 对话、打卡计算
│   ├── prompts/           # LLM Prompt 内容 — base / personas / safety / examples
│   ├── models/            # Pydantic 模型 — Request/Response 定义
│   └── core/              # 基础设施 — 配置、数据库、依赖注入、异常处理
```

规则：
- api/ 不直接访问数据库集合（通过 service 层，除非简单 CRUD）
- services/ 不导入 FastAPI 相关模块（保持纯净）
