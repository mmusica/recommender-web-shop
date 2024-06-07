import json

def process_jsonl(input_file_path, output_file_path, limit=10000):
    count = 0
    with open(input_file_path, 'r', encoding='utf-8') as infile, \
         open(output_file_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            record = json.loads(line)
            
            outfile.write(json.dumps(record) + '\n')
            
            count += 1
            if count >= limit:
                break

input_file_path = "meta_Electronics.jsonl"
output_file_path = "ME_small.jsonl"
process_jsonl(input_file_path, output_file_path, limit=10000)
