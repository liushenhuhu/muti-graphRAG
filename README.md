 **对graphRAG的改动** 
D:\Python311\Lib\site-packages\graphrag\utils\api.py  79行注释，80行添加
D:\Python311\Lib\site-packages\graphrag\api\query.py 552~655、716、719行注释
目的：为了增加图谱检索功能。
解释：
GraphRAG内置multi_index_local_search功能，需要将向量数据库和parquet数据库以列表形式传入，与普通local search不同的是，需要携带一个index name字段，为了防止不同数据库的id重复，graphRAG会将index name拼接在对应数据库id后方。然而在拼接过后，无法从向量数据库正确检索到parquet数据库中数据。
考虑到id重复的可能性非常小，几乎为0，因此对源码做变动，在lancedb和parquet数据id处理阶段取消拼接index name，从而实现多索引查询
