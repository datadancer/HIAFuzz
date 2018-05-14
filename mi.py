'''
This file provides function relate to c source code analyze.
get_struct_or_union_from_gdb
'''
import re, time, os
from utils import base_types, is_contain_special_char
import subprocess

kernel_root = ''

'''
Given a struct name, return the definition of the struct.
'''

def get_struct_or_union_from_gdb(gdbmi, struct_name):
    deps = [struct_name]
    all_struct = [struct_name]
    ccodes = {}
    all_struct += base_types
    while len(deps) > 0:
        sname = deps.pop().strip()
        if sname == '':
            continue
        #print('sname=%s' % sname)
        ccodes[sname] = ''
        ptype_cmd = 'ptype %s' % sname
        #print(ptype_cmd)
        response = gdbmi.write(ptype_cmd,  timeout_sec=20)
        #print(response)
        is_typedef_struct = False
        #print(response)
        for message in response:
            if message['stream'] == 'stdout' and message['payload'] is not None:
                if type(message['payload']) != str:
                    #print(type(message['payload']))
                    print('Not str')
                    continue

                if message['payload'].replace('\\n', '') == ptype_cmd:
                    continue
                if 'A syntax error in expression' in message['payload']:
                    break
                if '\\\\\\\\\\' in message['payload']:
                    break

                line = message['payload'].replace('\\n', '\n').replace('type = ', '')
                # print(line)

                if 'struct' in sname or 'union' in sname:  # Check depended types.
                    ccodes[sname] += line
                    if ':' in line:
                        # statements like     '__u8 reserved1      : 2;'
                        line = line[0:line.find(':')].strip()

                    typename = line[0:line.rfind(' ')].strip()
                    #print(line)
                    #print('typename=%s' % typename)
                    if typename not in all_struct and not is_contain_special_char(typename) and typename !='' and 'ptype' not in typename:
                    #if typename not in all_struct and 'struct' in typename and '}' not in typename:
                        deps.append(typename)
                        all_struct.append(typename)
                        print('add new type %s' % typename)
                elif 'enum' in sname or 'enum' in line:  # enum type
                    ccodes[sname] += line.replace(',', ',\n').replace('{','{\n').replace('}','\n}')
                elif 'struct' in line or is_typedef_struct: #special typedef struct {...}
                    if 'struct' in line:#The first line of typedef struct
                        ccodes[sname] += 'typedef %s' % line
                        is_typedef_struct = True
                    elif line == '}\n':
                        ccodes[sname] += '} %s\n' % sname
                    else: # the flowing line
                        ccodes[sname] += line
                else:  # normal typedef
                    uppertype = line.strip()
                    ccodes[sname] += 'typedef %s %s\n' % (uppertype, sname)
                    #if uppertype not in all_struct and '}' not in uppertype and uppertype != '' and 'ptype' not in uppertype:
                    if uppertype not in all_struct and 'struct' in uppertype and not is_contain_special_char(uppertype):
                        deps.append(uppertype)
                        all_struct.append(uppertype)
                        print('add new type %s' % uppertype)

        if len(ccodes[sname]) > 0 and ccodes[sname][-1] != ';':
            ccodes[sname] = ccodes[sname][0:-1] + ';\n'
        #print(ccodes[sname])
    return ccodes

'''
Given a function name, return the line and file name of the function.
'''

def get_kernel_root(gdbmi):
    global kernel_root
    if kernel_root == '':
        info_command = 'info line tty_ioctl'
        response = gdbmi.write(info_command, timeout_sec = 20)
        line_index = len(response)
        for i in range(len(response)):
            if 'Line' in response[i]['payload']:
                #/workspace/difuze/AndroidKernels/huawei/P9/kernel/drivers/tty/tty_io.c
                line_file_str = response[i]['payload']
                kernel_root = re.match(r'.*"(.*)\\"', line_file_str).group(1)
                kernel_root = kernel_root[0:len(kernel_root) - len('drivers/tty/tty_io.c')]
                break
    print('kernel_root = %s' % kernel_root)
    return kernel_root

def get_symble_file_from_ctags(gdbmi, function_name):
    kernel_root = get_kernel_root(gdbmi)
    tags_file_path = os.path.join(kernel_root, 'tags')
    print(tags_file_path)
    if not os.path.exists(tags_file_path):
        print('%s not exists' % tags_file_path)
        return ''
    p = subprocess.Popen(['grep', '^%s\t' % function_name, tags_file_path], stdout=subprocess.PIPE)
    p.wait()
    tag = str(p.stdout.readline(), encoding='utf-8')
    print(tag)
    file_name = os.path.join(kernel_root, tag.split('\t')[1])
    return file_name

def get_line_file_for_ioctl_function_from_gdb(gdbmi, function_name, allow_multi = False):
    info_command = 'info line %s' % function_name
    file_line_dict = {}

    try:
        response = gdbmi.write(info_command, timeout_sec=20)
        line_index = len(response)
        #print(line_index)
        print(response)

        for i in range(len(response)):
            #print(response[i]['payload'])
            if response[i]['payload'] is None:
                continue
            if 'Function' in response[i]['payload'] and 'not defined' in response[i]['payload'] and function_name in response[i]['payload']:
                if allow_multi:
                    return file_line_dict
                else:
                    return -1, ''

            #print('line_index=%d' % line_index)
            if response[i]['payload'].find('Line') >= 0:
                if function_name not in response[i]['payload']:
                    #Function inline by gcc may contains Line, but no it's name.
                    #Use ctags to find the line number.
                    print('Find inlined function %s\'s declication' % function_name)
                    line_file_str = response[i]['payload']
                    print(line_file_str)
                    #file_name = line_file_str[line_file_str.find('\\"') + 2 : line_file_str.rfind('\\"')]
                    file_name = re.match(r'.*"(.*)\\"', line_file_str).group(1)
                    print(file_name)

                    tags_file_path = os.path.join(get_kernel_root(gdbmi), 'tags')
                    print(tags_file_path)
                    if not os.path.exists(tags_file_path):
                        print('%s not exists' % tags_file_path)
                        break
                    line_number = -1
                    print("Try to open %s" % tags_file_path)


                    #with open(tags_file_path, 'r') as f:
                    try:
                        #tags = f.readlines()
                        if True:
                            p = subprocess.Popen(['grep', '^%s\t' % function_name,tags_file_path], stdout=subprocess.PIPE)
                            p.wait()
                            tag = str(p.stdout.readline(), encoding='utf-8')
                            #tag = f.readline()
                            while tag:
                                if tag.find(function_name) == 0:
                                    print(tag)
                                    decl_line = tag.split('\t')[2]
                                    file_name = os.path.join(kernel_root, tag.split('\t')[1])
                                    decl_line = decl_line[2:-4].strip()
                                    print(decl_line)
                                    print(file_name)
                                    with open(file_name, 'r') as ff:
                                        sourcecodes = ff.readlines()
                                        print(sourcecodes)
                                        for ii in range(len(sourcecodes)):
                                            if sourcecodes[ii].strip() == decl_line:
                                                line_number = ii + 1
                                                break
                                    break
                                tag = str(p.stdout.readline(), encoding='utf-8')
                    except:
                        print('Error %s' % tags_file_path)
                        pass
                else:
                    line_file_str = response[i]['payload']
                    print(line_file_str)
                    line_number = int(re.match(r'Line (\d+)', line_file_str).group(1))
                    file_name = re.match(r'.*"(.*)\\"', line_file_str).group(1)
                    print(line_number)
                    print('got line file:\n%s:%d' % (file_name, line_number))

                if not allow_multi:
                    return line_number-1, file_name
                else:
                    file_line_dict[file_name] = line_number-1
    except:
        pass
        #print('Error:')
        #for msg in response:
        #    print(msg['payload'])
    #Only for dev_ioctl

    if allow_multi:
        return file_line_dict
    else:
        return -1, ''

def get_macro_from_gdb(gdbmi, function_name, macro):
    print('%s:%s' % (function_name, macro))
    if macro.isdigit():
        return macro

    if function_name is not None:
        response = gdbmi.write('list %s' % function_name, timeout_sec=10)

    #Try multi times, gdb may act unexpectly.
    for i in range(5):
        response = gdbmi.write('p %s' % macro, timeout_sec=10)
        if len(response) < 2:
            print('Wait for 5 second to try %dth times.' % i)
            time.sleep(5)
        else:
            break

    if len(response) < 2:
        print(response)
        return '0'
    result_line = ''
    for msg in response:
        if '$' in msg['payload']:
            result_line = msg['payload']
            print(result_line)
            break
    if result_line == '':
        print(response)
        return '1'

    if macro in result_line:
        enumtype_dict = get_struct_or_union_from_gdb(gdbmi, macro)
        enumtype = enumtype_dict[macro]
        #(gdb) ptype ROUTE_SHB_PORT
        #type = enum port {ROUTE_SHB_PORT = 1, ROUTE_MOTION_PORT, ROUTE_CA_PORT, ROUTE_FHB_PORT}
        print(enumtype)
        if enumtype != '' and '{' in enumtype and '}' in enumtype:
            enums = enumtype[enumtype.find('{'): enumtype.rfind('}')]
            elem_list = enums.split(',')
            gap = 0
            last_val = 0
            for i in range(len(elem_list)):
                if '=' in elem_list:
                    last_val = int(elem_list.split('=')[2].strip())
                    gap = 0
                else:
                    gap += 1
                if macro in elem_list[i]:
                    #find macro in enums, then determin its value.
                    return str(gap+last_val)
    else:
        try:
            reObj = re.match(r'\$(\d+) = (\d+)', result_line)
            if reObj is not None:
                cmd_value = reObj.group(2)
                return cmd_value
        except:
            pass
    #TODO: Some macro value can not print, need to find it's definition file and print it.
    print("Can not get macro \'%s:%s\'" % (function_name,macro))
    print(response)
    return '1'

def gdb_sizeof_type(gdbmi, type_name):
    psizeof = 'p sizeof(%s)' % type_name
    response = gdbmi.write(psizeof, timeout_sec=10)
    if response is not None:
        #$1 = 4
        try:
            line = response[1]['payload']
            reObj = re.match(r'\$(\d+) = (\d+)', line)
            if reObj is not None:
                cmd_value = reObj.group(2)
                return int(cmd_value)
        except:
            pass
        return 4