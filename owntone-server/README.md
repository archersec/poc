**Affected version**

versions through commit [334beb1](https://github.com/owntone/owntone-server/commit/334beb1cfa3fb4129655360fb8d249a47c136f5f) in master branch

**Platform**

Ubuntu 20.04

**Description**

NULL pointer dereference in function parse_meta in src/httpd_daap.c in owntone-server through commit 334beb1 (newer commit after version 28.2) allows remote attackers to cause a Denial of Service via sending a DAAP request to the server.

**Analysis**

When parsing a DAAP request (pattern: `^/databases/[[:digit:]]+/groups$`) with an empty `meta` parameter, function `daap_reply_groups` calls `httpd_query_value_find` at src/httpd_daap.c:1647 and `param` is assigned an empty string. Function `parse_meta` calls `metastr = strdup(param)` at src/httpd_daap.c:606 and `metastr` is also an empty string. Therefore, `strchr(ptr + 1, ',')` causes a heap-buffer-overflow. If OwnTone is not compiled with ASan options, function `daap_reply_groups` will raise SIGSEGV at line 617 due to NULL pointer dereference.

**Reproduction method**

Provided in [reproduction.md](reproduction.md).

