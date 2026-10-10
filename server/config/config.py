BASEURL = "/api/"

ORIGIN = [
    "http://localhost:3000",
    "http://localhost:5173",
]
# route keys
URL_COUNTER = "counters"
URL_SERVICE = "services"
URL_TICKET  = "tickets"

ROUTES = {
    "COUNTER": BASEURL + URL_COUNTER,
    "SERVICE": BASEURL + URL_SERVICE,
    "TICKET":  BASEURL + URL_TICKET,
}