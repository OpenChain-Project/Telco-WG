import json
import argparse

class SchemaPath(object):
    def __init__(self, name, schema, parent=None) -> None:
        self.name = name
        self.type = schema["type"]
        self.parent = parent
        self.schema = schema
    
    def __str__(self) -> str:
        result = ""
        if self.parent is not None:
            result += str(self.parent)
            pass
        if result == "":
            result = self._get_current_str()
        else:
            result += "->" + self._get_current_str()
        return result
    
    def _get_current_str(self) -> str:
        return "{}({})".format(self.name, self.type)

    def __lt__(self, other):
        return str(self) < str(other)

def readJson(f_name):
    with open(f_name, "r") as f:
        try:
            result = json.load(f)
        except Exception as e:
            return None
        return result

def compare(lefts, rights):
    # double pos
    left_pos = right_pos = 0
    left_length = len(lefts)
    right_length = len(rights)
    commons = []
    left_right_differences = []
    right_left_differences = []
    while left_pos < left_length and right_pos < right_length:
        left = lefts[left_pos]
        right = rights[right_pos]
        if str(left) == str(right):
            commons.append([left, right])
            left_pos += 1
            right_pos += 1
        elif str(lefts[left_pos]) < str(rights[right_pos]):
            left_right_differences.append(left)
            left_pos += 1
        else:
            right_left_differences.append(right)
            right_pos += 1
    while left_pos < left_length:
        left_right_differences.append(lefts[left_pos])
        left_pos += 1
    while right_pos < right_length:
        right_left_differences.append(rights[right_pos])
        right_pos += 1
    return commons, left_right_differences, right_left_differences

def retrive_root_schema(schema):
    results = []
    def retrive(name, schema, parent=None):
        d = SchemaPath(name, schema, parent=parent)
        if d.type == "object":
            results.append(d)
            for key in schema.get("properties", {}):
                retrive(key, schema["properties"][key], d)
        elif d.type == "array":
            retrive(name+"_item", schema["items"], d)
        else:
            results.append(d)

    retrive("doc", schema)
    return sorted(results)

def compare_file(fname_1, fname_2):
    left_json_schema_paths = retrive_root_schema(readJson(f_name=fname_1))
    right_json_schema_paths = retrive_root_schema(readJson(f_name=fname_2))
    commons, left_right_differences, right_left_differences = compare(left_json_schema_paths, right_json_schema_paths)
    comparison_result = {
        "field_mandatory_comparison": {},
        "field_existence_comparison": {}
    }
    if len(left_right_differences) > 0:
        more_fields = []
        for key in left_right_differences:
            more_fields.append(str(key))
        if len(more_fields) > 0:
            comparison_result["field_existence_comparison"]["more_fields"] = more_fields
    if len(right_left_differences) > 0:
        less_fields = []
        for key in right_left_differences:
            less_fields.append(str(key))
        if len(less_fields) > 0:
            comparison_result["field_existence_comparison"]["less_fields"] = less_fields
    more_fields = []
    less_fields = []
    for key in commons:
        _, _left_right_differences, _right_left_differences = compare(sorted(key[0].schema.get("required",[])), sorted(key[1].schema.get("required",[])))
        if len(_left_right_differences) > 0:
            for _key in _left_right_differences:
                more_fields.append("{}->{}".format(str(key[0]), _key))
        if len(_right_left_differences) > 0:
            for _key in _right_left_differences:
                less_fields.append("{}->{}".format(str(key[0]), _key))
    if len(more_fields) > 0:
        comparison_result["field_mandatory_comparison"]["more_fields"] = more_fields
    if len(less_fields) > 0:
        comparison_result["field_mandatory_comparison"]["less_fields"] = less_fields
    return comparison_result

def print_result(comparison_result):
    json_str = json.dumps(comparison_result, indent=4)
    print(json_str)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="compare two json schema, such as fields and required info")
    parser.add_argument("-f", "--file", dest="file", nargs="+", help="file")
    args = parser.parse_args()
    if len(args.file) != 2:
        print("need 2 params, filenames of json schema")
        exit(-1)
    result = compare_file(args.file[0], args.file[1])
    print_result(result)
