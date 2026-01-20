**Affected version**

versions through commit [c4d57aa](https://github.com/owntone/owntone-server/commit/c4d57aa5d1227525479354209665fd2089b9607e) in master branch

**Description**

A NULL pointer dereference in the safe_atou64 function (src/misc.c) of owntone-server through commit c4d57aa allows attackers to cause a Denial of Service (DoS) via sending a series of crafted HTTP requests to the server.

**Analysis**

If an attacker sends an HTTP PUT request with URL "/api/outputs/set" and a carefully constructed JSON dictionary (e.g. '{"outputs": [123, null, {"id": "456"}, [], "valid", true]}'), and then sends an HTTP GET request with URL "/api/outputs", the server will call the function `safe_atou64` with a NULL `str` parameter, causing the function `strtoull` to raise a NULL Pointer Dereference.

**Reproduction method**

Provided in [reproduction.md](reproduction.md).

