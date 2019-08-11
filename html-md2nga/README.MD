### 简介

- 本工具支持将HTML或Markdown转换为NGA代码（一种BBCode方言）

- 本工具的流程为Markdown->HTML->NGA，对于Markdown来说，先经由开源代码PyMarkdown2转换为html后再次转换为NGA代码。
- 对于HTML->NGA的部分，请参见html2bbcode文件夹下的README.MD
- 在成立初期，这是一个**场景驱动**的项目，用于王者荣耀官方公告的自动搬运。支持了王者荣耀官方公告html中的一系列常见元素，如内嵌在HTML中的css代码等。对于其他HTML/Markdown元素，可能是未经充分测试的。对于这一部分，欢迎[联系作者](mailto:3160105216@zju.edu.cn)或提交Issue/PR

### 一些已知的限制

（欢迎补充）

- 无法将含有HTML标签的Markdown转换为NGA代码（原因：Markdown会先转换为HTML代码。
- 由于NGA代码的限制，不支持除字体大小/文字颜色外的大多数CSS
- NGA支持左/中/右文字对齐，但本工程暂还不包括

### 关于作者

NGAid: sjn4048,

