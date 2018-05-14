import os, re, chardet, traceback

from mi import get_line_file_for_ioctl_function_from_gdb, get_struct_or_union_from_gdb
from utils import base_types, is_contain_special_char

'''
Given a source file, a function name, a decl line number, return command list and varibales.
'''
def parser_source_codes(gdbmi, source_name, decl_line, function_name, depth=0, list_subprograms=[]):
    # print("Open CU's source file and find copy_from_user, get the first parameter and return its name.")
    try:
        rets = ''
        print("Parse %s in\n%s:%d" %( function_name, source_name, decl_line))

        with open(source_name, "rb") as cf:
            result = chardet.detect(cf.read())
            if result['encoding'] == 'GB2312':
                print("Fucking encoding GB2312")
                cmd = 'iconv -f gb2312 -t utf-8 %s -o %s' % (source_name, source_name)
                os.system(cmd)
        #cmd = 'dos2unix %s' % source_name
        #os.system(cmd)
        with open(source_name, 'r') as f:
            source_codes = f.readlines()

        DW_AT_decl_line = decl_line
        #print('Start line: %d' % DW_AT_decl_line)

        # Try to find lines of this subprogram, and find the copy_from_user function's first parameter.
        # Use a stack to store {}, if stack is empty, then the function is ended.
        braces_stack = 0
        cmds_args_list = []
        last_macro = ''
        for line_num in range(DW_AT_decl_line -1, len(source_codes)):
            line = source_codes[line_num]
            # print(line)
            braces_stack += line.count('{') - line.count('}')
            if braces_stack == 0 and line_num - DW_AT_decl_line >5:
                print("End line: %d" % (line_num +1))
                break
            if 'case' in line and ':' in line:
                try:
                    command_macro = line[line.index('case') + 4: line.index(':')].strip()
                    if '/' in command_macro: # May be a comment here like HIFI_MISC_IOCTL_ASYNCMSG /* comment here */
                        command_macro = command_macro[0: command_macro.index('/')].strip()
                    if command_macro != '' and ' ' not in command_macro and len(command_macro ) >5:
                        # Found Cmd:1090549505:START
                        if last_macro != '':
                            #print('Found Cmd:%s:END\n' % last_macro)
                            rets += 'Found Cmd:%s:%s@%s:END\n' % (source_name, function_name, last_macro)
                        last_macro = command_macro
                        cmds_args_list.append(command_macro)
                        #print('Found Cmd:%s:START' % command_macro)
                        rets += 'Found Cmd:%s:%s@%s:START\n' % (source_name, function_name, command_macro)
                except:
                    traceback.print_exc()
                    pass

            elif 'copy_from_user' in line:

                if 'copy_from_user_preempt_disabled' in line:
                    arg_start_index = line.index('copy_from_user_preempt_disabled')# + len('copy_from_user_preempt_disabled')
                    copy_from_user_name = 'copy_from_user_preempt_disabled'
                else:
                    arg_start_index = line.index('copy_from_user')# + len('copy_from_user')
                    copy_from_user_name = 'copy_from_user'

                arg_end_index = arg_start_index
                # .*copy_from_user( word, word, word).*

                tail = line[arg_end_index:].strip().replace(' ', '')
                # print('tail=%s' % tail)
                try:
                    first_arg = re.match(r'%s\((.*),' % copy_from_user_name, tail, re.I).group(1)
                    #first_arg = re.match(r'copy_from_user\((.*),', tail, re.I).group(1)
                    if ',' in first_arg:
                        first_arg = first_arg[0:first_arg.find(',')]
                except:
                    try:
                        tail += source_codes[line_num +1].strip().replace(' ', '')
                        first_arg = re.match(r'\((.*),(.*),(.*)\)', tail, re.I).group(1)
                    except:
                        # print("match %s error." % line)
                        continue
                while first_arg[0] == '&' or first_arg[0] == '*':
                    first_arg = first_arg[1:]
                # print("Found first arg")
                if first_arg != '' and ',' not in first_arg and '(' not in first_arg and ' ' not in first_arg and '<' not in first_arg:
                    if '[' in first_arg:
                        first_arg = first_arg[0:first_arg.index('[')]
                    #print('STARTTYPE')
                    #print(first_arg)
                    #print('ENDTYPE')
                    print('find variable %s in :' % first_arg)
                    print('%s:%d' % (source_name, line_num+1))
                    rets += 'STARTTYPE\n%s#%s\nENDTYPE\n' % (function_name, first_arg)
                    # Only keep the biggest struct, it will recover all the substruct.
                    cmds_args_list.append(first_arg.split('->')[0].split('.')[0])

            elif False and 'copy_to_user' in line:
                # copy_to_user will not cause problem.
                # No need to handle it.
                if 'copy_to_user_preempt_disabled' in line:
                    arg_start_index = line.index('copy_to_user_preempt_disabled') + len('copy_to_user_preempt_disabled')
                else:
                    arg_start_index = line.index('copy_to_user') + len('copy_to_user')
                arg_end_index = arg_start_index
                # .*copy_from_user( word, word, word).*
                tail = line[arg_end_index:].strip().replace(' ', '')
                # print('tail=%s' % tail)
                try:
                    first_arg = re.match(r'\((.*),(.*),(.*)\)', tail, re.I).group(2)
                except:
                    try:
                        tail += source_codes[line_num +1].strip().replace(' ', '')
                        first_arg = re.match(r'\((.*),(.*),(.*)\)', tail, re.I).group(2)
                    except:
                        # print("match %s error." % line)
                        continue
                while first_arg[0] == '&' or first_arg[0] == '*':
                    first_arg = first_arg[1:]

                if first_arg != '' and ',' not in first_arg and '(' not in first_arg and ' ' not in first_arg and '<' not in first_arg:
                    if '[' in first_arg:
                        first_arg = first_arg[0:first_arg.index('[')]
                    #print('STARTTYPE')
                    print('find variable %s in :' % first_arg)
                    print('%s:%d' % (source_name, line_num+1))
                    #print('ENDTYPE')
                    rets += 'STARTTYPE\n%s#%s\nENDTYPE\n' % (function_name, first_arg)
                    # Only keep the biggest struct, it will recover all the substruct.
                    cmds_args_list.append(first_arg.split('->')[0].split('.')[0])

            elif '(' in line:
                # head = line[0:line.index('(')]
                start = 0
                subfuncs = ['if', 'for', 'while', 'sizeof', 'copy_from_user', 'copy_to_user', 'printk', 'mutex_lock', 'mutex_unlock', 'switch']
                if not likely_ioctl(function_name, line, depth):
                    continue

                for i in range(line.count('(')):
                    # First get the function name.
                    func = ''
                    start = line.index('(', start)
                    head = line[0:start].strip().replace('\t', ' ')
                    if ' ' in head:
                        func = head[head.rfind(' ') +1:]
                    else:
                        func = head
                    print('call function \'%s\' at' % func)
                    print('%s:%d' % (source_name, line_num + 1))
                    # if len(func) > 0 and func not in called_fucnts_list and func not in subfuncs:
                    #    called_fucnts_list.append(func)

                    if func not in list_subprograms and func not in subfuncs:  # Some function we need not to check
                        list_subprograms.append(func)
                        #fDIE = find_subprogram_by_name(CU, func)
                        decl_line, source_file = get_line_file_for_ioctl_function_from_gdb(gdbmi, func)
                        #Some function may be inlined, and can not find definition from gdb.
                        #Use ctags to get the definition line.

                        print('function \'%s\' decl at' % func)
                        print('%s:%d' % (source_file, decl_line + 1))
                        if source_file != '':
                            child_rets = handle_subprogram(gdbmi, source_name=source_file, decl_line=decl_line, function_name = func, depth=depth + 1, list_subprograms=list_subprograms)
                            if child_rets is not None:
                                rets += child_rets
        if last_macro != '':
            #print('Found Cmd:%s:END\n' % last_macro)
            rets += 'Found Cmd:%s:%s@%s:END\n' %(source_name, function_name, last_macro)
        return rets
    except:
        traceback.print_exc()
        return None

def likely_ioctl(fatherf, line, depth):
    return True
    keywords = ['ioctl', 'cmd', 'do', 'route', 'arg', 'usr']
    if depth == 0:
        keywords += fatherf.split('_')

    for kw in keywords:
        if kw in line:
            return True
    return False
'''
Given a source file, a function name, a decl line number, return command list and varibales.
'''
def handle_subprogram(gdbmi, source_name, decl_line, function_name, depth=0, list_subprograms=[]):
    #Firstly handle every subprogram, use objdump to get the called subprogram's name,
    #Then find the cooresponding DIE and handle it.
    if depth > 2:
        print('Call %s reach max depth' % function_name)
        return None
    total_cmds_vars = ''

    #print('handling subprogram:%s' % function_name)
    if True: #is_copy_to_from_user_occur:
        #print("Found copy_from_user used.")
        list_subprograms.append(function_name)
        cmds_vars = parser_source_codes(gdbmi, source_name, decl_line, function_name, depth, list_subprograms)
        if cmds_vars is not None:
            total_cmds_vars += cmds_vars
    else:
        pass
    #Only the first level of unlocked_ioctl will handle BEGINTYPE ENDTYPE.
    return total_cmds_vars

def get_variable_type(gdbmi, function_name, variable_name):
    #print('Try to determine the type of %s:%s ' % (function_name, variable_name))
    decl_line, sourcefile = get_line_file_for_ioctl_function_from_gdb(gdbmi, function_name)
    #print('%s:%s' % (sourcefile, decl_line))
    line_count = 0
    if os.path.exists(sourcefile):
        f = open(sourcefile,'r')
        lines = f.readlines()
        f.close()
        bracket_count = 0
        for line in lines[decl_line-1:]:
            line_count += 1

            bracket_count += line.count('{')
            bracket_count -= line.count('}')

            if bracket_count == 0 and line_count>5:
                break
            statements = line.split(';')
            for statement in statements:
                statement = statement.strip().replace('*', ' * ').replace('[', ' [ ').replace('(', ' ( ')
                tokens = statement.split(' ')
                if variable_name in tokens:
                    #print(statements)
                    #print('find statement %s' % statement)
                    type_statement = ' '.join(tokens[0:tokens.index(variable_name)])

                    if '*' in type_statement:
                        type_statement = type_statement[0:statement.index('*')].strip()

                    if not is_contain_special_char(type_statement):
                        #print('find type_statement \'%s\'' % type_statement)
                        return type_statement

    #print('%s:%s' % (sourcefile, decl_line+line_count))

    return ''
