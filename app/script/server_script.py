#!/usr/bin/python
# coding=utf-8
#
# File Name: spark_script.py
# File Author: 姚丰利(lidey) 
# File Created Date: 2015-11-30 17:04
import os
import socket

import paramiko
import re


class ServerScript:
    def __init__(self, server):
        self.hostname = server.host
        self.username = server.name
        self.password = server.password

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.hostname, username=self.username, password=self.password)
        self.ssh = ssh

        self.transport = paramiko.Transport((self.hostname, 22))
        self.transport.connect(username=self.username, password=self.password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def command(self, shell, timeout=10):
        """

        :param shell:
        :param timeout:
        :return:
        """
        stdin, stdout, stderr = self.exec_command(shell, timeout=timeout)
        return stdout.read(), stderr.read()

    def get_connection(self):
        """

        :return:
        """
        return self.ssh

    def exec_command(self, shell, timeout=10):
        """

        :param shell:
        :param timeout:
        :return:
        """
        stdin, stdout, stderr = self.ssh.exec_command(shell, timeout=timeout)
        return stdin, stdout, stderr

    def make_dir(self, remote_directory):
        """
        Change to this directory, recursively making new folders if needed.
        Returns True if any folders were created.
        :param remote_directory:
        :return:
        """
        if remote_directory == '/':
            # absolute path so change directory to root
            self.sftp.chdir('/')
            return
        if remote_directory == '':
            # top-level relative directory must exist
            return
        try:
            self.sftp.chdir(remote_directory)  # sub-directory exists
        except IOError:
            dir_name, basename = os.path.split(remote_directory.rstrip('/'))
            self.make_dir(dir_name)  # make parent directories
            self.sftp.mkdir(basename)  # sub-directory missing, so created it
            self.sftp.chdir(basename)
            return True

    def remove_file(self, remote_file):
        """

        :param remote_file:
        :return:
        """
        self.sftp.remove(remote_file)

    def remove_dir(self, remote_directory):
        """

        :param remote_directory:
        :return:
        """
        self.sftp.rmdir(remote_directory)

    def upload(self, local_file, remote_file):
        """

        :param local_file:
        :param remote_file:
        :return:
        """
        (remote_path, file) = os.path.split(remote_file)
        self.make_dir(remote_path)
        self.sftp.put(local_file, remote_file)

    def close(self):
        """

        :return:
        """
        self.ssh.close()
        self.transport.close()


class Tty(object):
    """
    A virtual tty class
    一个虚拟终端类，实现连接ssh，基类
    """

    def __init__(self, server):
        self.hostname = server.host
        self.username = server.name
        self.password = server.password
        self.ip = None
        self.port = 22
        self.ssh = None
        self.channel = None
        self.vim_flag = False
        self.ps1_pattern = re.compile('\[.*@.*\][\$#]')

    @staticmethod
    def is_output(strings):
        newline_char = ['\n', '\r', '\r\n']
        for char in newline_char:
            if char in strings:
                return True
        return False

    @staticmethod
    def remove_obstruct_char(cmd_str):
        """
        删除一些干扰的特殊符号
        :param cmd_str:
        :return:
        """
        control_char = re.compile(r'\x07 | \x1b\[1P | \r ', re.X)
        cmd_str = control_char.sub('', cmd_str.strip())
        patch_char = re.compile('\x08\x1b\[C')  # 删除方向左右一起的按键
        while patch_char.search(cmd_str):
            cmd_str = patch_char.sub('', cmd_str.rstrip())
        return cmd_str

    @staticmethod
    def deal_backspace(match_str, result_command, pattern_str, backspace_num):
        """
        处理删除确认键
        :param match_str:
        :param result_command:
        :param pattern_str:
        :param backspace_num:
        :return:
        """
        if backspace_num > 0:
            if backspace_num > len(result_command):
                result_command += pattern_str
                result_command = result_command[0:-backspace_num]
            else:
                result_command = result_command[0:-backspace_num]
                result_command += pattern_str
        del_len = len(match_str) - 3
        if del_len > 0:
            result_command = result_command[0:-del_len]
        return result_command, len(match_str)

    @staticmethod
    def deal_replace_char(match_str, result_command, backspace_num):
        """
        处理替换命令
        :param match_str:
        :param result_command:
        :param backspace_num:
        :return:
        """
        str_lists = re.findall(r'(?<=\x1b\[1@)\w', match_str)
        tmp_str = ''.join(str_lists)
        result_command_list = list(result_command)
        if len(tmp_str) > 1:
            result_command_list[-backspace_num:-(backspace_num - len(tmp_str))] = tmp_str
        elif len(tmp_str) > 0:
            if result_command_list[-backspace_num] == ' ':
                result_command_list.insert(-backspace_num, tmp_str)
            else:
                result_command_list[-backspace_num] = tmp_str
        result_command = ''.join(result_command_list)
        return result_command, len(match_str)

    def remove_control_char(self, result_command):
        """
        处理日志特殊字符
        :param result_command:
        :return:
        """
        control_char = re.compile(r"""
                \x1b[ #%()*+\-.\/]. |
                \r |                                               #匹配 回车符(CR)
                (?:\x1b\[|\x9b) [ -?]* [@-~] |                     #匹配 控制顺序描述符(CSI)... Cmd
                (?:\x1b\]|\x9d) .*? (?:\x1b\\|[\a\x9c]) | \x07 |   #匹配 操作系统指令(OSC)...终止符或振铃符(ST|BEL)
                (?:\x1b[P^_]|[\x90\x9e\x9f]) .*? (?:\x1b\\|\x9c) | #匹配 设备控制串或私讯或应用程序命令(DCS|PM|APC)...终止符(ST)
                \x1b.                                              #匹配 转义过后的字符
                [\x80-\x9f] | (?:\x1b\]0.*) | \[.*@.*\][\$#] | (.*mysql>.*)      #匹配 所有控制字符
                """, re.X)
        result_command = control_char.sub('', result_command.strip())

        if not self.vim_flag:
            if result_command.startswith('vi') or result_command.startswith('fg'):
                self.vim_flag = True
            return result_command.decode('utf8', "ignore")
        else:
            return ''

    def deal_command(self, str_r):
        """
        处理命令中特殊字符
        :param str_r:
        :return:
        """
        str_r = self.remove_obstruct_char(str_r)

        result_command = ''  # 最后的结果
        backspace_num = 0  # 光标移动的个数
        reach_backspace_flag = False  # 没有检测到光标键则为true
        pattern_str = ''
        while str_r:
            tmp = re.match(r'\s*\w+\s*', str_r)
            if tmp:
                str_r = str_r[len(str(tmp.group(0))):]
                if reach_backspace_flag:
                    pattern_str += str(tmp.group(0))
                    continue
                else:
                    result_command += str(tmp.group(0))
                    continue

            tmp = re.match(r'\x1b\[K[\x08]*', str_r)
            if tmp:
                result_command, del_len = self.deal_backspace(str(tmp.group(0)), result_command, pattern_str,
                                                              backspace_num)
                reach_backspace_flag = False
                backspace_num = 0
                pattern_str = ''
                str_r = str_r[del_len:]
                continue

            tmp = re.match(r'\x08+', str_r)
            if tmp:
                str_r = str_r[len(str(tmp.group(0))):]
                if len(str_r) != 0:
                    if reach_backspace_flag:
                        result_command = result_command[0:-backspace_num] + pattern_str
                        pattern_str = ''
                    else:
                        reach_backspace_flag = True
                    backspace_num = len(str(tmp.group(0)))
                    continue
                else:
                    break

            tmp = re.match(r'(\x1b\[1@\w)+', str_r)  # 处理替换的命令
            if tmp:
                result_command, del_len = self.deal_replace_char(str(tmp.group(0)), result_command, backspace_num)
                str_r = str_r[del_len:]
                backspace_num = 0
                continue

            if reach_backspace_flag:
                pattern_str += str_r[0]
            else:
                result_command += str_r[0]
            str_r = str_r[1:]

        if backspace_num > 0:
            result_command = result_command[0:-backspace_num] + pattern_str

        result_command = self.remove_control_char(result_command)
        return result_command

    def get_connection(self):
        """
        获取连接成功后的ssh
        """
        # 发起ssh连接请求 Make a ssh connection
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.hostname,
                        port=self.port,
                        username=self.username,
                        password=self.password,
                        allow_agent=False,
                        look_for_keys=False)

        except paramiko.ssh_exception.AuthenticationException, paramiko.ssh_exception.SSHException:
            pass
        except socket.error:
            pass
        else:
            self.ssh = ssh
            return ssh


class WebTty(Tty):
    def __init__(self, *args, **kwargs):
        super(WebTty, self).__init__(*args, **kwargs)
        self.ws = None
        self.data = ''
        self.input_mode = False
