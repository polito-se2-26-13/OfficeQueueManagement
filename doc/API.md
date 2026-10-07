# API List

## GET

**show service**

name: `api/v1/service`<br>
parameter:-<br>
body:-<br>
HTTP Status: 202 ok, 500 ISE <br>
JSON response: 
```json 
[{
    "service_id": int,
    "service_name": string,
    "description": string,
},
{
    "service_id": int,
    "service_name": string,
    "description": string,
}... 
]
```
## POST

**new ticket**

name: `api/v1/service/ticket`<br>
parameter:-<br>
body:
```json
{
    "service_id": int
}
```
HTTP Status: 201 ok, 500 ISE <br>
JSON response: 
```json 
{
    "ticket_id": int,
    "ticket_cod": string,
    "service_name": string,
    "timeStamp": string,
}

```

## PUT

**next customer**

name: `api/v1/couter/{id_counter}/next-customer`<br>
parameter: id_counter<br>
body:-<br>
HTTP Status: 200 ok, 500 ISE <br>
JSON responses: 
```json
//not empty queue 
{
    "ticket_id": int,
    "ticket_cod": string,
    "service": {
	      "service_id": int,
	      "service_name": string,
	      "description": string,
    }
}

//empty queue 
{
    "ticket_id": null,
    "ticket_cod": null,
    "service_name": null,
}
```

## DELETE