import sys
import threading
import uuid
from io import StringIO

import fire

from dukepy.fire.fire_root import Root
from dukepy.traces import print_exception_traces
from dukepy.fire.fire_command import FireCommand

fire_threads = []


def db_fire_cmd(cmd, source):
    def act():
        try:
            req = FireCommand(cmd=cmd, source=source)
            req.save()
        except Exception as e:
            print_exception_traces(e)

    t = threading.Thread(target=act())
    t.start()


def main():
    if len(sys.argv) > 1:
        args = ""
        for arg in sys.argv[1:]:
            args += " " + arg
        try:
            db_fire_cmd(args, "cli")
            fire.Fire(Root, args)
        except Exception as e:
            print_exception_traces(e)
        Root.cmd_history.append(args)
    else:
        print("no args...")

    # while True:
    # 	cmd = input()
    # 	fire.Fire(Root, cmd)
    # 	Root.cmd_history.append(cmd)

    pass


def fire_task_wrapper(cmd, emit, req_id=None):
    class TeeIn(StringIO):
        def write(self, s):
            # print("fire out" + str(s))
            try:
                emit('fireout', {'stdin': s, 'req_id': req_id})
            # StringIO.write(self, s)
            # sys.__stdin__.write(s)
            except Exception as e:
                # print_exception_traces(e)
                pass

    class TeeOut(StringIO):
        def write(self, s):
            # print("fire out" + str(s))
            try:
                emit('fireout', {'stdout': s, 'req_id': req_id})
            # StringIO.write(self, s)
            # sys.__stdout__.write(s)
            except Exception as e:
                # print_exception_traces(e)
                pass

    class TeeErr(StringIO):
        def write(self, s):
            # print("fire out" + str(s))
            try:
                emit('fireout', {'stderr': s, 'req_id': req_id})
            # StringIO.write(self, s)
            # sys.__stderr__.write(s)
            except Exception as e:
                # print_exception_traces(e)
                pass

    # @processify
    def fire_task(command):
        db_fire_cmd(command, "websocket")

        # Save everything that would otherwise go to stdout.
        stdin = TeeIn()
        sys.stdin = stdin

        stdout = TeeOut()
        sys.stdout = stdout

        stderr = TeeErr()
        sys.stderr = stderr

        fire.Fire(Root, command)

    pass
    # fire_task(cmd)
    t = threading.Thread(name='fire_' + str(uuid.uuid4()), target=fire_task(cmd))
    fire_threads.append(t)
    t.start()
    # t.join()
    pass


if __name__ == "__main__":
    main()
