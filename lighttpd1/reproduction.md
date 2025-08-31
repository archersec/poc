# Reproduction Steps

1. Run:
```shell
docker build . -t vul-lighttpd1
cid=$(docker run -dit --cap-add=SYS_PTRACE --security-opt seccomp=unconfined vul-lighttpd1 bash)
docker cp replay.py $cid:/home/ubuntu
docker cp vul $cid:/home/ubuntu
```

2. Enter the container:
```shell
docker exec -it $cid bash
```

3. Run:
```shell
cd $WORKDIR
gdb lighttpd1/src/lighttpd
```

```shell
(gdb) r -D -f /home/ubuntu/experiments/lighttpd.conf -m /home/ubuntu/experiments/lighttpd1/src/.libs
```

4. Open another terminal, enter the same container, and run:
```shell
# to replay vulnerability #1
python3 replay.py -i vul/1-connections.c-471
```
