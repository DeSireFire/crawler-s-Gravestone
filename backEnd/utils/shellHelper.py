#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/8/11
# CreatTIME : 15:20
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import subprocess
import chardet


class ShellCommandExecutor:
    def __init__(self):
        self.output = None
        self.error = None

    def execute_command(self, command):
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.output, self.error = process.communicate()
            return process.returncode, self.output, self.error
        except Exception as e:
            return -1, None, str(e)

    def get_output_decoded(self, encoding=None):
        if encoding is None:
            result = chardet.detect(self.output)
            encoding = result['encoding']
        return self.output.decode(encoding)


# 使用示例
if __name__ == '__main__':
    shell_executor = ShellCommandExecutor()
    command = 'ipconfig'

    return_code, output, error = shell_executor.execute_command(command)

    if return_code == 0:
        print("Command executed successfully!")
        decoded_output = shell_executor.get_output_decoded()
        print("Output:\n", decoded_output)
    else:
        print("Command execution failed!")
        print("Error:\n", error)
