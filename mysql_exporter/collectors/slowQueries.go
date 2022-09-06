package collectors

import (
	"database/sql"
	"github.com/prometheus/client_golang/prometheus"
)

type slowCollector struct {
	*baseCollector
	desc *prometheus.Desc
}

func NewSlowCollector(db *sql.DB) *slowCollector {
	desc := prometheus.NewDesc("mysql_slowqueries", "mysql slow query", nil, nil)
	return &slowCollector{NewbaseCollector(db), desc}
}

func (c *slowCollector) Describe(desc chan<- *prometheus.Desc)  {
	desc <- c.desc
}

func (c *slowCollector) Collect(metrics chan<- prometheus.Metric)  {
	slowqueries := c.status("Slow_queries")
	metrics <- prometheus.MustNewConstMetric(c.desc, prometheus.GaugeValue, slowqueries)
}
