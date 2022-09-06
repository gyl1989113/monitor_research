package collectors

import (
	"database/sql"
	"github.com/prometheus/client_golang/prometheus"
)

type connectCollector struct {
	*baseCollector

	desc *prometheus.Desc
}

var constLabel = prometheus.Labels{"code": "f014270"}

func NewConnectCollector(db *sql.DB) *connectCollector {
	desc := prometheus.NewDesc("mysql_connect", "mysql connect", []string{"type"}, constLabel)
	return &connectCollector{NewbaseCollector(db), desc}
}

func (c *connectCollector) Describe(desc chan<- *prometheus.Desc)  {
	desc <- c.desc
}

func (c *connectCollector) Collect(metrics chan<- prometheus.Metric)  {
	connected := c.status("Threads_connected")
	cached := c.status("Threads_cached")
	created := c.status("Threads_created")
	running := c.status("Threads_running")
	metrics <- prometheus.MustNewConstMetric(c.desc, prometheus.CounterValue, connected, "connected")
	metrics <- prometheus.MustNewConstMetric(c.desc, prometheus.CounterValue, cached, "cached")
	metrics <- prometheus.MustNewConstMetric(c.desc, prometheus.CounterValue, created, "created")
	metrics <- prometheus.MustNewConstMetric(c.desc, prometheus.CounterValue, running, "running")
}
