**Affected version**

versions through commit [334beb1](https://github.com/owntone/owntone-server/commit/334beb1cfa3fb4129655360fb8d249a47c136f5f) in master branch

**Platform**

Ubuntu 20.04

**Description**

NULL pointer dereference in function parse_meta in src/httpd_daap.c in owntone-server through commit 334beb1 (newer commit after version 28.2) allows remote attackers to cause a Denial of Service via sending a DAAP request to the server.

**Analysis**

When parsing a DAAP request (pattern: `^/databases/[[:digit:]]+/groups$`) with an empty `meta` parameter, function `daap_reply_groups` calls `evhttp_find_header` at src/httpd_daap.c:1680 and `param` is assigned an empty string. Function `parse_meta` calls `metastr = strdup(param)` at src/httpd_daap.c:628 and `metastr` is also an empty string. Therefore, `field` becomes NULL at line 639, and the call to `strlen` at line 646 causes a NULL pointer dereference.

**Reproduction method**

Provided in [reproduction.md](reproduction.md).

