**Affected version**

master branch [83eadca2](https://git.lighttpd.net/lighttpd/lighttpd1.4/commit/83eadca2e811fc324049f509feb5d8e3d423aee7)

**Platform**

Ubuntu 20.04

**Description**

NULL pointer dereference in function connection_transition_h2 in src/connections.c in lighttpd/lighttpd1.4 through commit 83eadca2 allows remote attacker to cause a Denial of Service via sending a PRI request to the server.

**Analysis**

* When running function `plugins_load` in `plugin.c`, `srv->srvconf.h2proto` is not set to null.
* `http_dispatch[HTTP_VERSION_2]` is not initialized, leaving the `http_dispatch` struct empty.

These cause a null pointer dereference when user attempts to send the HTTP2 request `PRI`.

**Call stack**

```
Program received signal SIGSEGV, Segmentation fault.
0x0000000000000000 in ?? ()
(gdb) bt
#0  0x0000000000000000 in ?? ()
#1  0x00000000004e4bcc in connection_transition_h2 (h2r=0x619000000a80, 
    con=0x619000000a80) at connections.c:471
#2  0x00000000004e164b in connection_state_machine_loop (r=0x619000000a80, 
    con=0x619000000a80) at connections.c:643
#3  0x00000000004e12b3 in connection_state_machine (con=0x619000000a80)
    at connections.c:826
#4  0x00000000004d7591 in server_run_con_queue (joblist=0x619000000a80, 
    sentinel=0xf24ea0 <log_con_jqueue>) at server.c:2172
#5  0x00000000004d1db9 in server_main_loop (srv=0x614000000040)
    at server.c:2228
#6  0x00000000004cb7b2 in main (argc=6, argv=0x7fffffffe518) at server.c:2320
(gdb)
```

**Reproduction method**

Provided in [reproduction.md](reproduction.md).

