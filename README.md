# muti-graphRAG
基于[microsoftgraphRAG](https://www.runoob.com/markdown/md-link.html)进行二次开发
在原项目基础上增加功能：
- 增加了图谱数据库的管理功能，可以指定图谱进行创建、上传文件、索引构建和检索
- 扩展了multi_local_index接口，可以进行跨多个图谱的检索
- 增加了文件自动处理功能，构建图谱时可以上传所有常见类型文件

#### 模型支持
使用百炼平台，需要在.env添加DASHSCOPE_API_KEY

#### 文件处理
使用qwen-long进行处理，将文件转换为非结构化文本，并存入input中

对于超大文件，采取滑动窗口策略，分片进行内容提取

#### 对graphRAG的改动
\graphrag\utils\api.py  79行注释，80行添加
\graphrag\api\query.py 552~655、716、719行注释

目的：为了增加图谱检索功能。

解释：
GraphRAG内置multi_index_local_search功能，需要将向量数据库和parquet数据库以列表形式传入，与普通local search不同的是，需要携带一个index name字段，为了防止不同数据库的id重复，graphRAG会将index name拼接在对应数据库id后方。然而在拼接过后，无法从向量数据库正确检索到parquet数据库中数据。
考虑到id重复的可能性非常小，几乎为0，因此对源码做变动，在lancedb和parquet数据id处理阶段取消拼接index name，从而实现多索引查询
