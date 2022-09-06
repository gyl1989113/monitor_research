package collectors

import (
	"database/sql"
	"fmt"
	"github.com/prometheus/client_golang/prometheus"
)

type commandCollector struct {
	*baseCollector

	desc *prometheus.Desc
}

func NewCommandCollector(db *sql.DB) *commandCollector {
	desc := prometheus.NewDesc("mysql_command", "mysql insert,update,delete,select", []string{"cmd"}, nil)
	return &commandCollector{NewbaseCollector(db), desc}
}

func (c *commandCollector) Describe(desc chan<- *prometheus.Desc)  {
	desc <- c.desc
}

func (c *commandCollector) Collect(metrics chan<- prometheus.Metric)  {
	cmds := []string{"insert", "update", "delete", "select"}
	//注册多个指标
	for _,cmd := range cmds{
		metrics <- prometheus.MustNewConstMetric(c.desc, prometheus.CounterValue, c.status(fmt.Sprintf("com_%s", cmd)), cmd)
	}

}
