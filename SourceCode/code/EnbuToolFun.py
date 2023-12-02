# 往文件内写内容
def written_file(attribute_dict):
    keys = ['Month', 'Count', 'Mode', 'FontSize', 'timi', 'SecretId', 'SecretKey']

    data = "####请不要随意更改此文件内容####\n"
    for name in keys:
        data += name + ":" + str(attribute_dict[name]) + "\n"
    with open('..\data\model.txt', 'w') as file_handle:
        file_handle.write(data)  # 写入
        file_handle.write('\n')

# 从文件中读信息
def read_file():
    model = open('..\data\model.txt', encoding='gb18030', errors='ignore')
    data = model.readlines()  # 直接将文件中按行读到list里
    model.close()  # 关
    ans = {}
    for line in data[1:]:
        t = ''
        for i in range(len(line) - 2, -1, -1):
            if line[i] == ":":
                ans[line[:i]] = t
                break
            t = line[i] + t
    ans["Month"] = int(ans["Month"])
    ans["Count"] = int(ans["Count"])
    ans["Mode"] = int(ans["Mode"])
    ans["timi"] = int(ans["timi"])
    ans["FontSize"] = int(ans["FontSize"])
    return ans

if __name__ == "__main__":
    print(read_file())