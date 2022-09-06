package collectors

import (
	"database/sql"
	"fmt"
	"github.com/prometheus/client_golang/prometheus"
)

type upCollector struct {
	*baseCollector

	desc *prometheus.Desc
}

func NewUpCollector(db *sql.DB) *upCollector {
	desc := prometheus.NewDesc("mysql_up", "mysql health", nil, nil)
	return &upCollector{NewbaseCollector(db), desc}
}

func (c *upCollector) Describe(desc chan<- *prometheus.Desc)  {
	desc <- c.desc
}

func (c *upCollector) Collect(metrics chan<- prometheus.Metric)  {
	up := 1
	if err := c.db.Ping(); err !=nil{
		fmt.Println(err)
		up =0
	}
	metrics <- prometheus.MustNewConstMetric(c.desc, prometheus.GaugeValue, float64(up))
}
