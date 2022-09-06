package collectors

import (
	"database/sql"
	"github.com/prometheus/client_golang/prometheus"
)

type trafficCollector struct {
	*baseCollector

	desc *prometheus.Desc
}

func NewTrafficCollector(db *sql.DB) *trafficCollector {
	desc := prometheus.NewDesc("mysql_traffic", "mysql in and out traffic", []string{"direction"}, nil)
	return &trafficCollector{NewbaseCollector(db), desc}
}

func (c *trafficCollector) Describe(desc chan<- *prometheus.Desc)  {
	desc <- c.desc
}

func (c *trafficCollector) Collect(metrics chan<- prometheus.Metric)  {
	in := c.status("Bytes_received")
	out := c.status("Bytes_sent")
	metrics <- prometheus.MustNewConstMetric(c.desc, prometheus.CounterValue, in, "in")
	metrics <- prometheus.MustNewConstMetric(c.desc, prometheus.CounterValue, out, "out")
}
