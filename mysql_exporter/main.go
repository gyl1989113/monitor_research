package main

import (
	"database/sql"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	"github.com/sirupsen/logrus"
	"mysql_exporter/collectors"
	"net/http"
)

var	db *sql.DB

func InitMysql() (err error) {
	dsn := "root:root001@tcp(127.0.0.1:3306)/mysql?charset=utf8mb4&loc=PRC&parseTime=True"
	db, err = sql.Open("mysql", dsn)
	if err !=nil{
		logrus.Fatal(err)
		return err
	}
	fmt.Println("mysql 连接成功")
	err = db.Ping()
	if err !=nil{
		logrus.Fatal(err)
		return err
	}
	return nil
}


func main()  {
	addr := ":8090"
	err := InitMysql()
	if err != nil {
		logrus.Fatal(err)
	}
	//定义指标

	//数据库可用
	upCollector :=collectors.NewUpCollector(db)
	//慢查询
	slowQueryCollector := collectors.NewSlowCollector(db)
	//数据库流量
	trafficCollector := collectors.NewTrafficCollector(db)
	//指令数量
	cmdCollector := collectors.NewCommandCollector(db)
	//连接数
	connectCollector := collectors.NewConnectCollector(db)
	//注册指标
	prometheus.MustRegister(upCollector)
	prometheus.MustRegister(slowQueryCollector)
	prometheus.MustRegister(trafficCollector)
	prometheus.MustRegister(cmdCollector)
	prometheus.MustRegister(connectCollector)
	//注册控制器
	http.Handle("/metrics", promhttp.Handler())
	//启动web服务

	defer db.Close()
	err =http.ListenAndServe(addr,nil)
	if err != nil {
		logrus.Fatal(err)
	}
}
