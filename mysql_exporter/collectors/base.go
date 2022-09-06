package collectors

import "database/sql"

// 只在该包中访问此结构体，所以不需要大写
type baseCollector struct {
	db *sql.DB
}

func NewbaseCollector(db *sql.DB) *baseCollector {
	return &baseCollector{
		db: db,
	}
}

func (c *baseCollector)status(name string) float64 {
	row := c.db.QueryRow("show global status where variable_name=?", name)
	var (
		vname string
		value float64
	)
	if err := row.Scan(&vname, &value);err== nil{
		return value
	}
	return 0
}

func (c *baseCollector) variables(name string) float64 {
	row := c.db.QueryRow("show global variables where variable_name=?", name)
	var (
		vname string
		value float64
	)
	if err := row.Scan(&vname, &value);err== nil{
		return value
	}
	return 0
}
