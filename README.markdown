# 智能客服 RAG 项目

这是一个“企业风格但能直接运行”的智能客服 RAG 单仓库项目。它没有把所有企业能力都做满，但已经把真正企业项目里最关键的骨架搭出来了：

- 清晰的分层和目录
- 独立的应用入口
- 领域模型、服务层、基础设施层、工作流编排层
- 审计日志和用户反馈闭环
- 开箱即跑的 FastAPI 服务

你可以直接把这个仓库推到 GitHub，别人拉取后按本文档执行即可运行。

## 1. 项目定位

这个项目面向金融客服 RAG 场景，目标是把“知识加载、问题路由、检索召回、答案生成、合规校验、审计留痕、用户反馈”串成一条完整链路。

当前实现没有接入真实向量库和大模型，而是保留了企业项目中的职责边界，让你后续很容易替换成：

- Milvus / Elasticsearch / Neo4j
- LangGraph / Celery / Kafka
- vLLM / OpenAI / 自建模型服务
- MySQL / PostgreSQL / Redis

## 2. 目录结构

```text
智能客服-RAG项目/
├── apps/
│   └── api/                              # API 应用入口
│       ├── routers/
│       ├── dependencies.py
│       └── main.py
├── smart_cs_rag/                         # 核心业务包
│   ├── bootstrap/                        # 依赖装配
│   ├── common/                           # 配置等公共能力
│   ├── contracts/                        # API 契约模型
│   ├── domain/                           # 领域模型
│   ├── infrastructure/                   # 仓储与搜索引擎实现
│   ├── orchestration/                    # 问答工作流
│   └── services/                         # 业务服务
├── data/
│   ├── seed/                             # 种子知识库
│   └── runtime/                          # 运行时审计日志与反馈
├── tests/                                # 单元测试
├── 需求文档.md
├── 工作流程文档.md
├── requirements.txt
├── .gitignore
└── README.markdown
```

## 3. 项目分层

### 应用层 `apps/api`

负责 HTTP 接口、依赖注入和协议转换。

- `/health`：健康检查
- `/api/v1/ask`：问答接口
- `/api/v1/feedback`：反馈接口

### 领域层 `smart_cs_rag/domain`

定义系统里的核心对象：

- `KnowledgeDocument`
- `UserQuery`
- `RetrievalHit`
- `QueryResult`
- `FeedbackRecord`

### 服务层 `smart_cs_rag/services`

封装核心业务能力：

- `QueryRoutingService`：决定走哪条检索路径
- `RetrievalService`：召回知识
- `GenerationService`：组织答案
- `ComplianceService`：做输出合规检查
- `AuditService`：写审计日志
- `FeedbackService`：记录用户反馈

### 编排层 `smart_cs_rag/orchestration`

`QueryWorkflow` 把整个链路串起来：

1. 问题进入系统
2. 路由判定
3. 检索召回
4. 生成答案
5. 合规校验
6. 审计留痕
7. 返回结果

### 基础设施层 `smart_cs_rag/infrastructure`

当前提供两个落地实现：

- `JsonKnowledgeRepository`：从本地 JSON 加载知识库
- `JsonFeedbackRepository`：把反馈写到 JSON Lines 文件
- `SimpleHybridSearchEngine`：轻量混合检索引擎

## 4. 当前实现了什么

当前版本已经具备一个企业项目的最小闭环：

1. 可以启动 HTTP 服务
2. 可以接收用户问答请求
3. 可以做轻量路由判断
4. 可以从知识库中召回候选内容
5. 可以生成结构化回答
6. 可以做敏感词合规过滤
7. 可以记录审计日志
8. 可以接收用户反馈

## 5. 运行环境

- Python 3.11+
- Windows / macOS / Linux 均可

## 6. 安装依赖

```bash
pip install -r requirements.txt
```

## 7. 启动项目

在项目根目录执行：

```bash
uvicorn apps.api.main:app --reload
```

启动后访问：

- Swagger 文档：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- 健康检查：[http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

## 8. 接口示例

### 8.1 问答接口

请求：

```json
POST /api/v1/ask
{
  "question": "境外消费没有返现怎么办？",
  "language": "zh",
  "session_id": "demo-session-001",
  "history": []
}
```

响应示例：

```json
{
  "answer": "核心结论：针对“境外消费没有返现怎么办？”，当前最相关的知识是：境外消费返现活动需同时满足活动报名成功、消费币种符合规则、交易时间处于活动期三个条件。若未返现，应优先核查报名状态与入账时间。",
  "route": "faq_hybrid_route",
  "compliance_passed": true,
  "trace_id": "xxxx",
  "sources": [
    {
      "doc_id": "fee-001",
      "title": "境外消费返现活动规则",
      "source_type": "rate_table",
      "score": 2.5
    }
  ]
}
```

### 8.2 反馈接口

请求：

```json
POST /api/v1/feedback
{
  "session_id": "demo-session-001",
  "question": "境外消费没有返现怎么办？",
  "rating": 5,
  "comment": "回答清楚",
  "route": "faq_hybrid_route"
}
```

## 9. 测试

运行单元测试：

```bash
python -m unittest discover -s tests
```

## 10. 运行后会产生什么文件

程序运行后会在 `data/runtime/` 下写入运行时文件：

- `audit.log`：每次问答的审计记录
- `feedback.jsonl`：用户反馈记录

这两个文件已经加入 `.gitignore`，不会污染 Git 仓库。

## 11. 你后续可以怎么扩展

这个仓库已经给你留好了扩展点：

### 检索升级

- 替换 `SimpleHybridSearchEngine` 为 Elasticsearch + Milvus
- 在 `RetrievalService` 中增加 Reranker
- 增加 Query Rewriting

### 生成升级

- 替换 `GenerationService` 为真实 LLM 调用
- 接入 Prompt 模板管理
- 增加多轮对话记忆和工具调用

### 数据升级

- 将 `JsonKnowledgeRepository` 替换为数据库或对象存储
- 增加文档解析、切分、embedding、增量更新服务

### 工程升级

- 加 Dockerfile 和 docker-compose
- 加 CI/CD
- 加统一日志、监控和告警
- 加权限认证和租户隔离

## 12. 推荐提交到 GitHub 的方式

```bash
git init
git add .
git commit -m "feat: add enterprise-style smart customer service rag project"
```

然后推送到你的 GitHub 仓库即可。

## 13. 一句话介绍这个项目

这是一个按企业项目思路组织的智能客服 RAG 单仓库示例：应用层负责接口接入，领域层负责核心模型，服务层负责检索/生成/合规，编排层负责主链路，基础设施层负责知识库和反馈存储，因此它既能本地直接运行，也容易继续扩展成真正的企业级系统。
