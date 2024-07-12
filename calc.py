#!/usr/bin/env python
from math import factorial
from re import compile as rcompile


def del_empty(array: list):
    """配列の空要素を消す関数

    Args:
        lis (list[Any]): 空要素を消したい配列

    Returns:
        list[Any]: 空要素が消えた配列
    """
    while "" in array:
        array.remove("")


def indef_of(array: list, element) -> int:
    """要素の位置を返す関数

    任意の要素が配列に含まれていない場合に-1を返す関数

    Args:
        array (list):探したい配列
        element (any):探したい要素
    Returns:
        int: 要素の位置 無い場合は-1を返す
    """
    if element in array:
        return array.index(element)
    return -1


pettern = rcompile(r"^-?\d+\.?\d*?$")


def brackets(formula: list, bracket: str) -> list:
    """配列の括弧を探して計算する関数"""
    while bracket[0] in formula:
        left_bracket = indef_of(formula, bracket[0])
        right_bracket = indef_of(formula, bracket[1])
        if (
            left_bracket != 0 and bool(
                pettern.match(str(formula[left_bracket - 1]))
            )
        ):
            in_bracket = calc(formula[left_bracket + 1: right_bracket])
            del formula[left_bracket + 1: right_bracket]
            formula[left_bracket] = (
                in_bracket * float(formula.pop(left_bracket - 1))
            )
            formula.pop(left_bracket - 1)
        elif left_bracket != 0 and formula[left_bracket - 1] == "-":
            in_bracket = calc(formula[left_bracket + 1: right_bracket])
            del formula[left_bracket + 1: right_bracket]
            formula[left_bracket] = in_bracket * -1
            formula.pop(left_bracket - 1)
        elif (
            len(formula)-1 != right_bracket and
            pettern.match(str(formula[right_bracket + 1]))
        ):
            in_bracket = calc(formula[left_bracket + 1: right_bracket])
            del formula[left_bracket + 1: right_bracket]
            formula[left_bracket] = (
                in_bracket * float(formula.pop(right_bracket + 1))
            )
        else:
            formula[left_bracket] = calc(
                formula[left_bracket + 1: right_bracket]
            )
            del formula[left_bracket + 1: right_bracket + 1]
    return formula


def calc(formula: list) -> float:
    """引数に渡された式を評価する関数

    Args:
        formula (list):式
    Retuns:
        float:計算結果
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
    while "!" in formula:
        exclamation = formula.index("!")
        if not str(formula[exclamation - 1]).isdecimal():
            # 自然数ではない場合
            if int(formula[exclamation - 1]) < 0:
                # 負の数の場合
                formula[exclamation - 1] = (
                    f"-{factorial(abs(int(formula[exclamation-1])))}"
                )
                # 絶対値の階乗のマイナス
                formula.pop(exclamation)
        else:
            # 普通の階乗
            formula[exclamation -
                    1] = str(factorial(int(formula[exclamation - 1])))
            formula.pop(exclamation)
    while "^" in formula:
        hat = formula.index("^")
        formula[hat - 1] = str(
            float(formula[hat - 1]) ** float(formula.pop(hat + 1))
        )
        formula.pop(hat)
    while "*" in formula or "/" in formula or "%" in formula:
        asterisk = indef_of(formula, "*")
        slash = indef_of(formula, "/")
        percent = indef_of(formula, "%")
        if (slash != -1) and (
            (slash < asterisk or asterisk == -1) and
            (slash < percent or percent == -1)
        ):
            formula[slash - 1] = str(
                float(formula[slash - 1]) / float(formula.pop(slash + 1))
            )
            formula.pop(slash)
        elif asterisk != -1 and (asterisk < percent or percent == -1):
            formula[asterisk - 1] = str(
                float(formula[asterisk - 1]) * float(formula.pop(asterisk + 1))
            )
            formula.pop(asterisk)
        elif percent != -1:
            formula[percent - 1] = str(
                float(formula[percent - 1]) % float(formula.pop(percent + 1))
            )
            formula.pop(percent)
    while len(formula) > 1:
        formula[0] = str(float(formula[0]) + float(formula.pop(1)))
    return float(formula[0])


def calculator(str_formula: str) -> str:
    """渡された文字列を評価して返す関数

    Args:
        str_formula (str):評価したい文字列
    """
    # 引数が空文字列の場合に"0"を返す
    if str_formula == "":
        return "0"
    array_formula: list = []
    # 項ごとに分ける
    for char in str_formula:
        if char.isdecimal() or char == ".":
            if len(array_formula) == 0:
                array_formula.append(char)
            else:
                array_formula[-1] += char
        else:
            if char == "+":
                array_formula.append("")
            elif char == "-":
                array_formula.append("-")
            elif char in (
                "*", "/", "%", "!", "^", "(", ")", "{", "}", "[", "]"
            ):
                if len(array_formula) != 0 and array_formula[-1] == "-":
                    array_formula[-1] += "1"
                array_formula.append(char)
                array_formula.append("")
            else:
                raise ValueError()
    del_empty(array_formula)
    if str(x := calc(array_formula)).endswith(".0"):
        return str(int(x))
    return str(x)


print("数式を打ってください。(quitで終了)")
while (a := input(">")) != "quit":
    try:
        print(calculator(a))
    except (ValueError, IndexError):
        print("無効な値です")
    except OverflowError:
        print("オーバーフロー")
    except ZeroDivisionError:
        print("ゼロ除算が発生しました")
