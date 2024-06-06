with open('PVTL02242200000387-input.trace', 'r') as trace_file:
    trace_data = trace_file.readlines()

with open('output.txt', 'w') as text_file:
    all_lines = "".join(line for line in trace_data if "SVTL" not in line)
    # print(all_lines)
    text_file.write(all_lines.strip())
    text_file.close()
