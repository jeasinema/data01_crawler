##爬取地址
####成交指标：http://data.01caijing.com/p2p/website/index-data.json?website=www.my089.com&groupBy=day
####利率指标：http://data.01caijing.com/p2p/website/interest-data.json?website=www.my089.com&groupBy=month
####期限指标：http://data.01caijing.com/p2p/website/period-data.json?website=www.my089.com
####借款人数量：http://data.01caijing.com/p2p/borindex.json?website=www.my089.com
####人均借款额：http://data.01caijing.com/p2p/borrower/avg-data.json?website=www.my089.com
####投资人数量：http://data.01caijing.com/p2p/investor/index-data.json?website=www.my089.com
####人均投资额：http://data.01caijing.com/p2p/investor/avg-data.json?website=www.my089.com
####贷款余额：http://data.01caijing.com/p2p/website/balance-data.json?website=www.my089.comi


##说明：
1.返回json
2.无需cookie,token
3.按月与按天直接&groupBy=day/month即可
4.不同基金平台的区别在于website-key

##json时间戳：
1.magic_day：2015-3-25  1427241600000
2.magic_month：2015-9 1441065600000
3.递增即可：24*3600*1000 为一天的时间,30*24*3600*1000为一月的时间

##各信贷站的url：
index里面能获得信贷站的主页域名，添加至post_usl里面即可

##自动爬取所有的信贷站：
	
	function setpage(page){
		$("#p").val(page);
		$("#check_page").val(page);
		search_function()
	}

	// 表单查询
	function search_function(){
		$("#search_form").submit();
	}
	
	<form class="search_form" id="search_form" action="/p2p/index.html" method="post">
	<a href="javascript:setpage(41)">»</a>

1.	在http://data.01caijing.com/p2p/index.html上对这两个表单赋值
2.	post这个表单,{"p":new_page,"check_page":newe_page}
3.	返回的response即为新的页面
4.	总页数可以在首页获得

##脚本使用方法（Windows下）：
	
	MKDIR result
	python data_01.py

视网络情况等待约7分钟左右即可完成爬取
爬取结果输出于.\result目录下

###可能遇到的问题：

1.csv文件名/内容乱码
->notepad打开，选择用ANSI格式保存，再次打开即可

2.看不到包含所有信贷站的excel
->请等待后续版本

##版本更新：

20160326~v0.1  
	-	给定页面爬取
	-	时间戳对应
	-	空数据标记
	-	csv导出

TODO：
	-	自动爬取所有的p2p站点
	-	完成一次爬取即写一次文件
