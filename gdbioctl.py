#from elftools.elf.elffile import ELFFile
import os, re, time
import argparse
from utils import base_types

from cparser import handle_subprogram, get_variable_type
from pygdbmi.gdbcontroller import GdbController
from mi import get_line_file_for_ioctl_function_from_gdb, get_struct_or_union_from_gdb, get_macro_from_gdb, base_types, gdb_sizeof_type
gdbmi = None
DEBUG = False
#DEBUG = True
def get_ccodes_from_dict(recovered_struct_dict={}):

    keys = list(recovered_struct_dict.keys())
    #ordered_keys = list(keys)
    print(keys)
    print(recovered_struct_dict)
    def compare_key(key1, key2, dicts):
        if key1 == key2:
            return 0
        if key1 in dicts[key2]: # key1 < key2
            return -1
        if key2 in dicts[key1]: # key1 > key2
            return 1
        return 0

    #Need to use selection sort.
    def select_smallest_key(dicts = {}):
        # To ensure the select one is the smallest, it should be compared all the rest element.
        keys = dicts.keys()

        for potentail_key in keys:
            is_this_smallest = True
            for rest_key in keys:
                if compare_key(potentail_key, rest_key, dicts) > 0:
                    is_this_smallest = False
                    break
            if is_this_smallest:
                return potentail_key

    ordered_keys = []
    recovered_struct_dict_copy = recovered_struct_dict.copy()
    while len(recovered_struct_dict_copy) > 0:
        smallest_key = select_smallest_key(recovered_struct_dict_copy)
        ordered_keys.append(smallest_key)
        recovered_struct_dict_copy.pop(smallest_key)

    ccodes = ''
    print(ordered_keys)

    for key in ordered_keys:
        #TODO: Some complex struct may contains anonymous struct like struct {...} ptr;
        #TODO: Need to implement a gdb plugin to print struct recoursely.
        #But now just replace struct {...} to ignore it.
        if 'struct {...}' in recovered_struct_dict[key]:
            recovered_struct_dict[key] = recovered_struct_dict[key].replace('struct {...}', 'long int anon[4]');
        ccodes += recovered_struct_dict[key] + '\n'
    return ccodes

def handle_BEGINTYPE_ENDTYPE(gdbmi, rets):
    print('Before handle_BEGINTYPE_ENDTYPE')
    print(rets)
    intype = False
    lines = rets.split('\n')
    ccodes = ''
    handled_type_list = []
    recovered_struct_dict = {}
    for i in range(len(lines)):
        line = lines[i]
        if line == 'STARTTYPE':
            intype = True
            continue
        elif line == 'ENDTYPE':
            intype = False
            continue
                    
        if intype:
            if '#' in line:
                function_name, variable_name = line.strip().split('#')
                type_name = get_variable_type(gdbmi, function_name, variable_name)
                if 'struct' in type_name:
                    lines[i] = '%%%s = {}' % type_name.replace('struct ', 'struct.')
                elif 'union' in type_name:
                    lines[i] = '%%%s = {}' % type_name.replace('union ', 'union.')
                else:
                    sizeoftype = gdb_sizeof_type(gdbmi, type_name)
                    lines[i] = 'i%d' % (sizeoftype * 8)

                if type_name in base_types:
                    print('%s is base type %s' % (variable_name, type_name))
                else:
                    if type_name not in recovered_struct_dict.keys():
                        sub_recovered_struct_dict = get_struct_or_union_from_gdb(gdbmi, type_name)
                        for key, value in sub_recovered_struct_dict.items():
                            recovered_struct_dict[key] = value
            else:
                print('intype but no #')
                print(line)

            '''        
            if '.' in varname or '->' in varname:
                if '.' in varname:
                    varnames = varname.split('.')
                elif '->' in varname:
                    varnames = varname.split('->')                
                print('.->'.join(varnames))
            '''

    # remove duplicated structs.
    ccodes = get_ccodes_from_dict(recovered_struct_dict)
    structs_list = []
    backup_ccodes = ccodes
    print(ccodes)
    return '\n'.join(lines), ccodes

def assign_macros(gdbmi, cmdstypes):
    #Found Cmd:%s:END
    #print(cmdstypes)

    target_macro_list = []
    cmdstypes_list = cmdstypes.split('\n') 
    for cmd in cmdstypes_list:
        if 'Found Cmd' in cmd and 'START' in cmd:
            print(cmd)
            if cmd.count(':') == 3:
                acmd = cmd[cmd.index(':')+1:cmd.rindex(':')]

                if acmd not in target_macro_list and not acmd.isdigit():
                    target_macro_list.append(acmd)

    if target_macro_list == []:
        return cmdstypes
    print(target_macro_list)
    #gdbinit = 'file %s\n' % vmlinux
    macro_value = {}
    for func_macro in target_macro_list:
        func, macro = func_macro.split('@')
        macro_value[func_macro] = get_macro_from_gdb(gdbmi, func, macro)
    print(macro_value)

    for i in range(len(cmdstypes_list)):
        cmd = cmdstypes_list[i]
        if 'Found Cmd' in cmd:
            #print(cmd)
            if cmd.count(':') == 3:
                acmd = cmd[cmd.index(':') + 1:cmd.rindex(':')]      
                if acmd in macro_value.keys():
                    cmdstypes_list[i] = cmd.replace(acmd, macro_value[acmd])
    cmdstypes = '\n'.join(cmdstypes_list)
    #print(cmdstypes)
    return cmdstypes
    
def main():
    parser = argparse.ArgumentParser()
    # Ex: python3 gdbioctl.py -v /workspace/difuze/AndroidKernels/kindle_fire_7/WORKSPACE_DIR/out2/vmlinux -f /workspace/difuze/AndroidKernels/kindle_fire_7/WORKSPACE_DIR/out/kindle7_device_ioctl.txt
    # Ex: python3 gdbioctl.py -v /workspace/difuze/AndroidKernels/kindle_fire_7/WORKSPACE_DIR/out2/vmlinux -f /workspace/difuze/AndroidKernels/kindle_fire_7/WORKSPACE_DIR/out/kindle7_device_ioctl.txt
    #parser.add_argument('-o', action='store', dest='ioctl_out', help='Destination directory where all the generated interface should be stored.')
    parser.add_argument('-v', action='store', dest='vmlinux', help='Path of the vmlinux image. The recovered ioctls are stored in this folder.')
    parser.add_argument('-f', action='store', dest='device_ioctl_file', help='The file that conations ioctl and corresponding device file names, Ex: /dev/alarm alarm_ioctl.')
    olddir = os.getcwd()

    parsed_args = parser.parse_args()
    print('%s:%s' % (parsed_args.device_ioctl_file, 5))
    #Before make vmlinux, these steps should be taken.
    '''
    for f in `find . -name Makefile`; do sed -i "s/-g /-g3 /g" $f; done
    for f in `find . -name Makefile`; do sed -i "s/-g$/-g3/g" $f; done
    With make, add this CONFIG_DEBUG_SECTION_MISMATCH=y flag to xxxdeconfig.
    '''
    #Add flag: -fno-inline-functions-called-once

    outdir = os.path.join(os.path.dirname(parsed_args.vmlinux), 'ioctl_finder_out')
    outdir2 = os.path.join(os.path.dirname(parsed_args.vmlinux), 'ioctl_preprocessed_out')

    if not os.path.exists(outdir):
        os.mkdir(outdir)
    if not os.path.exists(outdir2):
        os.mkdir(outdir2)

    ioctl_set = []
    #ff = open('/workspace/difuze/AndroidKernels/huawei/mate9/fuben/Code_Opensource/out/ioctls', 'r')
    with open(parsed_args.device_ioctl_file, 'r') as ff:
        ioctl_set = [x.strip() for x in ff.readlines()]

    device_dict = {}
    ioctl_list = []
    if ' ' in ioctl_set[0]:# Contains devname
        for device_ioctl in ioctl_set:
            device_name, ioctl_name = device_ioctl.split(' ')
            device_dict[ioctl_name] = device_name
            ioctl_list.append(ioctl_name)

        ioctl_set = set(ioctl_list)
        print(device_dict)

    if DEBUG:
        ioctl_set.clear()
        ioctl_set.append('main')
    print(ioctl_set)

    #for aioctl in ioctl_set:
    for aioctl, device_name in device_dict.items():
        print('handling %s' % aioctl)
        ioctl_set.remove(aioctl)
        gdbmi = GdbController()
        response = gdbmi.write('file %s' % parsed_args.vmlinux)
        sourcefile_line_dict = get_line_file_for_ioctl_function_from_gdb(gdbmi, aioctl, allow_multi= True)
        item_count = 0
        for sourcefile, line in sourcefile_line_dict.items():
            if sourcefile == '':
                continue
            #if sourcefile[0] != '/':
            #    sourcefile = '/workspace/difuze/dwarf/test/'+sourcefile
            print('%s:%d' %(sourcefile, line))
            cmds_vars = handle_subprogram(gdbmi, source_name=sourcefile, decl_line=line, function_name=aioctl, depth=0,
                                      list_subprograms=[])
            #print(cmds_vars)
            cmdstypes, restruct = handle_BEGINTYPE_ENDTYPE(gdbmi, cmds_vars)

            if restruct is not None:
                if item_count == 0:
                    processed_filename = os.path.join(outdir2, aioctl + '.processed')
                    txt_filename = os.path.join(outdir, aioctl + '.txt')
                else:
                    processed_filename = os.path.join(outdir2, aioctl + str(item_count) + '.processed')
                    txt_filename = os.path.join(outdir, aioctl + str(item_count) + '.txt')

                with open(processed_filename,'w') as f:
                    f.write(restruct)
                    print(processed_filename+':1')
            if cmdstypes is not None:
                with open(txt_filename, 'w') as f:
                    f.write('O yeah...\n[+] Provided Function Name: %s\n' % aioctl)
                    if device_dict == {}:
                        f.write('Device Name: tododevname\n')
                    else:
                        f.write('Device Name: %s\n' % device_dict[aioctl])
                    f.write(assign_macros(gdbmi, cmdstypes))
                    f.write('Compl Preprocessed file:%s\n' % processed_filename)
                    f.write('ALL PREPROCESSED FILES:\n')
                    print(txt_filename + ':10')
            item_count += 1

        gdbmi.exit()
        time.sleep(2)

    if len(ioctl_set) == 0:
        print("All ioctl functions are found.")
    else:
        print("%d ioctl functions are not found." % len(ioctl_set))
        print(ioctl_set)
    os.chdir(olddir)
    print('Recovered interfaces are sotred in:\n%s\n%s' % (outdir, outdir2))
    print("Goodbye!")

if __name__ == "__main__":
    main()
