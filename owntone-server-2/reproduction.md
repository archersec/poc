# Reproduction Steps

1. Run:

   ```shell
   docker build . -t vul-owntone
   cid=$(docker run -dit --privileged vul-owntone bash)
   docker cp vul $cid:/home/ubuntu
   ```
2. Enter the container:

   ```shell
   docker exec -it $cid bash
   ```
3. Configure OwnTone:

   ```shell
   #Network deamons needed by OwnTone
   sudo /etc/init.d/dbus start
   sudo /etc/init.d/avahi-daemon start
   
   sudo /etc/init.d/dbus status
   if [ $? -ne 0 ]
   then
     echo "Unable to run DBUS"
     exit 1
   fi
   
   sudo /etc/init.d/avahi-daemon status
   if [ $? -ne 0 ]
   then
     echo "Unable to run AVAHI daemon"
     exit 1
   fi
   ```
4. Run:

   ```shell
   cd $WORKDIR
   gdb owntone/src/owntone -q
   ```

   ```shell
   (gdb) r -d 0 -c owntone.conf -f
   ```
5. Open another terminal, enter the same container.

   To reproduce the vulnerability:

   ```shell
   cat vul/1.txt | nc localhost 3689
   ```


