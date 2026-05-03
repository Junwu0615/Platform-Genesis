SINK_MACH_STATUS_LOGS = {
    'topic': 'inst.status-logs',
    'content': """
{
  "type": "record",
  "name": "machine_status_logs",
  "fields": [
    {"name": "machine_id", "type": "int"},
    {"name": "status", "type": "string"},
    {"name": "event_time", "type": "string"}
  ]
}
""",
}


SINK_PROD_ORDERS = {
    'topic': 'inst.prod-orders',
    'content': """
{
  "type": "record",
  "name": "production_orders",
  "fields": [
    {"name": "order_id", "type": "int"},
    {"name": "product_id", "type": ["null", "int"], "default": null},
    {"name": "quantity", "type": ["null", "int"], "default": null},
    {"name": "start_at", "type": ["null", "string"], "default": null},
    {"name": "end_at", "type": ["null", "string"], "default": null},
    {"name": "created_at", "type": ["null", "string"], "default": null}
  ]
}
""",
}


SINK_PROD_RECORDS = {
    'topic': 'inst.prod-records',
    'content': """
{
  "type": "record",
  "name": "production_orders",
  "fields": [
    {"name": "order_id", "type": "int"},
    {"name": "machine_id", "type": "int"},
    {"name": "product_id", "type": "int"},
    {"name": "quantity", "type": "int"},
    {"name": "event_time", "type": "string"}
  ]
}
""",
}