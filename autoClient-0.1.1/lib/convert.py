

def convert_mb2gb(value, default=0):
    """ 将MB转化为GB, 如1024MB，返回1GB"""
    try:
        v = value.strip('MB ')
        ret = int(v)//1024
    except Exception as e:
        ret = default
    return ret

