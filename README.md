## ME
#### MyError

- 本项目开发用于开发者监视自己的代码运行情况, 错误信息记录, GUI界面查看.
- 项目依赖于数据库信息, 程序需要将错误信息写入到数据库当中, 后续将开发对应的SDK用于接入.
- 数据库的支持目前暂定适配PostgreSQL/SQLite/MySQL/Oracle, 由于是个人开发者使用,  
  不会考虑太多性能问题, 比如不会兼容in-memory数据库, 以及更不会使用大数据库领域热门的数据库支持,  
  例如ClickHouse, Hive等.

- 目前项目状况:
  - 适配数据库GUI管理
    - [x] PgSQL
    - [ ] SQLite
    - [x] MySQL
    - [ ] Oracle
  - 错误信息GUI管理
    - [ ] 列表展示
    - [ ] 分页展示
    - [ ] 搜索
    - [ ] 排序
    - [ ] 删除(这部分考虑在SDK中加入接口处理)
    - [ ] 更新(忽略错误等操作, 单个错误忽略/应用级别忽略/应用组级别忽略)
  - 数据库结构
    - [ ] 错误类型表
    - [ ] 错误内容表
    - [ ] 错误日志表
    - [ ] 错误日志类型表
    - [ ] 应用管理表
    - [ ] 权限管理表