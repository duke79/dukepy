#!/usr/bin/python
import os, errno


class Hooks():
    def __init__(self):
        self.path_this_file_dir = os.path.dirname(os.path.realpath(__file__))
        path_project_root = os.path.dirname(os.path.dirname(self.path_this_file_dir))
        path_dot_git = os.path.join(path_project_root, ".git")
        self.path_hooks = os.path.join(path_dot_git, "hooks")

    def symlink_force(self, target, link_name):
        """ To create symlink in root/.git/hooks/"""
        try:
            os.symlink(target, link_name)
        except OSError as e:
            if e.errno == errno.EEXIST:
                os.remove(link_name)
                os.symlink(target, link_name)
            else:
                raise e

    def create_hook_symlink(self, name, src):
        src = os.path.join(hooks.path_this_file_dir, src)
        dst = os.path.join(self.path_hooks, name)
        self.symlink_force(src, dst)
        print("symlink %s created" % (dst))

    def create_hooks(self):
        self.create_hook_symlink("pre-commit", "pre-commit.py")
        self.create_hook_symlink("pre-push", "pre-push.py")

if __name__ == "__main__":
    hooks = Hooks()
    hooks.create_hooks()
