# -*- coding: UTF_8 -*-
import math

def delempty(l: list) -> list[str]:
    """配列の空要素を消す関数

    Args:
        l (list): 空要素を消したい配列

    Returns:
        list[Any]: 空要素が消えた配列
    Note:
        元の配列の空要素も消える
    """
    while "" in l:
        l.remove("")
    return l


def indexfind(li: list, st) -> int:
    """要素の位置を返す関数

    任意の要素が配列に含まれていない場合に-1を返す関数

    Args:
        li (list):探したい配列
        st (any):探したい要素
    Returns:
        int: 要素の位置 無い場合は-1を返す
    Examples:
        >>>indexfind([1,2,3],2)
        2
        >>>indexfind(["hoge","huga"],"foo")
        -1
    """
    if st in li:
        return li.index(st)
    return -1


def fact(f: list[str]) -> None:
    """渡された配列の!がある1個前の部分を階乗する"""
    while "!" in f:
        index = f.index("!")
        if not str(f[index - 1]).isdigit():
            # 自然数ではない場合
            if int(f[index - 1]) < 0:
                # 負の数の場合
                f[index - 1] = f"-{math.factorial(abs(int(f[index-1])))}"
                # 絶対値の階乗のマイナス
                f.pop(index)
        else:
            # 普通の階乗
            f[index - 1] = str(math.factorial(int(f[index - 1])))
            f.pop(index)


def lpow(l: list[str]) -> None:
    """渡された配列をべき乗する"""
    while "^" in l:
        index = l.index("^")
        l[index - 1] = str(float(l[index - 1]) ** float(l.pop(index + 1)))
        l.pop(index)


def calc(formula: list[str]) -> float:
    """引数に渡された式を評価する関数

    Args:
        formula (list):式
    Retuns:
        float:計算結果
    Examples:
        >>>calc(["10","20"])
        30
        >>>calc(["100","/","10"])
        10
    Note:
        優先順位:
            1:!
            2:^
            3:*、/、%
            4:+、-
    """
    try:
        fact(formula)
        lpow(formula)
        while "*" in formula or "/" in formula or "%" in formula:
            index = indexfind(formula, "*")
            index2 = indexfind(formula, "/")
            index3 = indexfind(formula, "%")
            if (
                (index2 != -1)
                and (
                    ((index2 < index) and (index2 < index3))
                    or ((index == -1) and (index3 == -1))
                )
            ):  # (index2が-1ではない)かつ、{(index2がindex1と3未満)または、(index1と3が両方-1の時)}
                formula[index - 1] = str(
                    float(formula[index2 - 1]) / float(formula.pop(index2 + 1))
                )
                formula.pop(index)
            elif index != -1 and (index < index3 or index3 == -1):
                formula[index - 1] = str(
                    float(formula[index - 1]) * float(formula.pop(index + 1))
                )
                formula.pop(index)
            elif index3 != -1:
                formula[index3 - 1] = str(
                    float(formula[index3 - 1]) % float(formula.pop(index3 + 1))
                )
                formula.pop(index3)
        while len(formula) > 1:
            formula[0] = str(float(formula[0]) + float(formula.pop(1)))
        p = float(formula[0])
        return p
    except (ValueError, TypeError, IndexError, OverflowError,ZeroDivisionError):
        print("無効な値です")
        return 0.0


def calculator(s: str) -> None:
    """渡された文字列を評価して出力する関数

    Args:
        s (str):評価したい文字列
    """
    b = []
    anser: float = 0.0
    if s == "":
        print(0)
        return
    u = 0
    minus = False
    for i, j in enumerate(s):
        if j.isdecimal():
            if i == 0:
                b.append(j)
            else:
                if minus:
                    b.append(f"-{j}")
                    minus = False
                    u += 1
                else:
                    b[u] += j
        else:
            if j == "-":
                minus = True
            else:
                if j != "+":
                    b.append(j)
                    b.append("")
                    u += 2
                elif j not in ("+", "-", "*", "/", "!", "^"):
                    print("無効な値です")
                    return
                else:
                    b.append("")
                    u += 1
    delempty(b)
    x = calc(b)
    if str(x).endswith(".0"):
        anser = int(x)
    else:
        anser = x
    print(anser)


print("数式を打ってください。")
while (a := input()) != "quit":
    calculator(a)
