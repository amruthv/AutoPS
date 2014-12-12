#include <fcntl.h>
#include <limits.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/fanotify.h>
#include <sys/stat.h>
#include <sys/types.h>
#define CHK(expr, errcode) if((expr)==errcode) perror(#expr), exit(EXIT_FAILURE)
int main(int argc, char** argv) {
  int fan;
  char buf[4096];
  char pname[1024];
  char fdpath[32];
  char path[PATH_MAX + 1];
  char * cwd;
  ssize_t buflen, linklen;
  struct fanotify_event_metadata *metadata;
  FILE *fp;
  FILE *fp2;

  //cwd = getcwd(0, 0);
  cwd = "/home/httpd/AutoPS/fanotify/test";
  fp = fopen("../log.txt", "w");

  CHK(fan = fanotify_init(FAN_CLASS_NOTIF, O_RDONLY), -1);
  CHK(fanotify_mark(fan, FAN_MARK_ADD | FAN_MARK_MOUNT, 
    FAN_ACCESS | FAN_MODIFY | FAN_OPEN | FAN_CLOSE | FAN_EVENT_ON_CHILD, 
    AT_FDCWD, cwd), -1);
  for (;;) {
    CHK(buflen = read(fan, buf, sizeof(buf)), -1);
    metadata = (struct fanotify_event_metadata*)&buf;
    while(FAN_EVENT_OK(metadata, buflen)) {
      if (metadata->mask & FAN_Q_OVERFLOW) {
        printf("Queue overflow!\n");
        continue;
      }
      // int ret1 = system("ps -p 8076 -o comm= > ../log.txt");
      sprintf(fdpath, "/proc/self/fd/%d", metadata->fd);
      // snprintf(pname, sizeof pname, "%s%d%s", "sudo ps -p ", (int)metadata->pid, " -o comm= >> ../log.txt");
      fp2 = fopen("../map.txt", "a");
      fprintf(fp2, "%d: ", (int)metadata->pid);
      fflush(fp2);
      fclose(fp2);
      snprintf(pname, sizeof pname, "%s%d%s", "sudo ps -p ", (int)metadata->pid, " -o comm= >> ../map.txt");
      int ret = system(pname);
      CHK(linklen = readlink(fdpath, path, sizeof(path) - 1), -1);
      path[linklen] = '\0';
      if ((metadata->mask & FAN_ACCESS) > 0) {
        fprintf(fp, "%s read by process %d.\n", path, (int)metadata->pid);
      }
      if ((metadata->mask & FAN_OPEN) > 0) {
        fprintf(fp, "%s opened by process %d.\n", path, (int)metadata->pid);
      }
      if ((metadata->mask & FAN_MODIFY) > 0) {
        fprintf(fp, "%s modified by process %d.\n", path, (int)metadata->pid);
      }
      if ((metadata->mask & FAN_CLOSE_WRITE) > 0 ||
        (metadata->mask & FAN_CLOSE_NOWRITE) > 0) {
        fprintf(fp, "%s closed by process %d.\n", path, (int)metadata->pid);
      }
      fflush(fp);
      close(metadata->fd);
      metadata = FAN_EVENT_NEXT(metadata, buflen);
    }
  }
  fclose(fp);
}
