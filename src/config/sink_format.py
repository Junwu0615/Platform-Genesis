# SINK_MACH_STATUS_LOGS = {
#   "schema": {
#     "type": "struct",
#     "fields": [
#       { "type": "int32", "optional": True, "field": "machine_id" },
#       { "type": "string", "optional": True, "field": "status" },
#       { "type": "string", "optional": True, "field": "event_time" }
#     ],
#     "optional": False
#   },
#   "payload": {
#     "machine_id": None,
#     "status": None,
#     "event_time": None
#   }
# }
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


# SINK_PROD_ORDERS = {
#   "schema": {
#     "type": "struct",
#     "fields": [
#       { "type": "int32", "optional": False, "field": "order_id" },
#       { "type": "int32", "optional": True, "field": "product_id" },
#       { "type": "int32", "optional": True, "field": "quantity" },
#       { "type": "string", "optional": True, "field": "start_at" },
#       { "type": "string", "optional": True, "field": "end_at" },
#       { "type": "string", "optional": True, "field": "created_at" },
#     ],
#     "optional": False
#   },
#   "payload": {
#     "order_id": None,
#     "product_id": None,
#     "quantity": None,
#     "start_at": None,
#     "end_at": None,
#     "created_at": None,
#   }
# }
SINK_PROD_ORDERS = {
    'topic': 'inst.prod-orders',
    'content': """
{
  "type": "record",
  "name": "production_orders",
  "fields": [
    {"name": "order_id", "type": "int"},
    {"name": "product_id", "type": "int"},
    {"name": "quantity", "type": "int"},
    {"name": "start_at", "type": "string"},
    {"name": "end_at", "type": "string"},
    {"name": "created_at", "type": "string"}
  ]
}
""",
}


# SINK_PROD_RECORDS = {
#   "schema": {
#     "type": "struct",
#     "fields": [
#       { "type": "int32", "optional": True, "field": "order_id" },
#       { "type": "int32", "optional": True, "field": "machine_id" },
#       { "type": "int32", "optional": True, "field": "product_id" },
#       { "type": "int32", "optional": True, "field": "quantity" },
#       { "type": "string", "optional": True, "field": "event_time" },
#     ],
#     "optional": False
#   },
#   "payload": {
#     "order_id": None,
#     "machine_id": None,
#     "product_id": None,
#     "quantity": None,
#     "event_time": None,
#   }
# }
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