


lines_list = []

with open("valid_skincare_urls_1-28.txt", "r") as urls:
    lines = urls.readlines()
    for line in lines:
        line = line.rstrip()
        lines_list.append(line)

    lines_list = list(set(lines_list))

    with open("valid_skin_urls.txt", "w") as dedup_urls:
        for line in lines_list:
            dedup_urls.write(line+"\n")        

    