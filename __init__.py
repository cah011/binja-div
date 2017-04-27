from binaryninja import *

# def find_mul(bv, function):
#     il = function.low_level_il
#     for bb in il.basic_blocks:
#         il_instr_count = 0
#         for instruction in bb:
#             if 'mulu.dp' in str(instruction):
#                 yield instruction, il_instr_count

def parse_mul(function, bb, instr):
    a_val = 0
    b_val = 0

    instruction = bb[instr]

    reg1 = str(instruction).split('(')[1].split(')')[0].split(',')[0]
    reg2 = str(instruction).split('(')[1].split(')')[0].split(',')[1].replace(" ", "")

    reg1_val = function.get_reg_value_at_low_level_il_instruction(instr, reg1)
    if 'entry' not in str(reg1_val):
        a_str = str(reg1_val).split(' ')[1].replace('>','')
        a_val = int(a_str, 16)

    reg2_val = function.get_reg_value_at_low_level_il_instruction(instr, reg2)
    if 'entry' not in str(reg2_val):
        b_str = str(reg2_val).split(' ')[1].replace('>','')
        b_val = int(b_str, 16)

    if a_val > b_val :
        c_val = a_val
    else:
        c_val = b_val

    return c_val

def parse_shifts(function, bb, instr):
    instruction = bb[instr]
    return int(str(instruction).split(' ')[-1], 16)



def find_divs(bv, function):
    il = function.low_level_il
    for bb in il.basic_blocks:
        il_instr_count = 0
        a_val = 0
        b_val = 0
        mul_list = []
        shift_list = []

        for instruction in bb:
            if 'mulu.dp' in str(instruction):
                log_info(instruction)
                mul_list.append(il_instr_count)



            if '>>' in str(instruction):
                log_info(instruction)
                shift_list.append(il_instr_count)



            il_instr_count = il_instr_count + 1
        for each in mul_list:
            log_info(str(bb[each]))
            c_val = parse_mul(function, bb, each)



        shift = 0
        for each in shift_list:
            log_info(str(bb[each]))
            shift = shift + parse_shifts(function, bb, each)
            if parse_shifts(function, bb, each) == int(str(bb[shift_list[0]]).split(' ')[-1], 16) and len(shift_list) != 1:
                log_info(each)
                y_val = parse_shifts(function, bb, each)

        if len(shift_list) == 1:
            shift = shift + 32
            denominator = round(2.0**shift / c_val)
        elif len(shift_list) == 2:
            shift = shift + 32
            log_info(shift)
            log_info(c_val)
            log_info(y_val)
            denominator = round(2.0**shift / (c_val *(2.0**y_val - 1) + 2.0**32))
        elif len(shift_list) >= 3:
            log_info("I have no idea how to handle this many shifts currently!")

        last_str = "This is a divide by : " + str(denominator)
        log_info(last_str)
        addr = get_address_input("Please provide an address for the comment", "Comment Address")
        function.set_comment(addr, last_str)


PluginCommand.register_for_function("Find divides", "Finds divides", find_divs)
