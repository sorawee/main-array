# Main Array Generator

## Installation

Things that you should have:

1. gcc
2. gdb
3. python2.x

Run:

    $ python setup.py install

## Usage

    $ echo "I love U\n" | python gen.py > file.c

## Then?

    $ gcc file.c -o myfile
	$ ./myfile
	I love U
	$
