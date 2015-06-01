#!/usr/bin/python3

import sys
import subprocess
import pexpect
import re

def compile():
    status = subprocess.call('gcc src.c -o src', shell=True)
    assert status == 0

def write(s):
    with open('src.c', 'w') as f:
        f.write(s)

def main():
    s = raw_input()
    l = len(s)
    s = s.replace('\\', r'\\\\')
    src = r"""
    void main() {{
        __asm__ (
            "movl $1, %eax;\n"  /* 1 is the syscall number for write */
            "movl $1, %ebx;\n"  /* 1 is stdout and is the first argument */
            // "movl $message, %esi;\n" /* load the address of string into the second argument*/
            // instead use this to load the address of the string 
            // as 16 bytes from the current instruction
            "leal 16(%eip), %esi;\n"
            "movl ${1}, %edx;\n"  /* third argument is the length of the string to print*/
            "syscall;\n"
            // call exit (so it doesn't try to run the string Hello World
            // maybe I could have just used ret instead
            "movl $60,%eax;\n"
            "xorl %ebx,%ebx; \n"
            "syscall;\n"
            // Store the Hello World inside the main function
            "message: .ascii \"{0}\";"
        );
    }}
    """.format(s, l)
    
    write(src)
    compile()
    
    child = pexpect.spawn('gdb ./src')
    child.expect("(gdb) ")
    child.sendline('disass main')
    child.expect("[\s\S]*")
    child.sendline('quit')
    child.expect(pexpect.EOF)
    last_line = child.before.split('\n')[-4]
    num_of_bytes = int(re.search("<\+(\d+)>", last_line).group(1)) / 4 + 1
    
    child = pexpect.spawn('gdb ./src')
    child.expect("(gdb) ")
    child.sendline('x/{0}dw main'.format(num_of_bytes))
    child.expect("[\s\S]*")
    child.sendline('quit')
    child.expect(pexpect.EOF)
    nums = [re.search(">:([-\t\d]+)\r", line).group(1).strip().split('\t')
                      for line in child.before.split('\n')[1:-2]]
    
    nums = [item for sublist in nums for item in sublist]
    
    src = "const int main[] = {{{}}};".format(",".join(nums))
    
    print(src)
    
    write(src)
    compile()

if __name__ == "__main__":
    main()