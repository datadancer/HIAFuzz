
base_types = ['int', 'unsigned int', 'float', 'char', 'unsigned char', 'double', 'long', 'unsigned long',
                   'unsigned long int', 'short', 'unsigned short', 'unsigned long long', 'void']

kernel_root = ''
ctags = []

def is_contain_special_char(statement):
    special_chars = ['.','-','<','>','(',')','*','!','@','#','$','%','^','&','+','=',
                     '/','\\','|',',','?','~','`', '{', '}','\'', '\"', ';']
    for achar in special_chars:
        if achar in statement:
            return True
    return False