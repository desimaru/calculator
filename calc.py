# -*- coding: UTF_8 -*-
from math import factorial
from re import compile as rcompile


def delempty(array: list) -> list[str]:
    """配列の空要素を消す関数

    Args:
        lis (list[Any]): 空要素を消したい配列

    Returns:
        list[Any]: 空要素が消えた配列
    Note:
        元の配列の空要素も消える
    """
    while "" in array:
        array.remove("")
    return array


def indexfind(li: list, felem) -> int:
    """要素の位置を返す関数

    任意の要素が配列に含まれていない場合に-1を返す関数

    Args:
        li (list):探したい配列
        felem (any):探したい要素
    Returns:
        int: 要素の位置 無い場合は-1を返す
    Examples:
        >>>indexfind([1,2,3],2)
        2
        >>>indexfind(["hoge","huga"],"foo")
        -1
    """
    if felem in li:
        return li.index(felem)
    return -1


def fact(f: list) -> None:
    """渡された配列の!がある1個前の部分を階乗する"""
    while "!" in f:
        index = f.index("!")
        if not str(f[index - 1]).isdigit():
            # 自然数ではない場合
            if int(f[index - 1]) < 0:
                # 負の数の場合
                f[index - 1] = f"-{factorial(abs(int(f[index-1])))}"
                # 絶対値の階乗のマイナス
                f.pop(index)
        else:
            # 普通の階乗
            f[index - 1] = str(factorial(int(f[index - 1])))
            f.pop(index)


def lpow(formula: list) -> None:
    """渡された配列をべき乗する"""
    while "^" in formula:
        index = formula.index("^")
        formula[index - 1] = str(
            float(formula[index - 1]) ** float(formula.pop(index + 1))
        )
        formula.pop(index)


pettern = rcompile(r"^-?\d+\.?\d*?$")


def brackets(formula: list, bracket: str) -> list:
    """配列の括弧を探して計算する関数"""
    while bracket[0] in formula:
        index = indexfind(formula, bracket[0])
        index2 = indexfind(formula, bracket[1])
        if index != 0 and bool(pettern.match(str(formula[index - 1]))):
            e = calc(formula[index + 1:index2])
            del formula[index + 1:index2]
            formula[index] = e * float(formula.pop(index - 1))
            formula.pop(index - 1)
        elif (len(formula) != index2 and
                pettern.match(str(formula[index2 + 1]))):
            e = calc(formula[index + 1:index2])
            del formula[index + 1:index2]
            formula[index] = e * float(formula.pop(index2 + 1))
        else:
            formula[index] = calc(formula[index + 1:index2])
            del formula[index + 1:index2 + 1]
    return formula


def calc(formula: list) -> float:
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
            1:[]
            2:{}
            3:()
            4:!
            5:^
            6:*、/、%
            7:+、-
    """
    brackets(formula, "[]")
    brackets(formula, "{}")
    brackets(formula, "()")
    fact(formula)
    lpow(formula)
    while "*" in formula or "/" in formula or "%" in formula:
        index = indexfind(formula, "*")
        index2 = indexfind(formula, "/")
        index3 = indexfind(formula, "%")
        if (index2 != -1) and (
            (index2 < index and index2 < index3) or (
                index == -1 and index3 == -1)
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
    return float(formula[0])


def mathsplit(s: str = "", c: bool = False) -> list:
    """渡された文字列を演算子と数字で分けて返す関数"""
    b: list = []
    for i in s:
        if i.isdecimal():
            if len(b) == 0:
                b.append(i)
            else:
                b[-1] += i
        else:
            if i == ".":
                b[-1] += "."
            elif i in ("+", "-"):
                if c:
                    b.append("-" if i == "-" else "")
                else:
                    b.append(i)
                    b.append("")
            elif i in ("*", "/", "!", "^", "(", ")", "{", "}", "[", "]"):
                b.append(i)
                b.append("")
            else:
                raise ValueError("無効な演算子")
    return b


def calculator(s: str) -> str:
    """渡された文字列を評価して返す関数

    Args:
        s (str):評価したい文字列
    """
    if s == "":
        return "0"
    c = mathsplit(s, True)
    delempty(c)
    if str(x := calc(c)).endswith(".0"):
        return str(int(x))
    return str(x)


print("数式を打ってください。(quitで終了)")
while (a := input()) != "quit":
    try:
        print(calculator(a))
    except (ValueError, IndexError, OverflowError, ZeroDivisionError):
        print("無効な値です")
