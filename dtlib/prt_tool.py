from tabulate import tabulate


def prt_warp_code(prt_str):
    """

    :return:
    """
    print('\n```')
    print(prt_str)
    print('\n```')


def print_hist(nd_hist):
    """
    打印hist图,numpy计算出来的
    :return:
    """
    height, section = nd_hist

    sec_list = section.tolist()
    head_list = []
    for cnt in range(len(sec_list) - 1):
        head_list.append('~'.join([str(sec_list[cnt]), str(sec_list[cnt + 1])]))

    tbl = tabulate(
        [
            head_list,
            height.tolist()
        ], tablefmt='grid'
    )
    prt_warp_code(tbl)
