## Plugin Description

’‘’
此插件用于获取牛客网上最近的社区讨论。
在回答用户有关招聘的问题时，使用此插件获取最新的社区讨论信息，如：有哪些公司正在招聘算法工程师？
在回答用户有关特定公司的岗位信息时，需要使用此插件查询特定公司岗位，keyword使用公司名称和岗位名称。例如：华为的算法工程师怎么样？
在给用户提供面试建议时，需要使用此插件获取面试经验。例如：给我提供华为的算法工程师面试建议。
‘’‘

## Plugin Interface Generate Prompt

Use this template to generate the interface information of the plugin. Please help me generate the interface information that conforms to the OpenAPI v3 specification based on the following parameters:

’‘’
请根据以下参数帮助我生成符合OpenAPI v3规范的接口信息：
URL: http://8.138.28.154:8000/niuke 
请求方式：post
请求参数：名称：company；含义：查询的公司名称。尽可能使用公司简称，比如：字节跳动->字节、理想汽车->理想；如果用户没有指定特定公司，传空字符串；是否必须：是。
请求参数：名称：jobName；含义：查询的岗位名称。如果用户没有指定岗位，传空字符串；是否必须：是。
请求参数：名称：type；含义：查询的信息类型。信息类型分两种：【薪资、面试经验】，根据用户的问题选择，比如：查询特定公司的待遇->薪资；必须传这三种中的一个；是否必须：是。
请求参数：名称：numPages；含义：查询的页面数量，范围1-10，用整数数字，一般使用5。是否必须：是。
返回参数：名称：data；含义：查询结果，是字符串数组。是否必须：是。
‘’‘