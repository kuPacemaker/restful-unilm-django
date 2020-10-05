def naver_parse_rule(key, selection):
    if key == "부작":
        return selection.text.split(" ")[-1]
    elif key == "기간":
        return " ".join(selection.text.split(" ")[1:4])

def series_parse_rule(key, selection):
    if key =="부작":
        return selection.text
    else:
        return selection.parent.text
    
def ctl_parse_rule(key, selection):
    if key == "이름":
        return selection.text.strip()
