
class myObj():
    def __init__(self, x) -> None:
        self.__x = x
    def get_val(self):
        return self.__x




list = [myObj(10), myObj(2)]


def find_min(target_list) -> int:
    min_index = 0

    for i in range(len(target_list)):
        if target_list[i].get_val() < target_list[min_index].get_val():
            min_index = i

    return min_index


print(find_min(list))