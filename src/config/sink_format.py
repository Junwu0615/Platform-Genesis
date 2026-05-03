SINK_MACH_STATUS_LOGS = {
  "schema": {
    "type": "struct",
    "fields": [
      { "type": "int32", "optional": True, "field": "machine_id" },
      { "type": "string", "optional": True, "field": "status" },
      { "type": "string", "optional": True, "field": "event_time" }
    ],
    "optional": False
  },
  "payload": {
    "machine_id": None,
    "status": None,
    "event_time": None
  }
}

SINK_PROD_ORDERS = {
  "schema": {
    "type": "struct",
    "fields": [
      { "type": "int32", "optional": False, "field": "order_id" },
      { "type": "int32", "optional": True, "field": "product_id" },
      { "type": "int32", "optional": True, "field": "quantity" },
      { "type": "string", "optional": True, "field": "start_at" },
      { "type": "string", "optional": True, "field": "end_at" },
      { "type": "string", "optional": True, "field": "created_at" },
    ],
    "optional": False
  },
  "payload": {
    "order_id": None,
    "product_id": None,
    "quantity": None,
    "start_at": None,
    "end_at": None,
    "created_at": None,
  }
}

SINK_PROD_RECORDS = {
  "schema": {
    "type": "struct",
    "fields": [
      { "type": "int32", "optional": True, "field": "order_id" },
      { "type": "int32", "optional": True, "field": "machine_id" },
      { "type": "int32", "optional": True, "field": "product_id" },
      { "type": "int32", "optional": True, "field": "quantity" },
      { "type": "string", "optional": True, "field": "event_time" },
    ],
    "optional": False
  },
  "payload": {
    "order_id": None,
    "machine_id": None,
    "product_id": None,
    "quantity": None,
    "event_time": None,
  }
}