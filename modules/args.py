from flask import Flask , request
def chk_arg(arg):
    if request.args.get(arg) is None:
        if arg is 'tags':
            return 0
        elif arg is 'vals':
            return 1
    else:
        if arg is 'tags':
            return request.args.get(arg).split(",")
        elif arg is 'vals':
            return request.args.get(arg).split(",")