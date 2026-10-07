# API List


All paths start with `/api` (the Vite dev server forwards them to the backend).<br>
Errors return `{"detail": "message"}`. Live docs: http://localhost:8000/docs

## GET

**show service**

name: `/api/services`<br>
parameter:-<br>
body:-<br>
HTTP Status: 200 ok, 500 ISE <br>
JSON response: 
```json 
//200
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

//500
{
    "error":string
}
```
## POST

**new ticket**

name: `/api/tickets`<br>
parameter:-<br>
body:
```json
{
    "service_id": int
}
```
HTTP Status: 201 ok, 500 ISE,404 Not Found (unknown service) <br>
JSON response: 
```json 
//201
{
    "ticket_id": int,
    "ticket_cod": string,
    "service_name": string,
    "timeStamp": string,
}

//404
{
    "error":string
}

//500
{
    "error":string
}
```
**next customer**

name: `/api/couters/{id_counter}/next-customer`<br>
parameter: id_counter<br>
body:-<br>
HTTP Status: 200 ok, 204 no content 500 ISE <br>
JSON responses: 
```json
//200 
{
    "ticket_id": int,
    "ticket_cod": string,
    "service": {
	      "service_id": int,
	      "service_name": string,
	      "description": string,
    }
}
//500
{
    "error":string
}
```
## PUT


## DELETE