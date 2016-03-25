##成交指标：http://data.01caijing.com/p2p/website/index-data.json?website=www.my089.com&groupBy=day
##利率指标：http://data.01caijing.com/p2p/website/interest-data.json?website=www.my089.com&groupBy=month
##期限指标：http://data.01caijing.com/p2p/website/period-data.json?website=www.my089.com
##借款人数量：http://data.01caijing.com/p2p/borrower/index-data.json?website=www.my089.com
##人均借款额：http://data.01caijing.com/p2p/borrower/avg-data.json?website=www.my089.com
##投资人数量：http://data.01caijing.com/p2p/investor/index-data.json?website=www.my089.com
##人均投资额：http://data.01caijing.com/p2p/investor/avg-data.json?website=www.my089.com
##贷款余额：http://data.01caijing.com/p2p/website/balance-data.json?website=www.my089.comi


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
