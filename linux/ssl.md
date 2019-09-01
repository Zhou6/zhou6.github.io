## ssl证书

1. 申请证书
2. 配置nginx
3. 打开443端口
4. 申请Domain Validation（DV）类型的SSL证书时，Certificate Authority（CA）机构只验证域名所有权，不会人工介入审核验证。这一特性使DV证书颁发十分方便快捷，但也导致在系统审核的过程中产生很多验证限制，例如安全审核，DNS验证失败等，影响证书的正常颁发。
为了使用户能够自主定位问题，查询原因，调整配置，提高DV证书的的颁发效率，我司提供《DV证书自主检测工具》（以下简称“工具”）。
通过访问https://myssl.com/dns_check.html#ssl_verify使用此工具。
具体使用方法参见手册：
http://sslfiles.ufile.ucloud.com.cn/DV%E8%AF%81%E4%B9%A6%E8%87%AA%E4%B8%BB%E6%A3%80%E6%B5%8B%E5%B7%A5%E5%85%B7%E6%89%8B%E5%86%8C.docx
下次如果不行可以有这样的测试步骤：
- https://myssl.com/ 测试一下
- 在该台服务器上 curl https://<域名> -k 做最简单的测试
- 如果再不行，在该台服务器上用 openssl s_server/s_client 做调试，例如openssl s_client -connect <域名>:443

